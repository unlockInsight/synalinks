# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

from synalinks.src import ops
from synalinks.src.api_export import synalinks_export
from synalinks.src.modules.core.decision import Decision
from synalinks.src.modules.module import Module
from synalinks.src.saving import serialization_lib


@synalinks_export(["synalinks.modules.Branch", "synalinks.Branch"])
class Branch(Module):
    """Use a `LanguageModel` to select which module to call based on an arbitrary
        input, a question and a list of labels.

    The selected branch output the data model computed using
    the inputs and module's branch, while the others output `None`.

    Example:

    ```python
    import synalinks
    import asyncio

    async def main():
        class Query(synalinks.DataModel):
            query: str

        class Answer(synalinks.DataModel):
            answer: str

        class AnswerWithCritique(synalinks.DataModel):
            thinking: str
            critique: str
            answer: str

        language_model = synalinks.LanguageModel("ollama_chat/deepseek-r1")

        x0 = synalinks.Input(data_model=Query)
        (x1, x2) = await synalinks.Branch(
            question="What is the difficulty level of the above query?",
            labels=["easy", "difficult"],
            branches=[
                synalinks.Generator(
                    data_model=Answer,
                    language_model=language_model,
                ),
                synalinks.Generator(
                    data_model=AnswerWithCritique,
                    language_model=language_model,
                ),
            ],
            language_model=language_model,
        )(x0)
        x3 = x1 | x2

        program = synalinks.Program(
            inputs=x0,
            outputs=x3,
            name="adaptative_chain_of_thought",
            description="Usefull to answer step by step only when needed",
        )

    if __name__ == "__main__":
        asyncio.run(main())
    ```

    Args:
        question (str): The question to ask.
        labels (list): The list of labels to choose from (strings).
        branches (list): The list of modules or programs to select from.
        inject_decision (bool): If True, inject the decision to the branch inputs.
            (default to True).
        return_decision (bool): If True, return the decision with the branch outputs.
            (default to True).
        language_model (LanguageModel): The language model to use.
        prompt_template (str): The default jinja2 prompt template
            to use (see `Generator`).
        decision_examples (list): The default examples to use in the prompt
            (see `Decision`).
        decision_hints (list): The default hints to use (see `Decision`).
        decision_use_inputs_schema (bool): Optional. Whether or not use the inputs
            schema in the decision prompt (Default to False) (see `Decision`).
        decision_use_outputs_schema (bool): Optional. Whether or not use the outputs
            schema in the decision prompt (Default to False) (see `Decision`).
        name (str): Optional. The name of the module.
        description (str): Optional. The description of the module.
        trainable (bool): Whether the module's variables should be trainable.
    """

    def __init__(
        self,
        question=None,
        labels=None,
        branches=None,
        inject_decision=True,
        return_decision=True,
        language_model=None,
        prompt_template=None,
        decision_examples=None,
        decision_hints=None,
        decision_use_inputs_schema=False,
        decision_use_outputs_schema=False,
        name=None,
        description=None,
        trainable=True,
    ):
        super().__init__(
            name=name,
            description=description,
            trainable=trainable,
        )
        if not branches:
            raise ValueError("The `branches` argument must be provided.")
        if not isinstance(branches, list):
            raise ValueError("The `branches` must be a list of `Module` or `Program`.")
        if len(labels) != len(branches):
            raise ValueError("The `labels` and `branches` must have the same length.")
        self.question = question
        self.labels = labels
        self.branches = {labels[i]: m for i, m in enumerate(branches)}
        self.inject_decision = inject_decision
        self.return_decision = return_decision
        self.prompt_template = prompt_template
        self.decision_examples = decision_examples
        self.decision_hints = decision_hints
        self.decision_use_inputs_schema = decision_use_inputs_schema
        self.decision_use_outputs_schema = decision_use_outputs_schema
        self.decision = Decision(
            question=question,
            labels=labels,
            language_model=language_model,
            prompt_template=prompt_template,
            examples=decision_examples,
            hints=decision_hints,
            use_inputs_schema=decision_use_inputs_schema,
            use_outputs_schema=decision_use_outputs_schema,
            name=self.name + "_decision",
        )

    async def call(self, inputs, training=False):
        if not inputs:
            return tuple([None] * len(self.branches))
        decision = await self.decision(
            inputs,
            training=training,
        )
        choice = decision.get("choice")
        outputs = []
        for label, module in self.branches.items():
            if label == choice:
                if module:
                    if self.inject_decision and self.return_decision:
                        outputs.append(
                            await ops.concat(
                                decision,
                                await module(
                                    await ops.concat(
                                        inputs,
                                        decision,
                                        name=self.name + "_inputs_with_decision",
                                    ),
                                    training=training,
                                ),
                                name=self.name + "_with_decision",
                            )
                        )
                    elif self.inject_decision and not self.return_decision:
                        outputs.append(
                            await module(
                                await ops.concat(
                                    inputs,
                                    decision,
                                    name=self.name + "_inputs_with_decision",
                                ),
                                training=training,
                            )
                        )
                    elif not self.inject_decision and self.return_decision:
                        outputs.append(
                            await ops.concat(
                                decision,
                                await module(
                                    inputs,
                                    training=training,
                                ),
                                name=self.name + "_with_decision",
                            )
                        )
                    else:
                        outputs.append(
                            await module(
                                inputs,
                                training=training,
                            )
                        )
                else:
                    outputs.append(None)
            else:
                outputs.append(None)
        return tuple(outputs)

    async def compute_output_spec(self, inputs, training=False):
        outputs = []
        decision = await self.decision(
            inputs,
            training=training,
        )
        for module in self.branches.values():
            if self.inject_decision and self.return_decision:
                outputs.append(
                    await ops.concat(
                        decision,
                        await module(
                            await ops.concat(
                                inputs,
                                decision,
                                name=self.name + "_inputs_with_decision",
                            ),
                            training=training,
                        ),
                        name=self.name + "_with_decision",
                    )
                )
            elif self.inject_decision and not self.return_decision:
                outputs.append(
                    await module(
                        await ops.concat(
                            inputs,
                            decision,
                            name=self.name + "_inputs_with_decision",
                        ),
                        training=training,
                    )
                )
            elif not self.inject_decision and self.return_decision:
                outputs.append(
                    await ops.concat(
                        decision,
                        await module(
                            inputs,
                            training=training,
                        ),
                        name=self.name + "_with_decision",
                    )
                )
            else:
                outputs.append(
                    await module(
                        inputs,
                        training=training,
                    )
                )
        return tuple(outputs)

    def get_config(self):
        config = {
            "question": self.question,
            "labels": self.labels,
            "inject_decision": self.inject_decision,
            "return_decision": self.return_decision,
            "prompt_template": self.prompt_template,
            "decision_examples": self.decision_examples,
            "decision_hints": self.decision_hints,
            "decision_use_inputs_schema": self.decision_use_inputs_schema,
            "decision_use_outputs_schema": self.decision_use_outputs_schema,
            "name": self.name,
            "description": self.description,
            "trainable": self.trainable,
        }
        language_model_config = {
            "language_model": serialization_lib.serialize_synalinks_object(
                self.language_model
            )
        }
        branches_config = {
            "branches": [
                serialization_lib.serialize_synalinks_object(branch)
                for branch in self.branches.values()
            ]
        }
        return {**config, **language_model_config, **branches_config}

    @classmethod
    def from_config(cls, config, custom_objects=None):
        language_model = serialization_lib.deserialize_synalinks_object(
            config.pop("language_model")
        )
        branches = [
            serialization_lib.deserialize_synalinks_object(
                branch_config, custom_objects=custom_objects
            )
            for branch_config in config.pop("branches")
        ]
        return cls(language_model=language_model, branches=branches, **config)
