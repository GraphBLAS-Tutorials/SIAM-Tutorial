# SIAM-Tutorial

To build the Docker container, run the following (this only needs to be done once):

`$ ./build.sh`

To run the docker container that starts the notebook server, run the following:

`$ ./notebook.sh`

It will output something like this:

```
    Or copy and paste one of these URLs:
        http://5303f0affe22:8888/?token=<long hash>
     or http://127.0.0.1:8888/?token=<long hash

```

Paste one of these links into your browser to take you to the Jupyter notebook environment.  Use the second link (the one with 127.0.0.1) if your browser and the docker container are running on the same system; otherwise use the first link.

The notebook will start in the notebook-workspace directory. 
