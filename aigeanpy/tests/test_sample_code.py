# pylint: disable = C0103, C0114, C0116, W0612, W0613
# type: ignore
from pathlib import Path
import yaml
from pytest import mark, raises

TEST_DIR = Path(__file__).parent
with open(TEST_DIR/'fixtures/fixture_example.yml', 'r', encoding="utf-8") as ymlFixtures:
    dFixtures = yaml.safe_load(ymlFixtures)


# Asserting Error Message is as expected
@mark.parametrize('dCase', dFixtures['function_1_cases_12'])
def test_function_1_cases_12(dCase):
    dProperties = list(dCase.values())[0]
    parameters = dProperties['parameters']
    expected_error_message_or_value = dProperties['expected_error_message_or_value']

    with raises(NotImplementedError) as exception:
        raise NotImplementedError("String_or_Value")
    assert str(exception.value) == expected_error_message_or_value


# Asserting Value is as expected
@mark.parametrize('dCase', dFixtures['function_1_cases_34'])
def test_function_1_cases_34(dCase):
    dProperties = list(dCase.values())[0]
    parameters = dProperties['parameters']
    expected_error_message_or_value = dProperties['expected_error_message_or_value']

    # import function_1 instead of below
    def function_1(parameters):
        return 'Value'
    assert function_1(parameters) == 'Value'
