#!/usr/bin/env python3

import time
from functions import get_data
from functions import create_logger
from functions import connect_db

import sys

# setup db connection
con = connect_db()
cursor = con.cursor()

# set sleep duration for test purposes
sleep_duration = 60

# set up logging for debugging
logger = create_logger('read_sensor.log')


# function for writing results to database
def write_to_db(cursor, date, humidity, temperature):

    insert_sql = """INSERT INTO humidity_data
                    VALUES (%s, %s, %s);"""

    cursor.execute(insert_sql, (date, humidity, temperature))

    con.commit()


def cleanup_db():
    con.close()
    cursor.close()
    logger.info("Database connections closed.")


def main():
    logger.info(f'Reading data and writing to database every {sleep_duration} seconds.')

    while True:
        date, humidity, temperature = get_data()
        # print(date, humidity, temperature)
        write_to_db(cursor, date, humidity, temperature)

        time.sleep(sleep_duration)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        logger.info('Terminating...')
        cleanup_db()
