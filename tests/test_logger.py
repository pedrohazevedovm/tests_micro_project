import pytest
from src.logger import Logger
import os
import shutil
import csv
from datetime import datetime

SAMPLE_LOG = {'date_now': datetime.now(),
              'device': 'moto g12',
              'cam': 'Cam 0',
              'resolution': '1920x1080'}


class TestLogger:

    def setup_class(self):
        self.logger = Logger()

    def setup_method(self, method):
        if method.__name__ != 'test_create_logger':
            self.logger.create_logger()

    def teardown_method(self, method):
        if method.__name__ != 'test_add_row_without_logfile':
            shutil.rmtree('log_dir')

    def test_create_logger(self):
        self.logger.create_logger()

        assert os.path.isfile('log_dir/log.csv') is True

        with open('log_dir/log.csv', 'r') as log:
            reader = csv.reader(log)
            header = next(reader)
            assert header == self.logger.CSV_FIELDNAMES

    def test_add_row(self):
        self.logger.add_row(SAMPLE_LOG['date_now'], SAMPLE_LOG['device'], SAMPLE_LOG['cam'], SAMPLE_LOG['resolution'])

        with open('log_dir/log.csv', 'r') as log:
            reader = csv.DictReader(log, fieldnames=self.logger.CSV_FIELDNAMES)
            next(reader)
            first_row = next(reader)
            assert first_row['datetime'] == SAMPLE_LOG['date_now'].strftime('%Y-%m-%d %H:%M:%S.%f')
            assert first_row['device'] == SAMPLE_LOG['device']
            assert first_row['cam'] == SAMPLE_LOG['cam']
            assert first_row['resolution'] == SAMPLE_LOG['resolution']

    def test_add_row_without_logfile(self):
        if os.path.exists("log_dir/log.csv"):
            shutil.rmtree('log_dir')
        with pytest.raises(FileNotFoundError):
            self.logger.add_row(SAMPLE_LOG['date_now'], SAMPLE_LOG['device'], SAMPLE_LOG['cam'],
                                SAMPLE_LOG['resolution'])


    def test_clear_log(self):
        self.logger.add_row(SAMPLE_LOG['date_now'], SAMPLE_LOG['device'], SAMPLE_LOG['cam'], SAMPLE_LOG['resolution'])

        self.logger.clear_log()

        with open('log_dir/log.csv', 'r') as log:
            reader = csv.reader(log)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0] == self.logger.CSV_FIELDNAMES
            assert rows[1] == []

