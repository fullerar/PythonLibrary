import sys

class Log:
    ENABLE_COLOR = True
    LOG_FILE = None

    COLORS = {
        "STEP": "\033[94m",
        "INFO": "\033[92m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }

    @classmethod
    def set_log_file(cls, filepath):
        cls.LOG_FILE = open(filepath, 'w')
        cls.ENABLE_COLOR = False

    @classmethod
    def close(cls):
        if cls.LOG_FILE:
            cls.LOG_FILE.close()

    @classmethod
    def print(cls, level, message):
        prefix = f"[{level}]"
        colored_prefix = f"{cls.COLORS.get(level, '')}{prefix}{cls.COLORS['RESET']}" if cls.ENABLE_COLOR else prefix
        output = f"{colored_prefix} {message}" if cls.ENABLE_COLOR else f"{prefix} {message}"
        if cls.LOG_FILE:
            cls.LOG_FILE.write(f"{prefix} {message}\n")
        else:
            print(output)