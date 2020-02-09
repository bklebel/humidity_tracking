import time
from functions import get_data
from functions import create_logger

import numpy as np

from prometheus_client import start_http_server
from prometheus_client import Gauge


from daemon import Daemon


sleep_duration = 60

logger_events = create_logger('read_sensor.log', 'events')
logger_data = create_logger(
    file='data.log', log='temps', form='%(asctime)s %(message)s')


def main():
    logger_events.info(f'Reading data and writing to database every {sleep_duration} seconds.')
    prom_temp = Gauge(
        'Temperature', 'Temperature measured by the DHT22 Sensor')
    prom_humid = Gauge(
        'Humidity', 'Relative Humidity measured by the DHT22 Sensor')
    start_http_server(8000)
    while True:
        date, humidity, temperature = get_data()
        print(date, humidity, temperature)
        # logger_data.info(f'; {humidity}; {temperature}')
        prom_temp.set(temperature)
        prom_humid.set(humidity)

        time.sleep(sleep_duration)


class MyDaemon(Daemon):

    def run(self):
        main()

if __name__ == '__main__':
    daemon = MyDaemon('/tmp/daemon-telegram-bot.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: {} start|stop|restart".format(
            sys.argv[0]))  # % sys.argv[0]
        sys.exit(2)
