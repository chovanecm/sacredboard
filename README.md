# Sacredboard

Sacredboard is a web dashboard for the [Sacred](https://github.com/IDSIA/sacred)
machine learning experiment management tool.
 
It connects to the MongoDB database used by Sacred
and displays a list of experiments, their state, Sacred configuration and
the standard output from the running program.  
Python 3.5 and a modern web browser are  required for it to work properly.

### Project Background (is Sacredboard dead?)

Sacredboard was written as a part of a [master's thesis](https://dspace.cvut.cz/bitstream/handle/10467/69995/F8-DP-2017-Chovanec-Martin-thesis.pdf?sequence=1&isAllowed=y) at Czech Technical University in 2016 and 2017. Supervised by the main developer of Sacred (Klaus Greff from the [Swiss AI Lab IDSIA](http://www.idsia.ch/)), who promoted Sacredboard on the Sacred homepage and at the end of his talk at the [SciPy 2017 Python conference](https://www.youtube.com/watch?v=qqg7RO0o1OE), it has become used by more people that I expected.

Unfortunately, the days I was full-time working on the tool as a student writing his thesis are gone. Sacredboard is now a side project, updated rather once in a while than on a regular basis, mainly because of its active users that deserve their requests for improvements and bugfixes to be addressed.

# Features in version 0.4

- Get an overview of running and finished experiments in a table,
 such as experiment name, machine on which it runs etc.
- Filter experiments
- Get detailed information of the experiment,
 such as the text output produced by the experiment.
- Run [Tensorboard](https://www.tensorflow.org/versions/r0.10/how_tos/summaries_and_tensorboard/) 
    directly from the web console in order to see detailed information,
    charts and [Tensorflow](https://www.tensorflow.org) graph visualisations,
    provided that the experiment uses Sacred's 
    [Integration with Tensorflow](http://sacred.readthedocs.io/en/latest/tensorflow.html)
     (this feature was broken for a long time and is (partially) fixed in the current dev version)
- Visualise [Metrics](http://sacred.readthedocs.io/en/latest/collected_information.html#metrics-api) in a chart.
- Use the MongoDB and newly also FileStorage backend (experimental, thanks to [Gideon Dresdner](https://github.com/gideonite))
- Delete experiments from the UI

## Roadmap

### Further Versions
- Deleting experiments including related records, such as artifacts
- [Customized formatting of the result column](https://github.com/chovanecm/sacredboard/issues/63)
- Write wiki for developers :-)
- TBD

## Screenshots

Screenshots are available on a separate [Screenshots](./docs/screenshots.md) page.

## Installation and Running Sacredboard

Install sacredboard using `pip`:  

    pip install sacredboard

To install the latest development version with new features, run:

    pip install https://github.com/chovanecm/sacredboard/archive/develop.zip

### Dependencies

Sacredboard may require additional dependencies to install, especilly Python3 development files and a C compiler:

On Ubuntu/Debian:

    libpython3-dev
    build-essential

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

## Contributing

Contributions to Sacred are welcomed (see issues for inspiration).
The project tries to follow the git-flow workflow. Therefore,
contributions of new features should be developed against the `develop` branch. Thank you!


## References

- [Sacred](http://github.com/IDSIA/sacred) 


Feel free to open new issues in case of requests or bugs found.  
Maintainer / Developer: Martin Chovanec, chovamar@fit.cvut.cz


Current master branch status:
[![Build Status](https://travis-ci.org/chovanecm/sacredboard.svg?branch=master)](https://travis-ci.org/chovanecm/sacredboard)
[![Coverage Status](https://coveralls.io/repos/github/chovanecm/sacredboard/badge.svg?branch=master)](https://coveralls.io/github/chovanecm/sacredboard?branch=master)


Current develop branch status:
[![Build Status](https://travis-ci.org/chovanecm/sacredboard.svg?branch=develop)](https://travis-ci.org/chovanecm/sacredboard)
[![Coverage Status](https://coveralls.io/repos/github/chovanecm/sacredboard/badge.svg?branch=develop)](https://coveralls.io/github/chovanecm/sacredboard?branch=develop)
