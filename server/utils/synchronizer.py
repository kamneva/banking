import requests

from datetime import datetime, time
from threading import Thread
from time import sleep

from utils.config import app_config
from utils.datetime_format import time_format

class Synchronizer:
    server_url = "http://127.0.0.1:5000"

    def __init__(self) -> None:
        self.keep_syncing = False
        self.force_update_time = False
        self.thread = Thread(target = self.sync)

    def current_time() -> time:
        return datetime.now().replace(second=0, microsecond=0).time()

    def next_update_time() -> time:
        time_list = [datetime.strptime(time, time_format).time() for time in app_config.time()]
        current_time = Synchronizer.current_time()

        for time in time_list:
            if time > current_time:
                return time

        return time_list[0]

    def sync(self) -> None:
        global app_config

        update_time = Synchronizer.next_update_time()
        while self.keep_syncing:
            current_time = Synchronizer.current_time()
            if update_time == current_time:
                requests.post(f"{Synchronizer.server_url}/update")
                update_time = Synchronizer.next_update_time()

            if self.force_update_time:
                update_time = Synchronizer.next_update_time()
                self.force_update_time = False

            sleep(1)

    def start(self) -> None:
        self.keep_syncing = True
        self.thread.start()

    def stop(self) -> None:
        if not self.thread.is_alive():
            return

        self.keep_syncing = False
        self.thread.join()

    def update(self) -> None:
        self.force_update_time = True