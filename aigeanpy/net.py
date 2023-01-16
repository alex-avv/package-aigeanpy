import requests
from pathlib import Path
import datetime

Now = datetime.datetime.now()
Current_time = Now.strftime("%Y-%m-%d")


def query_isa(start_date=Current_time, stop_date=Current_time, instrument=''):
    """query isa with start date, stop date and instrument

    Parameters
    ----------
    start_date : str, optional
        the start date of the data query, by default Current_time
    stop_date : str, optional
        the stop date of the data query, by default Current_time
    instrument : str, optional
        instrument for query data, by default ''

    Returns
    -------
    Response
        Response message from the url

    Raises
    ------
    TypeError
        Start data must in str type
    TypeError
        Stop data must in str type
    TypeError
        Instrument must in str type
    ValueError
        Start time should be in YYYY-MM-DD format
    ValueError
        Stop time should be in YYYY-MM-DD format
    ValueError
        Range requested too long - this service is limited to 3 days
    ValueError
        Stop time should be after the start time
    ConnectionError
        There is no internet connection
    """
    if not isinstance(start_date, str):
        raise TypeError('Start data must in str type')
    if not isinstance(stop_date, str):
        raise TypeError('Stop data must in str type')
    if not isinstance(instrument, str):
        raise TypeError('Instrument must in str type')
    # connection error
    try:
        time_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:  # noqa
        raise ValueError('Start time should be in YYYY-MM-DD format')
    try:
        time_stop = datetime.datetime.strptime(stop_date, '%Y-%m-%d')
    except:  # noqa
        raise ValueError('Stop time should be in YYYY-MM-DD format')

    if (time_stop-time_start).days > 3:
        raise ValueError('Range requested too long - this service is limited '
                         'to 3 days')
    if (time_stop-time_start).days < 0:
        raise ValueError('Stop time should be after the start time')

    if stop_date == Current_time:
        stop_date = ''
    else:
        stop_date = '&stop_date='+stop_date

    if instrument != '':
        instrument = '&instrument='+instrument
    http = ('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/'
            '?start_date='+start_date+stop_date+instrument)

    try:
        response = requests.get(http)
        print(response.text)
    except Exception:
        raise ConnectionError('There is no internet connection')
    return response


def download_isa(filename, save_dir=''):
    """download the file

    Parameters
    ----------
    filename : str
        filename you want to download from internet, you can see through the
        output of query_isa
    save_dir : str, optional
        the file saving path, by default ''
    Raises
    ------
    TypeError
        Filename must in str type
    TypeError
        Save_dir must in str type
    ConnectionError
        There is no internet connection
    ValueError
        File name is not valid, retype the valid file name
    """
    if not isinstance(filename, str):
        raise TypeError('Filename must in str type')
    if not isinstance(save_dir, str):
        raise TypeError('Save_dir must in str type')
    http = ('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/'
            '?filename='+filename)
    try:
        response = requests.get(http)
    except:  # noqa
        raise ConnectionError('There is no internet connection')

    if response.status_code != 200:
        raise ValueError('File name is not valid, retype the valid file name')

    path = Path(save_dir+filename)
    path.write_bytes(response.content)
