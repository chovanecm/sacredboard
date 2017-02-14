# coding=utf-8
import atexit
import os
import re
import select
import time
from subprocess import Popen, PIPE


TENSORBOARD_BINARY = "tensorboard"


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


class TensorboardNotFoundError(ProcessError):
    pass


class UnexpectedOutputError(ProcessError):
    def __init__(self, output, expected=None):
        self.expected = expected
        self.output = output


def stop_all_tensorboards():
    for process in Process.instances:
        print("Process '%s', running %d" % (process.command[0],
                                            process.is_running()))
        if process.is_running() and process.command[0] == "tensorboard":
            process.terminate()


def run_tensorboard(logdir, listen_on="0.0.0.0", tensorboard_args=None):
    if tensorboard_args is None:
        tensorboard_args = []
    tensorboard_instance = Process.create_process(
        TENSORBOARD_BINARY.split(" ")
        + ["--logdir", logdir, "--host", listen_on] + tensorboard_args)
    try:
        tensorboard_instance.run()
    except FileNotFoundError as ex:
        raise TensorboardNotFoundError(ex)

    # Read first line of output from tensorboard - it should contain
    # the port where it listens
    data = tensorboard_instance.read_line(time_limit=10)
    search = re.search("on port ([0-9]+)", data)
    if search is not None:
        port = search.group(1)
        return port
    else:
        tensorboard_instance.terminate()
        raise UnexpectedOutputError(
            data,
            expected="The port Tensorboard that listens on."
            )
