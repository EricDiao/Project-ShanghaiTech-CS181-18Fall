#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import time
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
        print("Get data: ", end='')
        print(data)
        time.sleep(interval)


if __name__ == "__main__":
    border = [(31.13, 102.28), (29.51, 102.28),
              (31.13, 106.22), (29.51, 106.22), ]
    data_queue = Queue()
    data_consumer = Process(target=data_consumer, args=(data_queue, 10,))
    data_provider = Process(
        target=crawlFR24MultiprocessingWrapper, args=(border, data_queue, 15,))
    data_provider.start()
    data_consumer.start()
