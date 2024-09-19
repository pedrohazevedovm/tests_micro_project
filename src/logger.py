import os
import csv
from datetime import datetime


class Logger:
    def __init__(self):
        self.CSV_FIELDNAMES = ['datetime', 'device', 'cam', 'resolution']
        self.log_dict = {}

    def create_logger(self) -> None:
        current_dir = os.getcwd()
        log_local_path = os.path.join(current_dir, r"log_dir")
        if not os.path.exists(log_local_path):
            os.mkdir(log_local_path)
        if not os.path.isfile('log_dir/log.csv'):
            with open('log_dir/log.csv', 'w', newline='') as log:
                writer = csv.writer(log)
                writer.writerow(self.CSV_FIELDNAMES)

    def add_row(self, date_now: datetime, device: str, cam: str, resolution: str) -> None:
        if os.path.isfile('log_dir/log.csv'):
            self.log_dict['datetime'] = date_now
            self.log_dict['device'] = device
            self.log_dict['cam'] = cam
            self.log_dict['resolution'] = resolution
            with open('log_dir/log.csv', 'a', newline='') as log:
                writer = csv.DictWriter(log, fieldnames=self.CSV_FIELDNAMES)
                writer.writerow(self.log_dict)
        else:
            raise FileNotFoundError('logfile not found.')

    def clear_log(self) -> None:
        os.remove('log_dir/log.csv')
        with open('log_dir/log.csv', 'w') as log:
            writer = csv.writer(log)
            writer.writerow(self.CSV_FIELDNAMES)
