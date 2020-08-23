import time
import sys

# import numpy as np

from prometheus_client import start_http_server
from prometheus_client import Gauge

from daemon import Daemon

from functions import get_data
# from functions import create_logger
from functions import customEx

import logging

sleep_duration = 60

# logger_events = create_logger('read_sensor.log', 'events')
# logger_data = create_logger(
#     file='data.log', log='temps', form='%(asctime)s %(message)s')


root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def main():
    root.info(f'Reading data and writing to database every {sleep_duration} seconds.')
    # start_http_server(8000)
    prom_temp = Gauge(
        'Temperature', 'Temperature measured by the DHT22 Sensor')
    prom_humid = Gauge(
        'Humidity', 'Relative Humidity measured by the DHT22 Sensor')
    while True:
        t_start = time.time()
        try:
            date, humidity, temperature = get_data()
            if None in (humidity, temperature):
                raise customEx
            # customEx can also be raised in get_data()! 
        except customEx:
            time.sleep(int(sleep_duration/10))
            continue
        # print(date, humidity, temperature)
        root.debug('climate inside: T[C] = {temp}, rH[%] = {hum}'.format(hum=humidity, temp=temperature))
        # logger_data.info(f'; {humidity}; {temperature}')
        prom_temp.set(temperature)
        prom_humid.set(humidity)
        t_end = time.time()
        t_delta = t_end - t_start
        try:
            first
        except NameError as e:
            first = False
            start_http_server(8000)
        try:
            time.sleep(sleep_duration - t_delta)
        except ValueError:
            continue


class MyDaemon(Daemon):

    def run(self):
        main()

if __name__ == '__main__':
    main()
    # daemon = MyDaemon('/tmp/daemon-telegram-bot.pid')
    # if len(sys.argv) == 2:
    #     if 'start' == sys.argv[1]:
    #         daemon.start()
    #     elif 'stop' == sys.argv[1]:
    #         daemon.stop()
    #     elif 'restart' == sys.argv[1]:
    #         daemon.restart()
    #     else:
    #         print("Unknown command")
    #         sys.exit(2)
    #     sys.exit(0)
    # else:
    #     print("usage: {} start|stop|restart".format(
    #         sys.argv[0]))  # % sys.argv[0]
    #     sys.exit(2)
