#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import time, logging
from multiprocessing import Process, Queue
from data_sources.flightradar24Crawler import crawlFR24, crawlFR24MultiprocessingWrapper


def data_consumer(queue, interval):
    """
    `data_consumer(queue, interval)`

    This is an EXAMPLE of the multiprocessing data consumer.
    You may write your own one and replace `data_consumer` in the following "main function".
    """
    while True:
        data = queue.get()
        logging.info("Data consumer: get data with timestamp {}.")
        print("get data: ", end='')
        print(data)
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(filename='atc.log',
                        format='%(levelname)s:%(asctime)s - %(message)s', level=logging.INFO)
    border = [(31.13, 102.28), (29.51, 102.28),
              (31.13, 106.22), (29.51, 106.22), ]  # This shall be passed in by sys.argv.
    logging.info("Artifical Idiot ATC started.")
    data_queue = Queue()
    logging.info("Mutiprocessing: data queue initialized.")
    data_consumer = Process(target=data_consumer, args=(data_queue, 10,))
    logging.info("Mutiprocessing: data consumer initialized.")
    data_provider = Process(
        target=crawlFR24MultiprocessingWrapper, args=(border, data_queue, 15,))
    logging.info("Mutiprocessing: data provider initialized.")
    data_provider.start()
    logging.info("Mutiprocessing: data provider started.")
    data_consumer.start()
    logging.info("Mutiprocessing: data consumer started.")
    logging.info("ATC initialized.")
