# SciDx Remote Execution Broker
This repository contains the implementation of remote execution broker in [SciDx software stack](https://scidx.sci.utah.edu/) with the support to [DataSpaces](https://dataspaces.sci.utah.edu/) Data Staging framework. It routes the client requests to the horizontally-scaled backend servers and allows both the user client and backend server to connect to a fixed ip address.

## Requirements
* Python __>=3.9__
* [PyZMQ](https://pypi.org/project/pyzmq/)

## Usage
```Bash
python3 run_broker.py [-h] [--client_port CLIENT_PORT] [--server_port SERVER_PORT] [--control_port CONTROL_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --client_port CLIENT_PORT
                        The port for listening the clients' requests. [0-65535]
  --server_port SERVER_PORT
                        The port for listening the servers' requests. [0-65535]
  --control_port CONTROL_PORT
                        The port for listening the termination signal. [0-65535]
```

## License
This project is licensed under the [Apache License 2.0](LICENSE).