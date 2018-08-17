"""Module for managing TensorBoard processes."""

from sacredboard.app.process.process \
    import Process, ProcessError, UnexpectedOutputError
import time
import re

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


def run_tensorboard(logdir, listen_on="0.0.0.0", port=0, tensorboard_args=None, timeout=10):
    """
    Launch a new TensorBoard instance.

    :param logdir: Path to a TensorFlow summary directory
    :param listen_on: The IP address TensorBoard should listen on.
    :param port: Port number to listen on. 0 for a random port.
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
        ["--logdir", logdir, "--host", listen_on, "--port", str(port)] + tensorboard_args)
    try:
        tensorboard_instance.run()
    except FileNotFoundError as ex:
        raise TensorboardNotFoundError(ex)

    # Wait for a message that signaliezes start of Tensorboard
    start = time.time()
    data = ""
    while time.time() - start < timeout:
        line = tensorboard_instance.read_line_stderr(time_limit=timeout)
        data += line
        if "at http://" in line:
            port = parse_port_from_tensorboard_output(line)
            # Good case
            return port
        elif "TensorBoard attempted to bind to port" in line:
            break

    tensorboard_instance.terminate()
    raise UnexpectedOutputError(
        data,
        expected="Confirmation that Tensorboard has started"
    )


def parse_port_from_tensorboard_output(tensorboard_output: str) -> int:
    """
    Parse tensorboard port from its outputted message.

    :param tensorboard_output: Output message of Tensorboard
    in format TensorBoard 1.8.0 at http://martin-VirtualBox:36869
    :return: Returns the port TensorBoard is listening on.
    :raise UnexpectedOutputError
    """
    search = re.search("at http://[^:]+:([0-9]+)", tensorboard_output)
    if search is not None:
        port = search.group(1)
        return int(port)
    else:
        raise UnexpectedOutputError(tensorboard_output, "Address and port where Tensorboard has started,"
                                                        " e.g. TensorBoard 1.8.0 at http://martin-VirtualBox:36869")


if __name__ == "__main__":
    print(run_tensorboard("."))
