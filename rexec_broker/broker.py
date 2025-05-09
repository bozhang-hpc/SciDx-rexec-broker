import logging
import threading
from typing import Any, Dict
import zmq
import zmq.utils.monitor

EVENT_MAP = {}

def setup_event_map(event_map: list):
    logging.debug("Event names:")
    for name in dir(zmq):
        if name.startswith('EVENT_'):
            value = getattr(zmq, name)
            logging.debug(f"{name:21} : {value:4}")
            event_map[value] = name

def event_monitor(monitor_socket: zmq.Socket, socket_name: str) -> None:
    while monitor_socket.poll():
        evt: Dict[str, Any] = {}
        mon_evt = zmq.utils.monitor.recv_monitor_message(monitor_socket)
        evt.update(mon_evt)
        evt['description'] = EVENT_MAP[evt['event']]
        logging.debug(f"{socket_name} Event: {evt}")

        if evt['event'] == zmq.EVENT_MONITOR_STOPPED:
            break

    monitor_socket.close()
    logging.debug("event monitor thread done!")

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

        self.debug = False
        if args.loglevel == logging.DEBUG:
            if zmq.zmq_version_info() > (4, 0):
                self.debug = True
                setup_event_map(EVENT_MAP)
                self.frontend_monitor = self.frontend_socket.get_monitor_socket()
                self.backend_monitor = self.backend_socket.get_monitor_socket()
                self.control_monitor = self.control_socket.get_monitor_socket()
            else:
                raise RuntimeError("monitoring in libzmq version < 4.0 is not supported")
            
    def run(self):
        try:
            logging.info(f"Proxy Starts...")
            if self.debug:
                frontend_monitor_thread = threading.Thread(target=event_monitor, args=(self.frontend_monitor,"Client Socket",))
                backend_monitor_thread = threading.Thread(target=event_monitor, args=(self.backend_monitor,"Server Socket",))
                control_monitor_thread = threading.Thread(target=event_monitor, args=(self.control_monitor,"Control Socket",))

                frontend_monitor_thread.start()
                backend_monitor_thread.start()
                control_monitor_thread.start()

            zmq.proxy_steerable(self.frontend_socket, self.backend_socket, None, self.control_socket)

        except KeyboardInterrupt:
            print("W: interrupt received, stopping broker...")

        finally:
            self.frontend_socket.close()
            self.backend_socket.close()
            self.control_socket.close()

            if self.debug:
                self.frontend_monitor.disable_monitor()
                self.backend_monitor.disable_monitor()
                self.control_monitor.disable_monitor()

            self.zmq_context.destroy()
