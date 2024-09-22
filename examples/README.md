# Example

Examples are provided in this directory to demonstrate the use of classes.

`exmaple.py` is a simple CLI and used to explain the use of the classes.

This sample shows an example where a symbolic link refers to this project itself and is used as a submodule.

An example is provided in combination with pytest.

```shell
cd ${NN_IO_INTERACT}/examples/

# Run all tests
# It is necessary to set environment variables in `SSHProcessIO`, so please do so as well.
pytest -v -s tests/
```

## ProcessIO

A class named `ProcessIO` is provided in the file `process_io.py`.

This class is a basic class that launches the process you want to run, sends commands to it, and analyzes the logs.

```shell
cd ${NN_IO_INTERACT}/examples/

# Run partial tests
pytest -v -s -m "simple_process_test and easy" tests/
pytest -v -s -m "simple_process_test and hard" tests/
```

## SSHProcessIO

A class named `SSHProcessIO` is provided in the file `ssh_io.py`.

This class is to run a process in the remote machine via ssh.

If you want to try it manually on a remote machine, set the environment variables as follows.

```shell
# e.g.)
export REMOTE_USER_NAME="hogehoge"
export REMOTE_HOST_NAME="192.168.100.2"
export REMOTE_KEY_PATH="${HOME}/.ssh/id_fugafuga" # Prepare a key to login

cd ${NN_IO_INTERACT}/examples/
pytest -v -s -m "ssh_test" tests/
```

## DockerProcessIO

A class named `DockerProcessIO` is provided in the file `docker_io.py`.

This class is to run a process in the docker container.

```shell
# Build docker image
cd ${NN_IO_INTERACT}
docker build -f examples/Dockerfile -t nn/example-app:latest ./

cd ${NN_IO_INTERACT}/examples/
pytest -v -s -m "docker_test" tests/
```

## ProcessIO(in the docker container)

This is for cases where the files of this project have been copied or mounted in a docker container.
In this case, it is not necessary to use `DockerProcessIO`, but it is sufficient to start up `ProcessIO` in the container.

```shell
# Build docker image
cd ${NN_IO_INTERACT}
docker build -f examples/Dockerfile -t nn/example-app:latest ./

# Start docker images and mount
docker run -it --rm -v $(pwd)/:/app/work -w /app/work/examples --name example_app nn/example-app:latest bash

pytest -v -s -m "docker_inner_test" tests/
# exit or ctrl+D
```
