# sacredboard
Sacred is a web dashboard for [sacred](https://github.com/IDSIA/sacred) showing overview of both running and finished machine learning experiments.

The information shown are based on data caught by sacred's mongodb observer.

## Roadmap
These are the things to do:
### v0.1
- Displaying an overview of running and finished experiments in a table, such as experiment name, machine on which it runs etc.
- Running [Tensorboard](https://www.tensorflow.org/versions/r0.10/how_tos/summaries_and_tensorboard/) from the web console in order to see detailed information, charts and [Tensorflow](https://www.tensorflow.org) graph visualisations, when the experiment was using Tensorboard
- Showing a detailed information of the experiment, such as text output produced by the programme, possibly with some graphs so that use doesn't have to run Tensorboard.

### v0.2 or later
- Filtering experiments based on custom queries on measured data.
- TBD
In addition, to support the users in using sacredboard features, sacred will be enhanced with API for storing common experiment information (such as error, accuracy etc).


## Running sacredboard
``python webapp.py``
Expects the mongo database to run on localhost, port 27017, database name sacred

``python webapp.py -m MY_DB``
Expects the mongo database to run on localhost, port 27017, database name MY_DB

``python webapp.py -m my_computer:27018:MY_DB``
Expects the mongo database to run on my_computer, port 27018, database name MY_DB

After starting the application, the listen address and port should appear. Open then /runs (e.g.: http://127.0.0.1:5000/runs) in your web browser and play with sacredboard.
