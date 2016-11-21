# sacredboard
Dashboard for sacred

## Running sacredboard
``python webapp.py``
Expects the mongo database to run on localhost, port 27017, database name sacred

``python webapp.py -m MY_DB``
Expects the mongo database to run on localhost, port 27017, database name MY_DB

``python webapp.py -m my_computer:27018:MY_DB``
Expects the mongo database to run on my_computer, port 27018, database name MY_DB

After starting the application, the listen address and port (default: http://127.0.0.1:5000) should appear.
Open it in your web browser and play with sacredboard.
