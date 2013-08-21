import time
import os

class __ltclogger(object):
    default_level = 3
    def __init__(self):
        self.level = self.default_level

        try:
            os.mkdir("logs")
        except OSError:
            pass

        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        basename = "logs/logltc_" + timestamp
        filename = basename

        for i in range(1, 1000):
            try:
                fd = os.open(filename + ".txt", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0666)
                self.log = os.fdopen(fd, "w")
            except IOError:
                filename = basename + "_" + str(i)
            else:
                break

    def __del__(self):
        self.log.close()

    def _set_default_level(self, level):
        self.level = level

    def _log(self, text, level):
        if level >= self.level:
            timestamp = time.strftime("%Y-%m-%d %X", time.localtime())
            self.log.write(str(level) + "|" + timestamp + "| " + text + "\n")

__globallogger = __ltclogger()

def set_default_level(level):
    __globallogger._set_default_level(level)

def log(text, level=__globallogger.default_level):
    __globallogger._log(text, level)


if __name__ == "__main__":
    log("TEST")
    log("TEST LEVEL 5", 5)
    log("TEST LEVEL 4", 4)
    log("TEST LEVEL 3", 3)
    log("TEST LEVEL 2", 2)
    log("TEST LEVEL 1", 1)
    log("Change default level to 1")
    set_default_level(1)
    log("TEST LEVEL 5", 5)
    log("TEST LEVEL 4", 4)
    log("TEST LEVEL 3", 3)
    log("TEST LEVEL 2", 2)
    log("TEST LEVEL 1", 1)
    log("Invalid level", "Dog")


