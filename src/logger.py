import sys


class Logger:

    def info(self, message):
        print(message)
        sys.stdout.flush()
