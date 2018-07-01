FROM python:3-alpine
ADD server.py /
ADD mqtt_creds_server.py /
RUN pip install paho-mqtt
RUN pip install pytz
RUN pip install weather-api
ENTRYPOINT [ "python"]
CMD ["./server.py"]
