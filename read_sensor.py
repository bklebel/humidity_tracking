#!/usr/bin/env python3

# import sys
# import Adafruit_DHT
# import logging
# from time import sleep
import time
from functions import get_data
from functions import create_logger

import numpy as np

from prometheus_client import start_http_server
from prometheus_client import Gauge

# setup db connection
# con = connect_db()
# cursor = con.cursor()

# set sleep duration for test purposes
sleep_duration = 60

# set up logging for debugging
logger_events = create_logger('read_sensor.log', 'events')
logger_data = create_logger(file='data.log', log='temps', form='%(asctime)s %(message)s')



# function for writing results to database
# def write_to_db(cursor, time, humidity, temperature):

#     insert_sql = """INSERT INTO humidity_data
#                     VALUES (%s, %s, %s);"""

#     cursor.execute(insert_sql, (time, humidity, temperature))

#     con.commit()


# def cleanup_db():
#     con.close()
#     cursor.close()
#     logger.info("Database connections closed.")


# def main():


if __name__ == '__main__':
    logger_events.info(f'Reading data and writing to database every {sleep_duration} seconds.')
    prom_temp = Gauge('Temperature', 'Temperature measured by the DHT22 Sensor')
    prom_humid = Gauge('Humidity', 'Relative Humidity measured by the DHT22 Sensor')
    start_http_server(8000)
    while True:
        date, humidity, temperature = get_data()
        print(date, humidity, temperature)
        # logger_data.info(f'; {humidity}; {temperature}')
        prom_temp.set(temperature)
        prom_humid.set(humidity)

        # write_to_db(cursor, time, humidity, temperature)

        time.sleep(sleep_duration)

    # try:
    #     main()
    # except KeyboardInterrupt:
    #     sys.exit(0)
    # finally:
    #     logger_events.info('Terminating...')
    #     # cleanup_db()
