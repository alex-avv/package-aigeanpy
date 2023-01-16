# Disabling missing-function-docstring error
# pylint: disable = C0116
from pathlib import Path; TEST_DIR = Path(__file__).parent
import yaml
from pytest import mark, raises
import numpy as np
from aigeanpy.satmap import get_satmap
from aigeanpy.command import unordered_mosaic


with open(TEST_DIR/'fixtures/fixture_command.yml', 'r',
          encoding="utf-8") as yml_fixtures:
    fixtures = yaml.safe_load(yml_fixtures)


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
