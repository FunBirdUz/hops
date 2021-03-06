# --- START: IMPORTS

# built-in
from typing import Callable, List
import inspect

# local
# django-specific
# other/external
# --- END: IMPORTS


def lock_method_for_strangers(
        checker: Callable[[int, List[int]], bool],
        default: Callable = None,
        white_list: List[int] = None
) -> Callable:
    """
    Used to lock a specific method in order to make the method inaccessible to specifici users
    :param checker: a callable object for doing the checking process
    :param default: default function to call when lock is necessary
    :param white_list: a list of tg user ids
    :return: function object
    """
    if not white_list:
        white_list = []

    def outer(method):
        # check if the method has proper arg
        arg = 'message'
        all_args = inspect.getfullargspec(method).args
        if arg in all_args:
            # method seems to be lockable, let's try to lock it
            def lockable(message, *args, **kwargs):
                # if chat is not in whitelist, we need to lock it
                if checker(message.from_user.id, white_list):
                    # method is not locked
                    return method(message, *args, **kwargs)
                # method is locked
                # now we'll try doing a default process
                return default(message, *args, **kwargs) if default else None
            return lockable
        else:
            # method is not lockable, we return the original version back without any changes
            return method
    return outer
