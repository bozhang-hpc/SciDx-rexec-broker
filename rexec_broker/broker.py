import zmq

class RExecBroker:
    def __init__(self, args):
        self.zmq_context = zmq.Context()
        
        self.frontend_zmq_addr = "tcp://*:" + args.client_port
        self.frontend_socket = self.zmq_context.socket(zmq.ROUTER)
        self.frontend_socket.bind(self.frontend_zmq_addr)

        self.backend_zmq_addr = "tcp://*:" + args.server_port
        self.backend_socket = self.zmq_context.socket(zmq.DEALER)
        self.backend_socket.bind(self.backend_zmq_addr)

        self.control_zmq_addr = "tcp://*:" + args.control_port
        self.control_socket = self.zmq_context.socket(zmq.REP)
        self.control_socket.bind(self.control_zmq_addr)

    def run(self):
        try:
            zmq.proxy_steerable(self.frontend_socket, self.backend_socket, None, self.control_socket)
        except KeyboardInterrupt:
            print("W: interrupt received, stopping broker...")
        finally:
            self.frontend_socket.close()
            self.backend_socket.close()
            self.control_socket.close()
            self.zmq_context.destroy()
