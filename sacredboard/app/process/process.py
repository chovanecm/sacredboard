import re
from subprocess import Popen, PIPE


def run_tensorboard(logdir, listen_on="0.0.0.0"):
    tensorboard_instance = run_process("tensorboard", ["--logdir", logdir, "--host", listen_on])
    # Read first line of output from tensorboard - it should contain the port where it listens
    data = tensorboard_instance.stdout.readline()
    search = re.search("on port ([0-9]+)", data.decode())
    return search.group(1)


running_processes = []


def run_process(path, args):
    """

    :param path:
    :type path: list
    :param args:
    :type args: list
    :return:
    :rtype:
    """
    proc = Popen([path] + args, stdout=PIPE)
    running_processes.append(proc)
    return proc
