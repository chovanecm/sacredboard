# Sacredboard

Sacredboard is a web dashboard for [Sacred](https://github.com/IDSIA/sacred).
 
It connects to the MongoDB database used by Sacred
and displays a list of experiments, their state, Sacred configuration and
the standard output from the running program.  
Python 3.5 and a modern web browser are  required for it to work properly.

## Features in version 0.1.2

- Get an overview of running and finished experiments in a table,
 such as experiment name, machine on which it runs etc.
- Get detailed information of the experiment,
 such as the text output produced by the experiment.
- Run [Tensorboard](https://www.tensorflow.org/versions/r0.10/how_tos/summaries_and_tensorboard/) 
    directly from the web console in order to see detailed information,
    charts and [Tensorflow](https://www.tensorflow.org) graph visualisations,
    provided that the experiment uses Sacred's 
    [Integration with Tensorflow](https://github.com/IDSIA/sacred/blob/develop/docs/tensorflow.rst)
     (currently in the development branch of Sacred).

### Changes in 0.1.2 since 0.1.1

- Added a command line option to specify a custom connection string for MongoDB,
thus enabling connections to password-protected databases etc.

### Changes in 0.1.1 since 0.1

- Added a command line option to specify the MongoDB collection that contains
the runs. This is useful when using a custom collection name or for
 [compatibility reasons](https://github.com/chovanecm/sacredboard/issues/20).

## Roadmap

### v0.2

- Filtering experiments based on their configuration
- Displaying the `info` dictionary

### Further Versions

- Filtering experiments based on custom queries on the data produced by experiments. 
- In addition, to support the users in using Sacredboard features,
 sacred will be enhanced with API to store common experiment information (such as error, accuracy etc).
- TBD

## Screenshots

Screenshots are available on a separate [Screenshots](./docs/screenshots.md) page.

## Installation and Running Sacredboard

Install sacredboard using `pip`:  

    pip install sacredboard



### Running

Sacredboard can be run simply by typing ``sacredboard`` to connect to
 a local MongoDB database listening on port 27017, database name `sacred`.
 
 To connect to another machine or database name, specifiy the connection string
 using the `-m host:port:db` option.
 
    sacredboard -m sacred
    
or, if you wish to connect to another machine and/or use a non-default
 name of the Sacred *runs* collection (`-mc`):
    
    sacredboard -m 192.168.1.1:27017:sacred -mc default.runs

For setting more advanced connection properties, use the `-mu` option
together with the Sacred database name ("sacred" in the example):

    sacredboard -mu mongodb://user:pwd@host/admin?authMechanism=SCRAM-SHA-1 sacred

See [MongoDB Connection String](https://docs.mongodb.com/manual/reference/connection-string/)
for more information.


The web browser with Sacredboard should open automatically.


To display help, run

    sacredboard --help


## References

- [Sacred](http://github.com/IDSIA/sacred) 


Feel free to open new issues in case of requests or bugs found.  
Maintainer / Developer: Martin Chovanec, chovamar@fit.cvut.cz
