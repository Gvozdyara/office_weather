import logging

from kivy.logger import Logger
from mainapp import MainApp


def main():
    formatter = '[%(levelname)s] [%(funcName)s] [%(asctime)s] %(message)s'
    logging.basicConfig(filename='log.log',
                        encoding='utf-8', 
                        level=logging.DEBUG,
                        format=formatter)
    Logger.handlers[0].setFormatter(
        logging.Formatter(formatter))
    Logger.handlers[1].setFormatter(
        logging.Formatter(formatter))
    Logger.handlers[2].setFormatter(
        logging.Formatter(formatter))
    app = MainApp()
    app.run()


if __name__ == '__main__':
    main()