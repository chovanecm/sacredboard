"""Module for managing TensorBoard processes."""
import re

from sacredboard.app.process.process \
    import Process, ProcessError, UnexpectedOutputError

TENSORBOARD_BINARY = "tensorboard"


def stop_all_tensorboards():
    """Terminate all TensorBoard instances."""
    for process in Process.instances:
        print("Process '%s', running %d" % (process.command[0],
                                            process.is_running()))
        if process.is_running() and process.command[0] == "tensorboard":
            process.terminate()


class TensorboardNotFoundError(ProcessError):
    """TensorBoard binary not found."""

    pass


def run_tensorboard(logdir, listen_on="0.0.0.0", tensorboard_args=None, timeout=10):
    """
    Launch a new TensorBoard instance.

    :param logdir: Path to a TensorFlow summary directory
    :param listen_on: The IP address TensorBoard should listen on.
    :param tensorboard_args: Additional TensorBoard arguments.
    :param timeout: Timeout after which the Timeout
    :type timeout: float
    :return: Returns the port TensorBoard is listening on.
    :raise UnexpectedOutputError
    :raise TensorboardNotFoundError
    :raise TimeoutError
    """
    if tensorboard_args is None:
        tensorboard_args = []
    tensorboard_instance = Process.create_process(
        TENSORBOARD_BINARY.split(" ") +
        ["--logdir", logdir, "--host", listen_on] + tensorboard_args)
    try:
        tensorboard_instance.run()
    except FileNotFoundError as ex:
        raise TensorboardNotFoundError(ex)

    # Read first line of output from tensorboard - it should contain
    # the port where it is listening on
    data = tensorboard_instance.read_line_stderr(time_limit=timeout)
    search = re.search("at http://[.+]:([0-9]+)", data)
    if search is not None:
        port = search.group(1)
        return port
    else:
        tensorboard_instance.terminate()
        raise UnexpectedOutputError(
            data,
            expected="The port that Tensorboard is listening on."
        )
