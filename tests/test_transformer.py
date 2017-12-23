import unittest
from transformer import Transformer


class TransformerTestClass(unittest.TestCase):
    def test_one_var_level_1_to_level_1(self):
        expected_result = {"a_ney_key": "Value A"}
        source = {"a_key": "Value A"}
        target_schema = {
            "root": {
                "a_ney_key": "a_key"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_two_vars_level_1_to_level_1_same_value(self):
        expected_result = {
            "a_ney_key": "Value A",
            "b_ney_key": "Value A"
        }
        source = {
            "a_key": "Value A",
            "b_key": "Value "
        }
        target_schema = {
            "root": {
                "a_ney_key": "a_key",
                "b_ney_key": "a_key"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_two_vars_level_1_to_level_1(self):
        expected_result = {
            "a_ney_key": "Value A",
            "b_ney_key": "Value B"
        }
        source = {
            "a_key": "Value A",
            "b_key": "Value B"
        }
        target_schema = {
            "root": {
                "a_ney_key": "a_key",
                "b_ney_key": "b_key"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_one_var_level_2_to_level_1(self):
        expected_result = {"a_ney_key": "Value A"}
        source = {
            "root": {
                "a_key": "Value A"
            }
        }
        target_schema = {
            "root": {
                "a_ney_key": "root>a_key"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_two_vars_levels_1_and_2_to_level_1(self):
        expected_result = {
            "a_ney_key": "Value A",
            "b_new_key": {
                "a_key": "Value A"
            }
        }
        source = {
            "root": {
                "a_key": "Value A"
            }
        }
        target_schema = {
            "root": {
                "a_ney_key": "root>a_key",
                "b_new_key": "root"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_level_1_to_level_2(self):
        expected_result = {
            "level_1": {
                "a_new_key": "Value A"
            }
        }

        source = {"a_key": "Value A"}

        target_schema = {
            "root": {
                "level_1": {
                    "a_new_key": "a_key"
                }
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_level_1_to_level_2_and_level_2_to_level_1(self):
        expected_result = {
            "a_new_key": "Value B",
            "level_1": {
                "b_new_key": "Value A"
            }
        }
        source = {
            "a_key": "Value A",
            "level_1": {
                "b_key": "Value B"
            }
        }
        target_schema = {
            "root": {
                "a_new_key": "level_1>b_key",
                "level_1": {
                    "b_new_key": "a_key"
                }
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_apply_1_helper_function(self):
        expected_result = {
            "a_new_key": "<p>El otro día comentándolo</p>"
        }
        source = {
            "level_1": {
                "a_key": "<p>El otro d&iacute;a coment&aacute;ndolo</p>"
            }
        }
        target_schema = {
            "root": {
                "a_new_key": "level_1>a_key:html_unescape"
            }
        }
        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_apply_2_chained_helper_function(self):
        expected_result = {
            "a_new_key": "El otro día comentándolo"
        }

        source = {
            "level_1": {
                "a_key": "<p>El otro d&iacute;a coment&aacute;ndolo</p>"
            }
        }

        target_schema = {
            "root": {
                "a_new_key": "level_1>a_key:html_unescape:html_cleaner"
            }
        }

        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_schema_ref(self):
        expected_result = {
            "collection": [
                {
                    "id": 1,
                    "name": "Name A"
                },
                {
                    "id": 2,
                    "name": "Name B"
                }
            ]
        }

        source = {
            "level_1": {
                "series": [
                    {
                        "base_id": 1,
                        "base_name": "Name A",
                        "base_extra": None
                    },
                    {
                        "base_id": 2,
                        "base_name": "Name B",
                        "base_extra": None
                    }
                ]
            }
        }

        target_schema = {
            "root": {
                "collection": ["level_1>series$item"]
            },
            "item": {
                "id": "base_id",
                "name": "base_name"
            }
        }

        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_empty_schema_ref(self):
        expected_result = {
            "collection": []
        }

        source = {
            "level_1": {
                "series": []
            }
        }

        target_schema = {
            "root": {
                "collection": ["level_1>series$item"]
            },
            "item": {
                "id": "base_id",
                "name": "base_name"
            }
        }

        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)

    def test_recursive_schema_ref(self):
        expected_result = {
            "collection": [
                {
                    "id": 1,
                    "name": "Name A",
                    "collection": [
                        {
                            "id": 3,
                            "name": "Name AA",
                            "collection": []
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Name B",
                    "collection": []
                }
            ]
        }

        source = {
            "level_1": {
                "series": [
                    {
                        "base_id": 1,
                        "base_name": "Name A",
                        "series": [
                            {
                                "base_id": 3,
                                "base_name": "Name AA",
                                "series": []
                            }
                        ]
                    },
                    {
                        "base_id": 2,
                        "base_name": "Name B",
                        "series": []
                    }
                ]
            }
        }

        target_schema = {
            "root": {
                "collection": ["level_1>series$item"]
            },
            "item": {
                "id": "base_id",
                "name": "base_name",
                "collection": ["series$item"]
            }
        }

        result = Transformer(source, target_schema).transform()
        self.assertDictEqual(result, expected_result)
