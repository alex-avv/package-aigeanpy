# Disabling missing-class-docstring, pointless-statement, redefined-builtin and
# and bare-except
# pylint: disable = C0115, W0104, W0622, W0702
import pytest
import json
import asdf
import zipfile
import numpy as np
from io import BytesIO
from aigeanpy import satmap
from pathlib import Path
from unittest import mock, TestCase


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
            'resolution': 30, 'xcoords': (100, 700), 'ycoords': (0, 300),
            'obs_date': '2023-01-04 14:53:10'}
    assert lir.meta == dict


def test_get_satmap_return_SatMap_object_with_correct_meta_data_Fand():
    filename = 'aigean_fan_20230104_150010.zip'
    fand = satmap.get_satmap(filename)
    dict = {'archive': 'ISA', 'instrument': 'Fand', 'observatory': 'Aigean',
            'resolution': 5, 'xcoords': (450, 675), 'ycoords': (150, 200),
            'obs_date': '2023-01-04 15:00:10'}

    assert fand.meta == dict


def test_get_satmap_return_SatMap_object_with_correct_meta_data_Man():
    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    dict = {'archive': '', 'instrument': 'Manannan', 'observatory': 'Aigean',
            'resolution': 15, 'xcoords': (750, 1200), 'ycoords': (250, 400),
            'obs_date': '2022-12-05 19:45:10'}

    assert man.meta == dict


def test_SatMapFactory_raise_ValueError_when_input_filename_cannot_match():
    filename = 'test.asdf'
    with pytest.raises(ValueError) as err:
        test = satmap.get_satmap(filename)


def test_earth_to_pixel_return_correct_value():
    x = 750
    y = 250
    resolution = 15
    assert satmap.earth_to_pixel(x, y, resolution) == (50, 17)


def test_pixel_to_earth_return_correct_value():
    x = 75
    y = 25
    resolution = 15
    assert satmap.pixel_to_earth(x, y, resolution) == (1125, 375)


def test_SatMap_generate_correct_fov_attribute_value():
    xcoords = (750, 1200)
    ycoords = (250, 400)
    expected_val_x = xcoords[1] - xcoords[0]
    expected_val_y = ycoords[1] - ycoords[0]
    expected = (expected_val_x, expected_val_y)

    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    actual = man.fov
    assert actual == expected


def test_SatMap_generate_correct_centre_attribute_value():
    xcoords = (750, 1200)
    ycoords = (250, 400)
    expected_val_x = int((xcoords[1] + xcoords[0])/2)
    expected_val_y = int((ycoords[1] + ycoords[0])/2)
    expected = (expected_val_x, expected_val_y)

    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    actual = man.centre
    assert actual == expected


def test_SatMap_generate_correct_shape_attribute_value():
    expected = (10, 30)
    filename = 'aigean_man_20221205_194510.hdf5'
    man = satmap.get_satmap(filename)
    actual = man.shape
    assert actual == expected

# Tests for SatMap function by using mock SatMap object fand and lir


def _get_fand(filename):
    file_path_abs = sorted(Path().rglob(filename))[0]
    meta = {}
    data = []
    with zipfile.ZipFile(file_path_abs, 'r') as f:
        file_json = json.load(BytesIO(f.read(f.namelist()[0])))
        meta = _meta_generate(file_json)
        data = np.load(BytesIO(f.read(f.namelist()[1])))
    return satmap.Fand(meta, data)


def _get_lir(filename):
    file_path_abs = sorted(Path().rglob(filename))[0]
    meta = {}
    data = []
    with asdf.open(file_path_abs, 'r') as f:
        meta = _meta_generate(f)
        data = np.array(f['data'])
    return satmap.Lir(meta, data)


def _meta_generate(meta_origin):
    meta = {}
    # meta contain following keys
    meta_list = ['archive', 'instrument', 'observatory', 'resolution',
                 'xcoords', 'ycoords']
    for key in meta_list:
        # update the information to the meta
        try:
            meta.update({key: meta_origin[key]})
        # update with an empty value if the file do not contain the key
        except:  # noqa
            meta.update({key: ''})

    # change coords into tuple, the type of each element is int
    meta['xcoords'] = tuple(map(int, meta['xcoords']))
    meta['ycoords'] = tuple(map(int, meta['ycoords']))
    # combine the date and time

    date = f"{meta_origin['date']} {meta_origin['time']}"
    meta.update({'obs_date': date})
    return meta


class Ecne:
    pass


def test_add_two_differetn_types_data_raise_TypeError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)

    with pytest.raises(TypeError) as err:
        ecne = Ecne()
        mock_fand + ecne


def test_add_two_SatMap_with_diff_resolution_raise_ValueError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    with pytest.raises(ValueError) as err:
        mock_fand + mock_lir


def test_add_two_SatMap_from_diff_date():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    mock_lir.meta['obs_date'] = '2023-01-14 14:53:10'
    with pytest.raises(ValueError) as err:
        mock_fand + mock_lir


def test_add_two_SatMap_should_generate_the_same_data_when_add_itself():
    fand_file = 'aigean_fan_20230104_150010.zip'
    fand1 = _get_fand(fand_file)
    expected = fand1
    actual = fand1 + fand1
    assert (actual.data == expected.data).all()


def test_add_two_SatMap_generate_correct_added_SatMap():
    fand_file = 'aigean_fan_20230104_150010.zip'
    fand1 = _get_fand(fand_file)
    fand_file2 = 'aigean_fan_20230112_074702.zip'
    fand2 = _get_fand(fand_file2)
    # set the other satmap to be the same date, but contains a map with
    # different shape
    fand2.meta['obs_date'] = '2023-01-04 14:53:10'
    actual = fand1 + fand2
    expected_centre = (637, 175)
    assert actual.centre == expected_centre


def test_sub_two_SatMap_from_the_same_day_raise_ValueError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    with pytest.raises(ValueError) as err:
        mock_fand - mock_lir


def test_sub_two_SatMap_with_diff_resolution_raise_ValueError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    with pytest.raises(ValueError) as err:
        mock_fand - mock_lir


def test_sub_two_diff_instrument_raise_TypeError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    ecne = Ecne()

    with pytest.raises(TypeError) as err:
        mock_fand - ecne


def test_sub_two_overlap_satmap():
    fand_file = 'aigean_fan_20230104_150010.zip'
    fand1 = _get_fand(fand_file)
    fand_file2 = 'aigean_fan_20230112_074702.zip'
    fand2 = _get_fand(fand_file2)

    actual = fand1 - fand2
    actual_arr = actual.data
    expected_arr = fand1.data[:, 30:45] - fand2.data[:, :15]
    assert (expected_arr == actual_arr).all()


def test_mosaic_two_diff_instrument_raise_TypeError():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    ecne = Ecne()

    with pytest.raises(TypeError) as err:
        mock_fand.mosaic(ecne)


def test_mosaic_only_allows_overlap_instruments_when_padding_is_false():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)
    mock_lir.meta['xcoords'] = (10, 20)
    mock_lir.meta['ycoords'] = (15, 25)

    with pytest.raises(ValueError) as err:
        mock_fand.mosaic(mock_lir, padding=False)


def test_mosaic_include_type_generate_correct_centre_with_padding_to_be_False():  # noqa
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    actual = mock_fand.mosaic(mock_lir, padding=False)
    expected = (400, 150)
    assert actual.centre == expected


def test_mosaic_intersect_type_generate_correct_centre_with_padding_to_be_False():  # noqa

    fand_file = 'aigean_fan_20230104_150010.zip'
    fand1 = _get_fand(fand_file)
    fand_file2 = 'aigean_fan_20230112_074702.zip'
    fand2 = _get_fand(fand_file2)

    # set fand2 to be in the same day
    fand2.meta['obs_date'] = '2023-01-04 14:53:10'

    actual = fand1.mosaic(fand2, padding=False)
    expected = (637, 175)
    assert actual.centre == expected


def test_mosaic_generate_correct_centre_with_padding_to_be_True():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    lir_file = 'aigean_lir_20230104_145310.asdf'
    mock_lir = _get_lir(lir_file)

    actual = mock_fand.mosaic(mock_lir)
    expected = (400, 150)
    assert actual.centre == expected


def test_visualise_savepath_should_be_str():
    fand_file = 'aigean_fan_20230104_150010.zip'
    mock_fand = _get_fand(fand_file)
    with pytest.raises(TypeError) as err:
        mock_fand.visualise(save_path=123)


class mocktest(TestCase):

    def test_add(self):
        lir_map1 = satmap.get_satmap('aigean_fan_20221205_191610.zip')
        lir_map2 = satmap.get_satmap('aigean_fan_20221205_192210.zip')
        get_added = mock.Mock(side_effect=lir_map1.__add__)
        result = get_added(lir_map2)
        self.assertEqual(get_added.called, True)
        self.assertEqual(get_added.call_count, 1)
        self.assertEqual(result.centre, (300, 275))

    def test_sub(self):
        lir_map1 = satmap.get_satmap('aigean_fan_20221208_170852.zip')
        lir_map2 = satmap.get_satmap('aigean_fan_20221210_150420.zip')
        get_substracted = mock.Mock(side_effect=lir_map1.__sub__)
        result = get_substracted(lir_map2)
        self.assertEqual(get_substracted.called, True)
        self.assertEqual(get_substracted.call_count, 1)
        self.assertEqual(result.centre, (1237, 475))

    def test_mosaic_padding_true(self):
        lir_map1 = satmap.get_satmap('aigean_lir_20221205_191610.asdf')
        lir_map2 = satmap.get_satmap('aigean_man_20221205_194510.hdf5')
        get_substracted = mock.Mock(side_effect=lir_map1.mosaic)
        result = get_substracted(lir_map2, padding=True)
        self.assertEqual(get_substracted.called, True)
        self.assertEqual(get_substracted.call_count, 1)
        self.assertEqual(result.centre, (850, 350))

    def test_mosaic_padding_false(self):
        lir_map1 = satmap.get_satmap('aigean_lir_20221205_191610.asdf')
        lir_map2 = satmap.get_satmap('aigean_man_20221205_194510.hdf5')
        get_substracted = mock.Mock(side_effect=lir_map1.mosaic)
        result = get_substracted(lir_map2, padding=False)
        self.assertEqual(get_substracted.called, True)
        self.assertEqual(get_substracted.call_count, 1)
        self.assertEqual(result.centre, (800, 350))
