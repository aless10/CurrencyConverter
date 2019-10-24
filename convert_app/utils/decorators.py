import logging
import time
from functools import wraps

log = logging.getLogger(__name__)


def retry(exceptions, tries=4, delay=3, backoff=2):
    """Retry calling the decorated function using an exponential backoff.
    :param exceptions: the exception to check. may be a tuple of
        exceptions to check
    :type exceptions: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """

    def wrapper(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            if mtries <= 0:
                raise ValueError("Invalid number of tries {}".format(tries))
            # Initializing a base exception to be overwritten during while loop. This in order to avoid warning on
            # variable referenced before assignment
            exception_to_raise = BaseException("This exception should not be raised.")
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    mtries -= 1
                    log.exception("Exception occurred while executing '%s'", f.__name__)
                    log.warning("Retrying in %s seconds, %d of %d tries left", mdelay, mtries, tries)
                    time.sleep(mdelay)
                    mdelay *= backoff
                    # updating the exception. The last one will be raised when no more tries are left
                    exception_to_raise = e

            raise exception_to_raise

        return f_retry

    return wrapper
