# DO NOT EDIT. Generated by api_gen.sh
from synalinks.api import Action
from synalinks.api import And
from synalinks.api import Branch
from synalinks.api import ChainOfThought
from synalinks.api import Concat
from synalinks.api import DataModel
from synalinks.api import Decision
from synalinks.api import EmbeddingModel
from synalinks.api import Function
from synalinks.api import Generator
from synalinks.api import Initializer
from synalinks.api import Input
from synalinks.api import JsonDataModel
from synalinks.api import LanguageModel
from synalinks.api import Metric
from synalinks.api import Module
from synalinks.api import Operation
from synalinks.api import Or
from synalinks.api import Program
from synalinks.api import Reward
from synalinks.api import Sequential
from synalinks.api import StatelessScope
from synalinks.api import SymbolicDataModel
from synalinks.api import SymbolicScope
from synalinks.api import __version__
from synalinks.api import backend
from synalinks.api import callbacks
from synalinks.api import chat_prompt_template
from synalinks.api import config
from synalinks.api import datasets
from synalinks.api import default_prompt_template
from synalinks.api import embedding_models
from synalinks.api import initializers
from synalinks.api import language_models
from synalinks.api import metrics
from synalinks.api import modules
from synalinks.api import name_scope
from synalinks.api import ops
from synalinks.api import optimizers
from synalinks.api import programs
from synalinks.api import rewards
from synalinks.api import saving
from synalinks.api import tree
from synalinks.api import utils
from synalinks.api import version

# END DO NOT EDIT.

import os  # isort: skip

# Add everything in /api/ to the module search path.
__path__.append(os.path.join(os.path.dirname(__file__), "api"))  # noqa: F405

# Don't pollute namespace.
del os


# Never autocomplete `.src` or `.api` on an imported synalinks object.
def __dir__():
    keys = dict.fromkeys((globals().keys()))
    keys.pop("src")
    keys.pop("api")
    return list(keys)


# Don't import `.src` or `.api` during `from synalinks import *`.
__all__ = [
    name
    for name in globals().keys()
    if not (name.startswith("_") or name in ("src", "api"))
]

if backend.backend() == "pydantic":
    from synalinks.src.backend import Field
