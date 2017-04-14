# coding=utf-8
import atexit
import os
import select
import time
from subprocess import Popen, PIPE


class Process:
    instances = []  # type: List[Process]

    def __init__(self, command):
        if type(command == list):
            self.command = command
        else:
            self.command = command.split(" ")

        self.proc = None  # type: Popen

    def run(self):
        environment = os.environ.copy()
        # necessary for reading from processes that don't flush
        # stdout automatically
        environment["PYTHONUNBUFFERED"] = "1"
        self.proc = Popen(self.command, env=environment, stdout=PIPE)
        Process.instances.append(self)

    def is_running(self):
        return self.proc is not None and not bool(self.proc.poll())

    def read_line(self, time_limit=None):
        if self.proc is not None:
            poll_obj = select.poll()
            poll_obj.register(self.proc.stdout, select.POLLIN)
            start = time.time()
            while time_limit is None or time.time() - start < time_limit:
                poll_result = poll_obj.poll(0)
                if poll_result:
                    line = self.proc.stdout.readline().decode()
                    return line
            raise TimeoutError()
        else:
            return None

    def terminate(self, wait=False):
        if self.proc is not None:
            self.proc.stdout.close()
            self.proc.terminate()
            if wait:
                self.proc.wait()

    def pid(self):
        if self.proc is not None:
            return self.proc.pid
        else:
            return None

    @staticmethod
    def terminate_all(wait=False):
        """

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
        if getattr(select, "poll", None) is not None:
            return Process(command)
        else:
            return WindowsProcess(command)


class WindowsProcess(Process):
    def __init__(self, command):
        Process.__init__(self, command)

    def read_line(self, time_limit=None):
        """ Time limit has no effect.
         The operation will always block on Windows."""
        if self.proc is not None:
            return self.proc.stdout.readline().decode()
        else:
            return None


# Kill all on exit
atexit.register(Process.terminate_all)


class ProcessError(Exception):
    pass




class UnexpectedOutputError(ProcessError):
    def __init__(self, output, expected=None):
        self.expected = expected
        self.output = output

