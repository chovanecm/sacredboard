# coding=utf-8
"""Fake TensorBoard."""
import sys
import time

import click


@click.command()
@click.option("--logdir")
@click.option("--host", default="0.0.0.0")
@click.option("--port", default="6006")
@click.option("--print-nonsense", is_flag=True, default=False)
@click.option("--print-nothing", is_flag=True, default=False)
@click.option("--address-in-use", is_flag=True, default=False)
@click.option("--sleep-time", default=20)
def mock_tensorboard(logdir, host, port, print_nonsense, print_nothing,
                     address_in_use, sleep_time):
    """Run fake TensorBoard."""
    if logdir is None:
        print('A logdir must be specified. Run `tensorboard --help` for '
              'details and examples.')
        return -1
    elif print_nothing:
        time.sleep(sleep_time)
    elif print_nonsense:
        for i in range(0, 150):
            print('Lorem ipsum %d' % i, file=sys.stderr)
            time.sleep(0.1)
    elif address_in_use:
        print('Tried to connect to port %d, but address is in use.' % 1234, file=sys.stderr)
    else:
        time.sleep(1)

        print('TensorBoard 1.8.0 at http://ntbthinkpad:%d' % 6006, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(mock_tensorboard())
