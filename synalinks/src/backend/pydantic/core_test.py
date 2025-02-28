# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

from synalinks.src import testing
from synalinks.src.backend.common.json_schema_utils import standardize_schema
from synalinks.src.backend.pydantic.core import DataModel
from synalinks.src.backend.pydantic.core import is_meta_class


class CoreTest(testing.TestCase):
    def test_non_instanciated_data_model_schema(self):
        class TestDataModel(DataModel):
            foo: str

        expected_schema = {
            "properties": {"foo": {"title": "Foo", "type": "string"}},
            "required": ["foo"],
            "title": "TestDataModel",
            "type": "object",
        }

        self.assertEqual(TestDataModel.schema(), expected_schema)

    def test_instanciated_data_model_schema(self):
        class TestDataModel(DataModel):
            foo: str

        expected_schema = {
            "properties": {"foo": {"title": "Foo", "type": "string"}},
            "required": ["foo"],
            "title": "TestDataModel",
            "type": "object",
        }

        self.assertEqual(TestDataModel(foo="bar").schema(), expected_schema)

    def test_instanciated_data_model_json(self):
        class TestDataModel(DataModel):
            foo: str

        expected_json = {"foo": "bar"}

        self.assertEqual(TestDataModel(foo="bar").json(), expected_json)

    async def test_concatenate_meta_data_model(self):
        class Foo(DataModel):
            foo: str

        class Bar(DataModel):
            bar: str

        class Result(DataModel):
            foo: str
            bar: str

        x = await (Foo + Bar)

        schema = x.schema()
        expected_schema = standardize_schema(Result.schema())
        self.assertEqual(schema, expected_schema)

    def test_is_meta_class(self):
        class Query(DataModel):
            query: str

        self.assertTrue(is_meta_class(Query))

    def test_is_not_meta_class(self):
        class Query(DataModel):
            query: str

        self.assertFalse(is_meta_class(Query(query="What is the French capital?")))
