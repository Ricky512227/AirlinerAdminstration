import os,sys
import datetime
import logging


class LogMonitor:
    log_time_format = "%Y-%m-%d %H:%M:%S"
    log_file_format = '%(asctime)s - %(levelname)s - [%(filename)s : %(lineno)d] :: %(message)s'
    log_level = logging.DEBUG
    log_file_mode = 'w'
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    service_name=None

    def __init__(self, service_name):
        self.service_name = service_name
        self.log_file_name = datetime.datetime.now().strftime("%Y%m%d_%H") + ".log"

    def create_logger_for_service(self):
        try:
            print("Initializing logger for the service [{0}] :: [STARTED]".format(self.service_name))
            service_dir = os.path.join(self.project_dir, 'logs', self.service_name)
            if not os.path.exists(service_dir):
                os.makedirs(service_dir)
            log_file_path = os.path.join(service_dir, self.log_file_name)
            logger = logging.getLogger(self.service_name)
            formatter = logging.Formatter(self.log_file_format, datefmt=self.log_time_format)
            file_handler = logging.FileHandler(log_file_path, mode=self.log_file_mode)
            file_handler.setFormatter(formatter)

            logger.setLevel(self.log_level)
            logger.addHandler(file_handler)

            print("Initialized logger for the service [{0}] :: [SUCCESS]".format(self.service_name))
            return logger
        except Exception as ex:
            print("Initialized logger for the service [{0}] :: [FAILED]".format(self.service_name))
            print(f'Error occurred :: {ex} \tLine No: {sys.exc_info()[2].tb_lineno}')
            return logging.getLogger(__name__)


