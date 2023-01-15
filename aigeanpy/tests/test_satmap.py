import pytest
from aigeanpy import satmap
from pathlib import Path

def test_get_satmap_return_correct_type_when_input_Lir():
    filename = 'aigean_lir_20230104_145310.asdf'
    lir = satmap.get_satmap(filename)
    assert isinstance(lir, satmap.SatMap)

def test_get_satmap_return_correct_type_when_input_Fand():
    filename = 'aigean_fan_20230104_150010.zip'
    fand = satmap.get_satmap(filename)
    assert isinstance(fand, satmap.SatMap)

def test_get_satmap_return_correct_type_when_input_Manannan():
    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    assert isinstance(man, satmap.SatMap)

def test_get_satmap_return_SatMap_object_with_correct_meta_data_Lir():
    filename = 'aigean_lir_20230104_145310.asdf'
    lir = satmap.get_satmap(filename)
    dict = {'archive': 'ISA', 'instrument': 'Lir', 'observatory': 'Aigean',
            'resolution': 30, 'xcoords': (100, 700), 'ycoords': (0, 300), 'obs_date': '2023-01-04 14:53:10'}
    assert lir.meta == dict

def test_get_satmap_return_SatMap_object_with_correct_meta_data_Fand():
    filename = 'aigean_fan_20230104_150010.zip'
    fand = satmap.get_satmap(filename)
    dict = {'archive': 'ISA', 'instrument': 'Fand', 'observatory': 'Aigean',
            'resolution': 5, 'xcoords': (450, 675), 'ycoords': (150, 200), 'obs_date': '2023-01-04 15:00:10'}

    assert fand.meta == dict

def test_get_satmap_return_SatMap_object_with_correct_meta_data_Man():
    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    dict = {'archive': '', 'instrument': 'Manannan', 'observatory': 'Aigean',
            'resolution': 15, 'xcoords': (750, 1200), 'ycoords': (250, 400), 'obs_date': '2022-12-05 19:45:10'}

    assert man.meta == dict

def test_SatMapFactory_raise_ValueError_when_input_filename_cannot_match():
    filename = 'test.asdf'
    with pytest.raises(ValueError) as err:
        test = satmap.get_satmap(filename)

def test_earth_to_pixel_return_correct_value():
    x = 750
    y = 250
    resolution = 15
    assert satmap.earth_to_pixel(x,y,resolution) == (50, 16)

def test_pixel_to_earth_return_correct_value():
    x = 75
    y = 25
    resolution = 15
    assert satmap.pixel_to_earth(x,y,resolution) == (1125, 375)



