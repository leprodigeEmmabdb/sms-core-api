# from settings.base import ERROR_LOGGER
import logging
import sys
import traceback

logger = logging.getLogger(__name__)


def handle_exceptions():
    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)

    log = "Exception type : %s" % ex_type.__name__
    log2 = "Exception message : %s" % ex_value
    # Format stacktrace
    stack_trace = list()

    log3 = ""
    for trace in trace_back:
        errorContent = "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3])
        stack_trace.append(errorContent)
        log_ = f"Stack trace: {errorContent}"
        logger.error(log_)

    logger.error(log)
    logger.error(log2)
    logger.error(("=" * 25) + "\n")
