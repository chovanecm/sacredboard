import atexit
import os
import re
import select
import time
from subprocess import Popen, PIPE

TENSORBOARD_BINARY = "tensorboard"


class Process:
    instances = []  # type: Process

    def __init__(self, command):
        if type(command == list):
            self.command = command
        else:
            self.command = command.split(" ")

        self.proc = None  # type: Popen

    def run(self):
        environment = os.environ.copy()
        # necessary for reading from processes that don't flush stdout automatically
        environment["PYTHONUNBUFFERED"] = "1"
        self.proc = Popen(self.command, env=environment, stdout=PIPE)
        Process.instances.append(self)

    def is_running(self):
        return self.proc is not None and self.proc.returncode is not None

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

    def kill(self, wait=False):
        if self.proc is not None:
            self.proc.kill()
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
                instance.kill(wait)


# Kill all at exit
atexit.register(Process.terminate_all)


class ProcessError(BaseException):
    pass


class TensorboardNotFoundError(ProcessError):
    pass


class UnexpectedOutputError(ProcessError):
    def __init__(self, output, expected=None):
        self.expected = expected
        self.output = output


def run_tensorboard(logdir, listen_on="0.0.0.0", tensorboard_args=[]):
    tensorboard_instance = Process(
        TENSORBOARD_BINARY.split(" ") + ["--logdir", logdir, "--host", listen_on] + tensorboard_args)
    try:
        tensorboard_instance.run()
    except FileNotFoundError as ex:
        raise TensorboardNotFoundError(ex)

    # Read first line of output from tensorboard - it should contain the port where it listens
    data = tensorboard_instance.read_line(time_limit=10)
    search = re.search("on port ([0-9]+)", data)
    if search is not None:
        port = search.group(1)
        return port
    else:
        tensorboard_instance.kill()
        raise UnexpectedOutputError(data, expected="The port Tensorboard listens on.")
