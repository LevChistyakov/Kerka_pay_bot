import logging
import os


class SimpleLogging:
    path_to_logs = "log_files"
    logs_format = "%(asctime)s - %(processName)-10s - %(name)-10s - %(levelname)-8s - %(message)s"

    @classmethod
    def get_handlers(cls) -> list[logging.StreamHandler]:
        return [
            cls._get_console_logs_handler(),
            cls._get_main_logs_file_handler(),
            cls._get_errors_logs_file_handler()
        ]

    @classmethod
    def _get_errors_logs_file_handler(cls) -> logging.FileHandler:
        errors_file = logging.FileHandler(filename=os.path.join(cls.path_to_logs, "errors.log"), mode="w")
        errors_file.setLevel(level=logging.WARNING)

        return errors_file

    @classmethod
    def _get_main_logs_file_handler(cls) -> logging.FileHandler:
        main_file = logging.FileHandler(filename=os.path.join(cls.path_to_logs, "default.log"), mode="w")
        main_file.setLevel(level=logging.INFO)

        return main_file

    @classmethod
    def _get_console_logs_handler(cls) -> logging.StreamHandler:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)

        return console
