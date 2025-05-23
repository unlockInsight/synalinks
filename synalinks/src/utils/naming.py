# Modified from: keras/src/utils/naming.py
# Original authors: François Chollet et al. (Keras Team)
# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

import collections
import re

from synalinks.src.api_export import synalinks_export
from synalinks.src.backend.common import global_state


def auto_name(prefix):
    prefix = to_snake_case(prefix)
    return uniquify(prefix)


def uniquify(name):
    object_name_uids = global_state.get_global_attribute(
        "object_name_uids",
        default=collections.defaultdict(int),
        set_to_default=True,
    )
    if name in object_name_uids:
        unique_name = f"{name}_{object_name_uids[name]}"
    else:
        unique_name = name
    object_name_uids[name] += 1
    return unique_name


def to_snake_case(name):
    name = re.sub(r"\W+", "", name)
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z])([A-Z])", r"\1_\2", name).lower()
    return name


def to_pkg_name(name):
    name = name.replace("-", "_")
    name = name.replace(" ", "_")
    name = to_snake_case(name)
    return name


@synalinks_export("synalinks.backend.get_uid")
def get_uid(prefix=""):
    """Associates a string prefix with an integer counter.

    Args:
        prefix: String prefix to index.

    Returns:
        Unique integer ID.

    Example:

    >>> get_uid('action')
    1
    >>> get_uid('action')
    2
    """
    object_name_uids = global_state.get_global_attribute(
        "object_name_uids",
        default=collections.defaultdict(int),
        set_to_default=True,
    )
    object_name_uids[prefix] += 1
    return object_name_uids[prefix]


def reset_uids():
    global_state.set_global_attribute("object_name_uids", collections.defaultdict(int))


def get_object_name(obj):
    if hasattr(obj, "name"):  # Most synalinks objects.
        return obj.name
    elif hasattr(obj, "__name__"):  # Function.
        return to_snake_case(obj.__name__)
    elif hasattr(obj, "__class__"):  # Class instance.
        return to_snake_case(obj.__class__.__name__)
    return to_snake_case(str(obj))
