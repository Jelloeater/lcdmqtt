FROM python:3-alpine
ADD server.py /
ADD mqtt_creds_client.py /
RUN pip install paho-mqtt
ENTRYPOINT [ "python"]
CMD ["./server.py"]
