FROM python:3-alpine
ADD server.py /
RUN pip install pip install paho-mqtt
ENTRYPOINT [ "python"]
CMD ["./temp_server.py"]
