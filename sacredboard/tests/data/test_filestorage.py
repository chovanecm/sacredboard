"""Tests for the file storage backend."""

# coding=utf-8
import bson
import pytest
import json
import tempfile
import os

from sacredboard.app.data.filestorage import FileStorage


def create_tmp_datastore():
    """
    Rather than mocking the file system, this actually creates some temporary files that emulate the file store system
    in Sacred. Unfortunately, Sacred and Sacredboard are completely decoupled, which makes it impossible to ensure that
    this standard is upheld throughout the sacred system.
    
    :return: dict
    """
    config = {"length": None, "n_input": 255, "batch_size": None,
         "dataset_path": "./german-nouns.hdf5", "validation_ds": "validation",
         "log_dir": "./log/rnn500_dropout0.5_lrate1e-4_minibatch_1000steps",
         "seed": 144363069, "dropout_keep_probability": 0.5,
         "max_character_ord": 255, "training_ds": "training", "num_classes": 3,
         "training_steps": 1000, "learning_rate": 0.0001, "hidden_size": 500}

    run = {"status": "COMPLETED",
                        "_id": "57f9efb2e4b8490d19d7c30e",
                        "info": {}, "resources": [],
                        "host": {"os": "Linux",
                                 "os_info": "Linux-3.16.0-38-generic-x86_64-with-LinuxMint-17.2-rafaela",
                                 "cpu": "Intel(R) Core(TM) i3 CPU       M 370  @ 2.40GHz",
                                 "python_version": "3.4.3",
                                 "python_compiler": "GCC 4.8.4",
                                 "cpu_count": 4,
                                 "hostname": "ntbacer"},
                        "experiment": {"doc": None, "sources": [[
                            "/home/martin/mnt/noun-classification/train_model.py",
                            "86aaa9b81d6e32a181598ed78bb1d7a1"]],
                                       "dependencies": [["h5py", "2.6.0"],
                                                        ["numpy", "1.11.2"],
                                                        ["sacred", "0.6.10"]],
                                       "name": "German nouns"},
                        "result": 2403.52, "artifacts": [], "comment": "",
                        # N.B. time formatting is different between mongodb and file store.
                        "start_time": "2017-06-02T07:13:05.305845",
                        "stop_time": "2017-06-02T07:14:02.455460",
                        "heartbeat": "2017-06-02T07:14:02.452597",
           "captured_out": "Output: \n"}

    experiment_dir = tempfile.mkdtemp()
    experiment42 = os.path.join(experiment_dir, "42") # experiment number 42
    os.mkdir(experiment42)

    with open(os.path.join(experiment42, "config.json"), 'w') as config_file:
       json.dump(config, config_file)

    with open(os.path.join(experiment42, "run.json"), 'w') as run_file:
        json.dump(run, run_file)

    return experiment_dir

@pytest.fixture
def tmpfilestore() -> FileStorage:
    """Fixture that prepares a file store in /tmp for dependency injection."""
    dir = create_tmp_datastore()
    return FileStorage(dir)

def test_get_run(tmpfilestore : FileStorage):
    """Tests the get_run function."""
    run42 = tmpfilestore.get_run(42)

    for key in ["info", "resources", "host", "experiment", "result", "artifacts", "comment", "start_time", "stop_time",
                "heartbeat", "captured_out", "config"]:
        assert key in run42

def test_get_runs(tmpfilestore : FileStorage):
    """Tests the get_runs function."""
    runs = tmpfilestore.get_runs()
    runs = list(runs)

    assert 1 == len(runs)

    run = runs[0]
    for key in ["info", "resources", "host", "experiment", "result", "artifacts", "comment", "start_time", "stop_time",
                "heartbeat", "captured_out", "config"]:
        assert key in run
