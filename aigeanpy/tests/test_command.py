# Disabling missing-function-docstring error
# pylint: disable = C0116
from pathlib import Path; import os; 
CWD = Path(os.getcwd()); TEST_DIR = Path(__file__).parent
import yaml, json
from pytest import mark, raises
import subprocess
from subprocess import check_output
import sys
import numpy as np
from aigeanpy.satmap import get_satmap
from aigeanpy.command import unordered_mosaic, output_info


with open(TEST_DIR/'fixtures/fixture_command.yml', 'r',
          encoding="utf-8") as yml_fixtures:
    fixtures = yaml.safe_load(yml_fixtures)


#~~~ AIGEAN_METADATA TESTS ~~~#
# Mocking aigeanpy.satmap.get_satmap function which requires to open files. 
# Returns 'SatMap' object with only-defined meta member variable.
# With Aigean observations from the 05/Dec/2022 to the 20/Dec/2022
def get_satmap_mock(filename):
    with open(TEST_DIR/'extra_aigean_files/metadata_sample.json', 'r',
              encoding="utf-8") as json_metadata:
        dict_metadata = json.load(json_metadata)
    
    meta = dict_metadata[f'{filename}']
    # Changing the x- and y-coordinates (stored in the JSON file as lists) to
    # tuples
    for key in meta:
        if key not in ['archive', 'instrument', 'observatory', 'resolution',
                       'xcoords', 'ycoords', 'obs_date']:
            raise TypeError
        elif f'{key}' == 'xcoords':
            meta['xcoords'] = tuple(meta['xcoords'])
        elif f'{key}' == 'ycoords':
            meta['ycoords'] = tuple(meta['ycoords'])   

    # Defining mock class
    class MockClass:
        def __init__(self, meta):
            self.meta = meta

    return MockClass(meta)


@mark.parametrize('test_name', fixtures['output_info'])
def test_output_info(capsys, test_name):
    properties = list(test_name.values())[0]
    files = properties['parameters']
    expected_output = properties['expected_value']

    # Capturing expected print-out message
    sys.stdout.write(expected_output)
    expected_print = capsys.readouterr().out

    # Asserting print-out message when calling output_info is as expected
    output_info(files, get_satmap_mock, TEST_DIR)
    assert capsys.readouterr().out == expected_print


@mark.parametrize('test_name', fixtures['metadata'])
def test_metadata(capsys, test_name):
    properties = list(test_name.values())[0]
    parameters = properties['parameters']
    expected_output = properties['expected_value']
    
    # Capturing expected print-out message
    sys.stdout.write(expected_output)
    expected_print = capsys.readouterr().out

    # Asserting print-out message when calling output_info is as expected
    os.chdir(TEST_DIR)
    output_print = check_output(parameters).decode("utf-8").replace('\r','')
    os.chdir(CWD)
    assert output_print == expected_print   


#~~~ AIGEAN_MOSAIC TESTS ~~~#
def test_unordered_mosaic():
    lir_map_1 = get_satmap('aigean_lir_20230104_145310.asdf')
    lir_map_2 = get_satmap('extra_aigean_files/'
                           'aigean_lir_20230104_152610.asdf')
    man_map_1 = get_satmap('extra_aigean_files/'
                           'aigean_man_20230104_151010.hdf5')
    man_map_2 = get_satmap('extra_aigean_files/'
                           'aigean_man_20230104_152610.hdf5')
    fan_map_1 = get_satmap('aigean_fan_20230104_150010.zip')
    fan_map_2 = get_satmap('aigean_fan_20230112_074702.zip')
    fan_map_2.meta['obs_date'] = '2023-01-04 14:53:10'
    
    satmaps = [man_map_1, man_map_2, fan_map_1, fan_map_2, lir_map_1,
               lir_map_2]
    # Trying to build mosaic in the specified ordered. Note that the correct
    # order would be man_map_1.mosaic(lir_map_1).mosaic(lir_map_2 OR fan_map_2)
    # .mosaic(man_map_2). Since lir_map_2 is placed at the end of the list it
    # will be added to the mosaic last.
    mosaic = unordered_mosaic(satmaps)
    # mosaic.visualise()
    
    expected_array = np.load(TEST_DIR/'extra_aigean_files/'
                             'mosaic_data_sample.npy')
    np.testing.assert_almost_equal(mosaic.data, expected_array)
