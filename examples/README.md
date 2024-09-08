# Example

Examples are provided in this directory to demonstrate the use of classes.

`exmaple.py` is a simple CLI and used to explain the use of the classes.

This sample shows an example where a symbolic link refers to this project itself and is used as a submodule.

## pytest

An example is shown using pytest.

```shell
cd ${NN_IO_INTERACT}/examples/

# Run all tests
# It is necessary to set environment variables in `ssh-related testing`, so please do so as well.
pytest -v -s tests/

# Run partial tests
pytest -v -s -m "easy and simple_process_test" tests/
pytest -v -s -m "hard and simple_process_test" tests/
```

> ssh-related testing

This is a test of the class that does the input at the ssh destination, but for that test, it enters itself via ssh and performs the test.

```shell
export REMOTE_HOST_NAME="localhost"
export REMOTE_KEY_PATH="$your_key" # Prepare a key to login your computer itself
pytest -v -s -m "ssh_test" tests/
```
