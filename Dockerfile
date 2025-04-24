FROM python:3.13.1

WORKDIR /broker

COPY rexec_broker /broker/rexec_broker
COPY requirements.txt /broker
COPY run_broker.py /broker

RUN pip install -r requirements.txt

ENV client_port=5559
ENV server_port=5560
ENV control_port=5561

CMD ["sh", "-c", "python run_broker.py                \
                  --client_port ${client_port}          \
                  --server_port ${server_port}          \
                  --control_port ${control_port}"]