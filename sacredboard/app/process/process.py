# coding=utf-8
"""Module for launching processes and reading their output."""
import atexit
import os
import time
from subprocess import Popen, PIPE

import select


class Process:
    """A process that can be run and read output from."""

    instances = []  # type: List[Process]
    """Instances of all processes."""

    def __init__(self, command):
        """
        Define a new process but do not start it.

        :param command: A command to start. Parameters separated with spaces
         or as a list, e.g. "command arg1 arg2" or ["command", "arg1", "arg2"].
        """
        if type(command == list):
            self.command = command
        else:
            self.command = command.split(" ")

        self.proc = None  # type: Popen

    def run(self):
        """Run the process."""
        environment = os.environ.copy()
        # necessary for reading from processes that don't flush
        # stdout automatically
        environment["PYTHONUNBUFFERED"] = "1"
        self.proc = Popen(self.command, env=environment, stdout=PIPE, stderr=PIPE)
        Process.instances.append(self)

    def is_running(self):
        """Test if the process is running."""
        return self.proc is not None and not bool(self.proc.poll())

    def read_line(self, time_limit=None):
        """
        Read a line from the process.

        Block or wait for time_limit secs. Timeout does not work on Windows.

        :raise TimeoutError
        """
        return self._read_line("stdout", time_limit)

    def read_line_stderr(self, time_limit=None):
        """
        Read a line from the process standard error.

        Wait at most time_limit seconds for output, then :raise TimeoutError.
        """
        return self._read_line("stderr", time_limit)

    def _read_line(self, source, time_limit=None):
        if self.proc is not None:
            read_from = self._get_read_object(source)
            poll_obj = select.poll()
            poll_obj.register(read_from, select.POLLIN)
            start = time.time()
            while time_limit is None or time.time() - start < time_limit:
                poll_result = poll_obj.poll(0)
                if poll_result:
                    line = read_from.readline().decode()
                    return line
                else:
                    time.sleep(0.05)
            raise TimeoutError()
        else:
            return None

    def _get_read_object(self, source):
        if source == "stdout":
            read_from = self.proc.stdout
        elif source == "stderr":
            read_from = self.proc.stderr
        else:
            raise ValueError("Unknown source " + source + ". Valid: stdout, stderr")
        return read_from

    def terminate(self, wait=False):
        """Terminate the process."""
        if self.proc is not None:
            self.proc.stdout.close()
            self.proc.terminate()
            if wait:
                self.proc.wait()

    def pid(self):
        """Get the process id. Returns none for non-running processes."""
        if self.proc is not None:
            return self.proc.pid
        else:
            return None

    @staticmethod
    def terminate_all(wait=False):
        """
        Terminate all processes.

        :param wait: Wait for each to terminate
        :type wait: bool
        :return:
        :rtype:
        """
        for instance in Process.instances:
            if instance.is_running():
                instance.terminate(wait)

    @staticmethod
    def create_process(command):
        """
        Create a process using this factory method. This does not start it.

        :param command: A command to start. Parameters separated with spaces
         or as a list, e.g. "command arg1 arg2" or ["command", "arg1", "arg2"].
        """
        if getattr(select, "poll", None) is not None:
            return Process(command)
        else:
            return WindowsProcess(command)


class WindowsProcess(Process):
    """A class for a Windows process."""

    def __init__(self, command):
        """
       Define a new process but do not start it.

       :param command: A command to start. Parameters separated with spaces
        or as a list, e.g. "command arg1 arg2" or ["command", "arg1", "arg2"].
       """
        Process.__init__(self, command)

    def read_line(self, time_limit=None):
        """
        Read a line from the process.

        On Windows, this the time_limit has no effect, it always blocks.
        """
        if self.proc is not None:
            return self.proc.stdout.readline().decode()
        else:
            return None

    def read_line_stderr(self, time_limit=None):
        """
        Read a line from the process.

        On Windows, this the time_limit has no effect, it always blocks.
        """
        if self.proc is not None:
            return self.proc.stderr.readline().decode()
        else:
            return None


# Kill all on exit
atexit.register(Process.terminate_all)


class ProcessError(Exception):
    """A process-related exception."""

    pass


class UnexpectedOutputError(ProcessError):
    """An unexpected output produced by the process."""

    def __init__(self, output, expected=None):
        """Create an unexpected output exception."""
        self.expected = expected
        self.output = output
