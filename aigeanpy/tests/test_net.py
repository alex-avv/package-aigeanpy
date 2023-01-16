# Disabling no-value-for-parameter
# pylint: disable = E1120
import requests
from unittest.mock import patch
import pytest
from aigeanpy.net import query_isa, download_isa


def test_query_isa_raise_TyperError_when_start_date_is_not_str():
    with pytest.raises(TypeError) as err:
        query_isa(start_date=1234)


def test_query_isa_raise_TyperError_when_stop_date_is_not_str():
    with pytest.raises(TypeError) as err:
        query_isa(stop_date=1234)


def test_query_isa_raise_TyperError_when_instrument_is_not_str():
    with pytest.raises(TypeError) as err:
        query_isa(instrument=1234)


def test_query_isa_raise_ValueError_when_start_date_is_not_YYYY_MM_DD_format():
    with pytest.raises(ValueError) as err:
        query_isa(start_date='10012-1-1')


def test_query_isa_raise_ValueError_when_time_interval_larger_than_3():
    with pytest.raises(ValueError) as err:
        query_isa(start_date='2000-1-1', stop_date='2000-1-5')


def test_query_isa_raise_ValueError_when_time_interval_less_than_0():
    with pytest.raises(ValueError) as err:
        query_isa(start_date='2000-1-2', stop_date='2000-1-1')


def test_mock_query_isa_has_no_internet_connect():
    start_date = '2023-01-11'
    stop_date = '2023-01-14'
    instrument = 'Fand'
    http = ('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/'
            '?start_date=' + start_date + '&stop_date=' + stop_date +
            '&instrument=' + instrument)

    with patch.object(requests, 'get') as mock_get:
        response = query_isa(start_date, stop_date, instrument)
        mock_get.assert_called_with(http)


def test_download_isa_raise_TypeError_when_input_filename_is_not_str():
    filename = 1234
    with pytest.raises(TypeError):
        download_isa(filename)


def test_download_isa_raise_TypeError_when_input_savedir_is_not_str():
    filename = 'aigean_fan_20230112_074702'
    save_dir = 1234
    with pytest.raises(TypeError):
        download_isa(save_dir=save_dir)


def test_mock_download_isa_has_no_internet_connect():
    start_date = '2023-01-11'
    stop_date = '2023-01-14'
    instrument = 'Fand'
    http = ('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/'
            '?start_date=' + start_date + '&stop_date=' + stop_date +
            '&instrument=' + instrument)

    with patch.object(requests, 'get') as mock_get:
        response = query_isa(start_date, stop_date, instrument)
        mock_get.assert_called_with(http)
