# coding=utf-8
import os

import pytest as py

import sacredboard.app.process.process as p
import sacredboard.tests.app.process.fixtures.tensorboard as mock_tensorboard

path = os.path.dirname(mock_tensorboard.__file__)

p.TENSORBOARD_BINARY = "python %s/tensorboard.py" % path


@py.mark.timeout(15)
def test_run_tensorboard():
    port = p.run_tensorboard("/tmp/logdir")
    assert port == "6006"


@py.mark.timeout(15)
def test_run_tensorboard_other_output():
    with py.raises(p.UnexpectedOutputError) as ex:
        port = p.run_tensorboard("/tmp/logdir",
                                 tensorboard_args=["--print-nonsense"])


@py.mark.timeout(15)
def test_run_tensorboard_address_in_use():
    with py.raises(p.UnexpectedOutputError) as ex:
        port = p.run_tensorboard("/tmp/logdir",
                                 tensorboard_args=["--address-in-use"])


@py.mark.timeout(15)
def test_run_tensorboard_binary_not_found():
    original_binary = p.TENSORBOARD_BINARY
    p.TENSORBOARD_BINARY = "/tmp/asdf__4567897"
    with py.raises(p.TensorboardNotFoundError) as ex:
        port = p.run_tensorboard("/tmp/logdir",
                                 tensorboard_args=["--address-in-use"])
    p.TENSORBOARD_BINARY = original_binary


@py.mark.timeout(15)
def test_run_tensorboard_timeout():
    with py.raises(TimeoutError) as ex:
        port = p.run_tensorboard("/tmp/logdir",
                                 tensorboard_args=["--print-nothing"])
