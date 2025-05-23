# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

import json
import warnings

import litellm

from synalinks.src.api_export import synalinks_export
from synalinks.src.backend import ChatRole
from synalinks.src.saving.synalinks_saveable import SynalinksSaveable


@synalinks_export(["synalinks.LanguageModel", "synalinks.language_models.LanguageModel"])
class LanguageModel(SynalinksSaveable):
    """A language model API wrapper.

    A language model is a type of AI model designed to generate, and interpret human
    language. It is trained on large amounts of text data to learn patterns and
    structures in language. Language models can perform various tasks such as text
    generation, translation, summarization, and answering questions.

    We support providers that implement *constrained structured output*
    like OpenAI, Ollama or Mistral. In addition we support providers that otherwise
    allow to constrain the use of a specific tool like Groq or Anthropic.

    For the complete list of models, please refer to the providers documentation.

    **Using OpenAI models**

    ```python
    import synalinks
    import os

    os.environ["OPENAI_API_KEY"] = "your-api-key"

    language_model = synalinks.LanguageModel(
        model="openai/gpt-4o-mini",
    )
    ```

    **Using Groq models**

    ```python
    import synalinks
    import os

    os.environ["GROQ_API_KEY"] = "your-api-key"

    language_model = synalinks.LanguageModel(
        model="groq/llama3-8b-8192",
    )
    ```

    **Using Anthropic models**

    ```python
    import synalinks
    import os

    os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

    language_model = synalinks.LanguageModel(
        model="anthropic/claude-3-sonnet-20240229",
    )
    ```

    **Using Mistral models**

    ```python
    import synalinks
    import os

    os.environ["MISTRAL_API_KEY"] = "your-api-key"

    language_model = synalinks.LanguageModel(
        model="mistral/codestral-latest",
    )
    ```

    **Using Ollama models**

    ```python
    import synalinks
    import os

    language_model = synalinks.LanguageModel(
        model="ollama/deepseek-r1",
    )
    ```

    Args:
        model (str): The model to use.
        api_base (str): Optional. The endpoint to use.
        retry (int): Optional. The number of retry.
    """

    def __init__(
        self,
        model=None,
        api_base=None,
        retry=5,
    ):
        if model is None:
            raise ValueError("You need to set the `model` argument for any LanguageModel")
        model_provider = model.split("/")[0]
        if model_provider == "ollama":
            # Switch from `ollama` to `ollama_chat`
            # because it have better performance due to the chat prompts
            model = model.replace("ollama", "ollama_chat")
        self.model = model
        if self.model.startswith("ollama") and not api_base:
            self.api_base = "http://localhost:11434"
        else:
            self.api_base = api_base
        self.retry = retry

    async def __call__(self, messages, schema=None, streaming=False, **kwargs):
        """
        Call method to generate a response using the language model.

        Args:
            messages (dict): A formatted dict of chat messages.
            schema (dict): The target JSON schema for structed output (optional).
                If None, output a ChatMessage-like answer.
            streaming (bool): Enable streaming (optional). Default to False.
                Can be enabled only if schema is None.
            **kwargs (keyword arguments): The additional keywords arguments
                forwarded to the LLM call.

        Returns:
            (dict): The generated structured response.
        """
        formatted_messages = messages.get_json().get("messages", [])
        json_instance = {}
        if schema:
            if self.model.startswith("groq"):
                # Use a tool created on the fly for groq
                kwargs.update(
                    {
                        "tools": [
                            {
                                "function": {
                                    "name": "structured_output",
                                    "description": "Generate a valid JSON output",
                                    "parameters": schema.get("properties"),
                                },
                                "type": "function",
                            }
                        ],
                        "tool_choice": {
                            "type": "function",
                            "function": {"name": "structured_output"},
                        },
                    }
                )
            elif self.model.startswith("anthropic"):
                # Use a tool created on the fly for anthropic
                kwargs.update(
                    {
                        "tools": [
                            {
                                "name": "structured_output",
                                "description": "Generate a valid JSON output",
                                "input_schema": {
                                    "type": "object",
                                    "properties": schema.get("properties"),
                                    "required": schema.get("required"),
                                },
                            }
                        ],
                        "tool_choice": {
                            "type": "tool",
                            "name": "structured_output",
                        },
                    }
                )
            elif self.model.startswith("ollama") or self.model.startswith("mistral"):
                # Use constrained structured output for ollama/mistral
                kwargs.update(
                    {
                        "response_format": {
                            "type": "json_schema",
                            "json_schema": {"schema": schema},
                            "strict": True,
                        },
                    }
                )
            elif self.model.startswith("openai"):
                # Use constrained structured output for openai
                # OpenAI require the field  "additionalProperties"
                kwargs.update(
                    {
                        "response_format": {
                            "type": "json_schema",
                            "json_schema": {
                                "name": "structured_output",
                                "strict": True,
                                "schema": schema,
                            },
                        }
                    }
                )
            else:
                provider = self.model.split("/")[0]
                raise ValueError(
                    f"LM provider '{provider}' not supported yet, please ensure that"
                    " they support constrained structured output and fill an issue."
                )

        if self.api_base:
            kwargs.update(
                {
                    "api_base": self.api_base,
                }
            )
        if streaming and schema:
            streaming = False
        if streaming:
            kwargs.update({"stream": True})
        for i in range(self.retry):
            try:
                response_str = ""
                response = litellm.completion(
                    model=self.model,
                    messages=formatted_messages,
                    caching=False,
                    **kwargs,
                )
                if streaming:
                    return StreamingIterator(response)
                if (
                    self.model.startswith("groq") or self.model.startswith("anthropic")
                ) and schema:
                    response_str = response["choices"][0]["message"]["tool_calls"][0][
                        "function"
                    ]["arguments"]
                else:
                    response_str = response["choices"][0]["message"]["content"].strip()
                if schema:
                    json_instance = json.loads(response_str)
                else:
                    json_instance = {"role": ChatRole.ASSISTANT, "content": response_str}
                return json_instance
            except Exception as e:
                warnings.warn(str(e))
        return None

    def _obj_type(self):
        return "LanguageModel"

    def get_config(self):
        return {
            "model": self.model,
            "api_base": self.api_base,
            "retry": self.retry,
        }

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def __repr__(self):
        api_base = f" api_base={self.api_base}" if self.api_base else ""
        return f"<LanguageModel model={self.model}{api_base}>"


class StreamingIterator:
    def __init__(self, iterator):
        self._iterator = iterator

    def __iter__(self):
        return self

    def __next__(self):
        content = self._iterator.__next__()["choices"][0]["delta"]["content"]
        if content:
            return {"role": ChatRole.ASSISTANT, "content": content}
        else:
            raise StopIteration
