# coding=utf-8
import os
import pytest as py
import sacredboard.tests.app.process.fixtures.tensorboard as mock_tensorboard

import sacredboard.app.process.process as p
import sacredboard.app.process.tensorboard

path = os.path.dirname(mock_tensorboard.__file__)

sacredboard.app.process.tensorboard.TENSORBOARD_BINARY = "python %s/tensorboard.py" % path


@py.mark.timeout(15)
def test_run_tensorboard():
    port = sacredboard.app.process.tensorboard.run_tensorboard("/tmp/logdir")
    assert port == "6006"


@py.mark.timeout(15)
def test_run_tensorboard_other_output():
    with py.raises(p.UnexpectedOutputError) as ex:
        port = sacredboard.app.process.tensorboard.run_tensorboard("/tmp/logdir",
                                                                   tensorboard_args=["--print-nonsense"])


@py.mark.timeout(15)
def test_run_tensorboard_address_in_use():
    with py.raises(p.UnexpectedOutputError) as ex:
        port = sacredboard.app.process.tensorboard.run_tensorboard("/tmp/logdir",
                                                                   tensorboard_args=["--address-in-use"])


@py.mark.timeout(15)
def test_run_tensorboard_binary_not_found():
    original_binary = sacredboard.app.process.tensorboard.TENSORBOARD_BINARY
    sacredboard.app.process.tensorboard.TENSORBOARD_BINARY = "/tmp/asdf__4567897"
    with py.raises(sacredboard.app.process.tensorboard.TensorboardNotFoundError) as ex:
        port = sacredboard.app.process.tensorboard.run_tensorboard("/tmp/logdir",
                                                                   tensorboard_args=["--address-in-use"])
    sacredboard.app.process.tensorboard.TENSORBOARD_BINARY = original_binary


@py.mark.timeout(1)
def test_run_tensorboard_timeout():
    """ Fails on Windows because of missing "poll" on stdout. """
    with py.raises(TimeoutError) as ex:
        port = sacredboard.app.process.tensorboard.run_tensorboard("/tmp/logdir",
                                                                   tensorboard_args=["--print-nothing"],
                                                                   timeout=0.5)
