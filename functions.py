# import psycopg2
import board
import adafruit_dht
from datetime import datetime
from time import sleep
import numpy as np

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NoneException(Exception):
    pass


class customEx(Exception):
    pass


# def connect_db():
#     with open('db_credentials.txt') as file:
#         params = file.read()

#     connection = psycopg2.connect(params)

#     return connection

# define function for printing results


def format_result(time, humidity, temperature):
    """format results nicely"""
    if None in (humidity, temperature):
        return 'Failed to get reading.'

    # format time string
    time_pretty = time.strftime('%Y-%m-%d %H:%M:%S')
    return 'Time={0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(time_pretty, temperature, humidity)


def filterOutliers(values, std_factor=2):
    """discard outliers of distribution of measured values"""
    mean = np.mean(values)
    standard_deviation = np.std(values)

    if standard_deviation == 0:
        return mean

    final_values = np.zeros_like(values)
    final_values[:] = np.NaN  # fill array with NaN values
    # take only those values, which are within a central part of the
    # distribution of values
    final_values = values[
        np.where(values > mean - std_factor * standard_deviation)]
    final_values = final_values[
        np.where(final_values < mean + std_factor * standard_deviation)]

    # return one value: mean
    mean = np.nanmean(final_values)
    if np.isnan(mean) or mean is None:
        raise customEx
    return mean


def read_sensor():
    try:
        dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if None in (humidity, temperature):
            raise NoneException

        return (datetime.now(), humidity, temperature)
    except RuntimeError as e:
        logger.debug(e)
        logger.debug('We got no reading, trying again.')
        sleep(0.01)
        return read_sensor()
    except NoneException:
        logger.info('We got no reading, but ``humidity = ' + str(humidity) +
                    ' & temp = ' + str(temperature) + '`` , trying again.')
        sleep(0.5)
        return read_sensor()


def get_data_raw(n=1):
    """read raw sensor data for humidity and temperature
    sensor type and the pin to which the sensor is connected are hard coded
    since they don't change

    This is a generator! - it is best used in the definition of a for-loop, as in 'get_data()'
    if one wants all the output of this function in a list, the easiest way would be:
        list(get_data_raw(n))
    This however, somehow defeats the purpose...."""
    for _ in range(n):
        # sleep(0.5)
        d, humidity, temperature = read_sensor()
        yield (humidity, temperature)


def get_data():
    """read data from the DHT22/AM2302

    this includes filtering outliers
    returns (datetime object, humidity:float, temperature:float)"""
    date = datetime.now()
    temperature = []
    humidity = []
    for hum, temp in get_data_raw(10):
        temperature.append(temp)
        humidity.append(hum)

    return date, filterOutliers(np.array(humidity)), filterOutliers(np.array(temperature))


def create_logger(file):
    # set up logging for debugging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler(file)

    # create formatter and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler
    logger.addHandler(fh)

    return logger
