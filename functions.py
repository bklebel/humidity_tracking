# import psycopg2
import Adafruit_DHT
from datetime import datetime
import time

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# def connect_db():
#     with open('db_credentials.txt') as file:
#         params = file.read()

#     connection = psycopg2.connect(params)

#     return connection

# define function for printing results
def format_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        return 'Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity)
    else:
        return 'Failed to get reading.'


def get_data():
    # sensor type and the pin to which the sensor is connected are hard coded
    # since they don't change
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    date = datetime.now()

    if humidity is not None and temperature is not None:
        return (date, humidity, temperature)
    else:
        logger.info('We got no reading, but ``humidity = ' + str(humidity) +
                    ' & temp = ' + str(temperature) + '`` , trying again.')
        time.sleep(2)  # sleep for two seconds before re-trying
        return get_data()


def create_logger(file, log=None, form='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    # set up logging for debugging
    if log is None:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(log)
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler(file)

    # create formatter and add it to the handler
    formatter = logging.Formatter(form)
    fh.setFormatter(formatter)

    # add handler
    logger.addHandler(fh)

    return logger
