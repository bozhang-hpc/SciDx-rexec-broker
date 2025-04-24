import argparse
from rexec_broker.broker import RExecBroker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--client_port", type=str, default="5559",
        help="The port for listening the clients' requests. [0-65535]"
    )

    parser.add_argument(
        "--server_port", type=str, default="5560",
        help="The port for listening the servers' requests. [0-65535]"
    )

    parser.add_argument(
        "--control_port", type=str, default="5561",
        help="The port for listening the termination signal. [0-65535]"
    )

    args = parser.parse_args()

    broker = RExecBroker(args)
    broker.run()