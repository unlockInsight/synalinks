"""DO NOT EDIT.

This file was autogenerated. Do not edit it by hand,
since your modifications would be overwritten.
"""

from synalinks.src.backend import DataModel
from synalinks.src.backend.common.global_state import clear_session
from synalinks.src.backend.common.json_data_model import is_json_data_model
from synalinks.src.backend.common.symbolic_data_model import is_symbolic_data_model
from synalinks.src.backend.config import api_key
from synalinks.src.backend.config import backend
from synalinks.src.backend.config import epsilon
from synalinks.src.backend.config import floatx
from synalinks.src.backend.config import set_api_key
from synalinks.src.backend.config import set_backend
from synalinks.src.backend.config import set_epsilon
from synalinks.src.backend.config import set_floatx
from synalinks.src.backend.pydantic.base import ChatMessage
from synalinks.src.backend.pydantic.base import ChatMessages
from synalinks.src.backend.pydantic.base import ChatRole
from synalinks.src.backend.pydantic.base import Document
from synalinks.src.backend.pydantic.base import Edge
from synalinks.src.backend.pydantic.base import Embedding
from synalinks.src.backend.pydantic.base import Embeddings
from synalinks.src.backend.pydantic.base import Entities
from synalinks.src.backend.pydantic.base import Entity
from synalinks.src.backend.pydantic.base import GenericInputs
from synalinks.src.backend.pydantic.base import GenericIO
from synalinks.src.backend.pydantic.base import GenericOutputs
from synalinks.src.backend.pydantic.base import Instructions
from synalinks.src.backend.pydantic.base import KnowledgeGraph
from synalinks.src.backend.pydantic.base import KnowledgeGraphs
from synalinks.src.backend.pydantic.base import Label
from synalinks.src.backend.pydantic.base import Prediction
from synalinks.src.backend.pydantic.base import Reward
from synalinks.src.backend.pydantic.base import Stamp
from synalinks.src.backend.pydantic.base import Unique
from synalinks.src.backend.pydantic.base import Weight
from synalinks.src.backend.pydantic.base import is_chat_message
from synalinks.src.backend.pydantic.base import is_chat_messages
from synalinks.src.backend.pydantic.base import is_document
from synalinks.src.backend.pydantic.base import is_edge
from synalinks.src.backend.pydantic.base import is_embedding
from synalinks.src.backend.pydantic.base import is_embeddings
from synalinks.src.backend.pydantic.base import is_entities
from synalinks.src.backend.pydantic.base import is_entity
from synalinks.src.backend.pydantic.base import is_instructions
from synalinks.src.backend.pydantic.base import is_knowledge_graph
from synalinks.src.backend.pydantic.base import is_knowledge_graphs
from synalinks.src.backend.pydantic.base import is_prediction
from synalinks.src.backend.pydantic.core import is_meta_class
from synalinks.src.utils.naming import get_uid
