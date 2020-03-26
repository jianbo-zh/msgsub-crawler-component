import logging
import logging.handlers as handlers

logger = logging.getLogger("crawler")
logger.setLevel(logging.DEBUG) # 最低日志级别

_formatter = logging.Formatter(fmt="%(asctime)s %(filename)s line:%(lineno)d %(levelname)s - %(message)s", datefmt="%Y%m%d%I%M%S[%p]")

_consoleHandler = logging.StreamHandler()
_consoleHandler.setLevel(logging.DEBUG)
_consoleHandler.setFormatter(_formatter)

_fileHandler = handlers.RotatingFileHandler("crawler.log", maxBytes=1048576, backupCount=5)
_fileHandler.setLevel(logging.WARNING)
_fileHandler.setFormatter(_formatter)

logger.addHandler(_consoleHandler)
logger.addHandler(_fileHandler)