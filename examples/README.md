# Example

Examples are provided in this directory to demonstrate the use of classes.

`example_app.py` is a virtual development target software with simple CLI and used to explain the use of the classes.

It is recommended that it be used alone once.

```shell
cd ${BLABOT}/examples/
uv run python example_app.py

# sample commands
> sample-status
> sample-ctrl on
> sample-ctrl off
```

The samples are provided in two major formats: Pytest and a single python script file.

## Single python script

```shell
cd ${BLABOT}/examples/
uv run python example_usage.py
```

## ProcessIO

A class named `ProcessIO` is provided in the file `process_io.py`.

This class is a basic class that launches the process you want to run, sends commands to it, and analyzes the logs.

```shell
cd ${BLABOT}/examples/

# Run partial tests
uv run pytest -v -s -m "simple_process_test and easy" tests/
uv run pytest -v -s -m "simple_process_test and hard" tests/
```

## DeviceIO

```mermaid
graph LR
    subgraph HostPC["Host PC"]
        Software["Software"]
        DeviceIO["DeviceIO"]
    end

    subgraph SerialDev["Serial Device"]
        SoftwareDev["Software (flashed)"]
    end

    Software -.->|flash| SoftwareDev
    DeviceIO <-->|"Send command
                  +
                  Receive result
                  (via serial device,
                  /dev/ttyUSB0, ...)"| SoftwareDev
```

A class named `DeviceIO` is provided in the file `device_io.py`.

This class is to communicate with serial device such as /dev/ttyUSB0.

By following the steps below, you can try it virtually with socat.

And the following procedure is the same as executing the `${BLABOT}/examples/scripts/run_device_test.sh` file, so you may execute that one.

```shell
# Prepare virtual device
sudo apt install socat # if socat is not installed in your environment
socat PTY,link=/tmp/ttyV0,echo=0 PTY,link=/tmp/ttyV1,echo=0 &

# Run example_app.py with input/output set to /tmp/ttyV0
cd ${BLABOT}/examples/
uv run python example_app.py < /tmp/ttyV0 > /tmp/ttyV0 2>&1

# Run example test (In a terminal different from the terminal where example_app.py is executed.)
cd ${BLABOT}/examples/
uv run pytest -v -s -m "device_test" tests/

# optional)
# Input/Output can be confirmed by minicom, and other tools.
# e.g)
sudo apt install minicom # if minicom is not installed in your environment
minicom -D /tmp/ttyV1 # Exit: ctrl+a -> x
```

## SSHProcessIO

```mermaid
graph LR
    subgraph HostPC["Host PC"]
        Software["Software"]
        SSHIO["SSHProcessIO"]
    end

    subgraph RemotePC["Remote PC"]
        Software_copied["Software (copied)"]
    end

    Software -.->|Copy| Software_copied
    SSHIO <-->|"Send command
                +
                Receive result
                (via SSH)"| Software_copied
```

A class named `SSHProcessIO` is provided in the file `ssh_io.py`.

This class is to run a process in the remote machine via ssh.

If you want to try it manually on a remote machine, set the environment variables as follows.

```shell
# e.g.)
export REMOTE_USER_NAME="hogehoge"
export REMOTE_HOST_NAME="192.168.100.2"
export REMOTE_KEY_PATH="${HOME}/.ssh/id_fugafuga" # Prepare a key to login

cd ${BLABOT}/examples/
uv run pytest -v -s -m "ssh_test" tests/
```

## DockerIO(DockerRunIO + DockerExecIO)

```mermaid
graph LR
    subgraph HostPC["Host PC"]
        Software["Software"]
        DockerIO["DockerIO
                  (No need to be
                  in container)"]
    end

    subgraph Container["Docker container"]
        Software_copied["Software (copied)"]
    end

    Software -.->|Copy or mount| Software_copied
    DockerIO <-->|"Send command
                   +
                   Receive result"| Software_copied
```

`DockerRunIO` and `DockerExecIO` are provided in the file `docker_io.py`.

These classes are to run a process in the docker container.

```shell
# Pull docker image
docker pull ghcr.io/nunoya-yuma/blabot/example-app:latest

# Build using Docker Compose (Recommended)
cd ${BLABOT}/examples
docker compose build

# Or build using plain Docker
cd ${BLABOT}
docker build -f examples/Dockerfile -t ghcr.io/nunoya-yuma/blabot/example-app:latest ./

cd ${BLABOT}/examples/
uv run pytest -v -s -m "docker_test" tests/
```

## ProcessIO(in the docker container)

```mermaid
graph LR
    subgraph HostPC["Host PC"]
        Software["Software"]
    end

    subgraph Container["Docker container"]
        Software_copied["Software (copied)"]
        ProcessIO["ProcessIO"]
    end

    HostPC -.->|Copy or mount| ProcessIO
    Software -.->|Copy or mount| Software_copied
    ProcessIO <-->|"Send command
                   +
                   Receive result"| Software_copied
```

This is for cases where the files of this project have been copied or mounted in a docker container.
In this case, it is not necessary to use `DockerRunIO` or `DockerExecIO`, but it is sufficient to start up `ProcessIO` in the container.

```shell
# Build and run using Docker Compose (Recommended)
cd ${BLABOT}/examples/
docker compose run --rm example-app pytest -v -s -m docker_inner_test tests/

# Alternative: Using plain Docker
cd ${BLABOT}
docker build -f examples/Dockerfile -t ghcr.io/nunoya-yuma/blabot/example-app:latest ./
docker run -it --rm -v $(pwd):/app/work -w /app/work/examples --name example_app ghcr.io/nunoya-yuma/blabot/example-app:latest pytest -v -s -m docker_inner_test tests/
```
