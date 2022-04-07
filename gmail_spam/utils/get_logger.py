"""
Log messages with levels of DEBUG and higher to file, and those 
messages at level INFO and higher to the console. 
Logs to file should contain timestamps, but the console messages should not
"""
import logging
import os
import time

def get_logger(log_dir, logger_name, file_level=logging.DEBUG, console_level=logging.INFO):
    ts_str = time.strftime("%m%d%Y_%H%M%s", time.localtime()) + '.log'
    fname = os.path.join(log_dir, ts_str) # the filename
    lgr = logging.getLogger(logger_name)

    # set up logging to file - see previous section for more details
    logging.basicConfig(
        level=file_level,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename=fname,# "/temp/myapp.log",
        filemode="w",
    )
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(console_level)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    lgr.addHandler(console)

    return lgr
