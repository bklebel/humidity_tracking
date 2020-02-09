# import psycopg2
import Adafruit_DHT
from datetime import datetime
import time
import numpy as np
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def connect_db():
    with open('db_credentials.txt') as file:
        params = file.read()

    connection = psycopg2.connect(params)

    return connection

# define function for printing results


def format_result(time, humidity, temperature):
    if humidity is not None and temperature is not None:
        # format time string
        time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')

        return 'Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity)
    else:
        return 'Failed to get reading.'


def filterOutliers(values, std_factor=2):
    mean = np.mean(values)
    standard_deviation = np.std(values)

    if standard_deviation == 0:
        return np.mean(values)

    final_values = np.zeros_like(values)
    final_values[:] = np.NaN
    final_values = values[
        np.where(values > mean - std_factor * standard_deviation)]
    final_values = final_values[
        np.where(final_values < mean + std_factor * standard_deviation)]

    return np.mean(final_values)


def get_data_raw(n=1):
    # sensor type and the pin to which the sensor is connected are hard coded
    # since they don't change
    for _ in range(n):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

        if humidity is not None and temperature is not None:
            yield (humidity, temperature)
        else:
            logger.info('We got no reading, but ``humidity = ' + str(humidity) +
                        ' & temp = ' + str(temperature) + '`` , trying again.')
            time.sleep(2)  # sleep for two seconds before re-trying
            yield [x for x in get_data_raw(n)]


def get_data():
    date = datetime.now()
    temperature = []
    humidity = []
    for hum, temp in get_data_raw(10):
        temperature.append(temp)
        humidity.append(hum)

    return date, filterOutliers(np.array(humidity)), filterOutliers(np.array(temperature))


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
