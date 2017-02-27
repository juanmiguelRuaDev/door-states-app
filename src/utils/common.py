import logging

logging.basicConfig(format='%(levelname)s ::%(asctime)-15s %(filename)s  %(message)s')
handler = logging.FileHandler('raspbarrier.log')
handler.setLevel(logging.INFO)


def app_logger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s ::%(asctime)-15s %(filename)s  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def os_platform_system():
    import platform
    return str(platform.system()).lower()


def add_secs(tm, seconds):
    import datetime
    full_date = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    full_date = full_date + datetime.timedelta(seconds=seconds)
    return full_date.time()


def convert_to_card_list(list_as_string):
    list_as_string = list_as_string.strip('[]')
    card_list = list_as_string.split(',')
    response = [card.strip() for card in card_list]
    return response


class Config:

    __local_instance = None

    def __init__(self, base_dir):
        import os
        import configparser
        absolute_path = base_dir + os.path.sep + "resources" + os.path.sep + "config.ini"
        config = configparser.ConfigParser()
        config.read(absolute_path)
        self.config = config

    @classmethod
    def instance(cls, base_dir=None):
        if cls.__local_instance is not None:
            return cls.__local_instance.config
        if base_dir is not None:
            cls.__local_instance = Config(base_dir)
            return cls.__local_instance.config
        return None


class Constants:
    DATE_FORMAT = '%Y%m%d%H%M%S'
    # from datetime import datetime
    # datetime.strptime(date_value_str, Constants.DATE_FORMAT)
