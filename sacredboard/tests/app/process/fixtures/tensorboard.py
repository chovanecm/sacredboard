# coding=utf-8
"""Fake TensorBoard."""
import sys
import time

import click

@click.command()
@click.option("--logdir")
@click.option("--host", default="0.0.0.0")
@click.option("--print-nonsense", is_flag=True, default=False)
@click.option("--print-nothing", is_flag=True, default=False)
@click.option("--address-in-use", is_flag=True, default=False)
@click.option("--sleep-time", default=20)
def mock_tensorboard(logdir, host, print_nonsense, print_nothing,
                     address_in_use, sleep_time):
    """Run fake TensorBoard."""
    if logdir is None:
        print('A logdir must be specified. Run `tensorboard --help` for '
              'details and examples.')
        return -1
    elif print_nothing:
        time.sleep(sleep_time)
    elif print_nonsense:
        print('Lorem ipsum')
        time.sleep(sleep_time)
    elif address_in_use:
        print('Tried to connect to port %d, but address is in use.' % 1234)
        time.sleep(sleep_time)
    else:
        time.sleep(1)
        print('Starting TensorBoard %s on port %d' % ('...', 6006))


if __name__ == "__main__":
    sys.exit(mock_tensorboard())
