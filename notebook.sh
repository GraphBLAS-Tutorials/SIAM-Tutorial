docker run --rm --user root -e NB_UID=$(id -u) -e NB_GID=$(id -g) -p 8888:8888 \
	   -w /home/jovyan/workspace \
	   -v `pwd`/notebook-workspace:/home/jovyan/workspace  \
	   -it graphblas/pygraphblas-siam21-tutorial:latest
