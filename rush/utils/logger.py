import sys
import logging


rush_logger = logging.getLogger('rush')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='{levelname}:{filename}:{funcName}:{asctime}:\n\t{message:s}', style='{'))
handler.setLevel(logging.INFO)
rush_logger.setLevel(logging.INFO)
rush_logger.addHandler(handler)
rush_logger.propagate = False
