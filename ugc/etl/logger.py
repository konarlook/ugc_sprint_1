"""
Модуль для логирования.
"""
import logging
import sys
from typing import List, Any

class UGCLogger:
    """
    Класс logger.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        file_handler: logging.FileHandler = logging.FileHandler(
            filename="./logs.log"
        )
        stdout_handler: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
        handlers: List[Any[logging.FileHandler, logging.StreamHandler]] = [
            file_handler,
            stdout_handler,
        ]
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
            handlers=handlers,
        )