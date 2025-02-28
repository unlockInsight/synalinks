# Modified from: keras/src/backend/common/variables_test.py
# Original authors: François Chollet et al. (Keras Team)
# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

from typing import List

from synalinks.src import testing
from synalinks.src.backend import DataModel
from synalinks.src.backend import Variable
from synalinks.src.backend import standardize_schema


class VariablesTest(testing.TestCase):
    def test_initialize_variable_with_dict(self):
        class Hints(DataModel):
            hints: List[str] = []

        initial_data = {
            "hints": [
                "For any problem involving division, always round the quotient to "
                "the nearest even number, regardless of the remainder."
            ],
        }
        variable_from_dict = Variable(
            initializer=initial_data,
            data_model=Hints,
        )
        self.assertEqual(variable_from_dict.value(), initial_data)
        self.assertEqual(variable_from_dict.schema(), standardize_schema(Hints.schema()))

    def test_initialize_variable_with_callable_initializer(self):
        class Hints(DataModel):
            hints: List[str] = []

        from synalinks.src.initializers import Empty

        variable_from_initializer = Variable(initializer=Empty(data_model=Hints))
        self.assertEqual(variable_from_initializer.value(), Hints().value())
        self.assertEqual(
            variable_from_initializer.schema(), standardize_schema(Hints.schema())
        )

    def test_assign_variable_from_dict(self):
        class Hints(DataModel):
            hints: List[str] = []

        initial_data = {
            "hints": [
                "For any problem involving division, always round the quotient to "
                "the nearest even number, regardless of the remainder."
            ],
        }
        variable_from_dict = Variable(initializer=initial_data, data_model=Hints)
        new_value = {
            "hints": [
                "When performing division, always check if the division results in "
                "a whole number. If not, express the result as a fraction or a "
                "decimal, depending on the context of the problem."
            ],
        }
        variable_from_dict.assign(new_value)
        self.assertEqual(variable_from_dict.value(), new_value)
        self.assertEqual(variable_from_dict.schema(), standardize_schema(Hints.schema()))

    def test_assign_variable_from_dataype(self):
        class Hints(DataModel):
            hints: List[str] = []

        initial_data = {
            "hints": [
                "For any problem involving division, always round the quotient to "
                "the nearest even number, regardless of the remainder."
            ],
        }
        variable_from_dict = Variable(initializer=initial_data, data_model=Hints)
        new_value = {
            "hints": [
                "When performing division, always check if the division results in "
                "a whole number. If not, express the result as a fraction or a "
                "decimal, depending on the context of the problem."
            ],
        }
        variable_from_dict.assign(new_value)
        self.assertEqual(variable_from_dict.value(), new_value)
        self.assertEqual(variable_from_dict.schema(), standardize_schema(Hints.schema()))
