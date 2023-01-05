# Disabling missing-function-docstring error
# pylint: disable = C0116
from pathlib import Path
import yaml
from pytest import mark, raises

TEST_DIR = Path(__file__).parent
with open(TEST_DIR/'fixtures/fixture_example.yml', 'r',
          encoding="utf-8") as yml_fixtures:
    dict_fixtures = yaml.safe_load(yml_fixtures)


# Asserting Error Message is as expected
@mark.parametrize('dict_case', dict_fixtures['function_1_cases_12'])
def test_function_1_cases_12(dict_case):
    dict_properties = list(dict_case.values())[0]
    _parameters = dict_properties['parameters']
    expected_error_message_or_value = (dict_properties
                                       ['expected_error_message_or_value'])

    with raises(NotImplementedError) as exception:
        raise NotImplementedError("String_or_Value")
    assert str(exception.value) == expected_error_message_or_value


# Asserting Value is as expected
@mark.parametrize('dict_case', dict_fixtures['function_1_cases_34'])
def test_function_1_cases_34(dict_case):
    dict_properties = list(dict_case.values())[0]
    _parameters = dict_properties['parameters']

    # import function_1 instead of below
    def function_1(_parameters):
        return 'Value'
    assert function_1(_parameters) == 'Value'
