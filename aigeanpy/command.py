# Disabling invalid-name, missing-module-docstring, too-many-branches,
# redefined-outer-name, bare-except and broad-except
# pylint: disable = C0103, C0114, R0912, W0621, W0702, W0703
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
import json
import sys
from pathlib import Path
from os import getcwd, chdir
from numpy import argmax, inf
from aigeanpy.net import query_isa, download_isa
from aigeanpy.satmap import get_satmap
CWD = Path(getcwd())


def get_latest_obs(query):
    """ Returns the latest observation from a query.

    Parameters
    ----------
    query : list of dicts
        Query, as output by the Aigean webservice.

    Returns
    -------
    latest_obs : dict
        Resultant newest observation.

    """

    # Finding the index of the newest observation
    latest_i = argmax([datetime.strptime(obs['date'] + ' ' + obs['time'],
                                         '%Y-%m-%d %H:%M:%S')
                       for obs in query])
    latest_obs = query[latest_i]
    return latest_obs


def output_info(files, get_satmap, DIR):
    """ Outputs metadata information from the specified files.

    Parameters
    ----------
    files : list of strs
        List of filenames from which to extract metadata.
    get_satmap : function
        Function to get aigeanpy.satmap.SatMap objects.
    DIR : Path
        Path object denoting system directory.
    """

    failed = ''
    missing = ''

    for file in files:
        # Try processing the file, if not store the missing/failed file name
        try:
            meta = get_satmap(file).meta
        except:  # noqa
            # Checking whether file exits
            file_path = DIR/file
            if not file_path.is_file():
                missing += f' - {file}\n'
            else:
                failed += f' - {file}\n'
            meta = None

        if meta:
            # Replacing empty data with informative message
            for key in meta:
                if meta[f'{key}'] == '':
                    meta[f'{key}'] = '<No information available>'

            # Printing screen information
            if len(files) == 1:
                for key in meta:
                    value = meta[f'{key}']
                    sys.stdout.write(f'{key}: {value}\n')
            else:
                for key in meta:
                    value = meta[f'{key}']
                    sys.stdout.write(f'{file}:{key}: {value}\n')

    # Print messages with missing/failed files
    if failed:
        sys.stdout.write("\nThese files failed while being processed\n"
                         f"{failed}")
    if missing:
        sys.stdout.write(f"\nThese files couldn't be found\n{missing}")


def unordered_mosaic(satmaps, resolution=None):
    """ Generates a mosaic from a SatMap list, independent of order.

    Parameters
    ----------
    satmaps : list of SatMaps
        List of aigeanpy.satmap.SatMap objects to build the mosaic.
    resolution : int, optional
        Mosaic resolution, by default None.

    Returns
    -------
    mosaic : SatMap
        aigeanpy.satmap.SatMap object with the mosaic.
    """

    processed = []
    store_err = []
    mosaic = None

    # Choosing the smallest resolution among the satmap list if not specified
    if resolution is None:
        resolution = inf
        for satmap in satmaps:
            if satmap.meta['resolution'] < resolution:
                resolution = int(satmap.meta['resolution'])

    # Getting mosaic from the first two available satmaps
    for satmap in satmaps:
        for other_satmap in satmaps:
            if satmap != other_satmap:
                try:
                    mosaic = satmap.mosaic(other_satmap, resolution)
                    processed += [satmap, other_satmap]
                    # Breaking the inner for loop
                    break
                except Exception as err:
                    store_err += [f'{type(err).__name__}: {str(err)}']
        else:
            # Continuing if inner loop wasn't broken.
            continue
        # Inner loop was broken, breaking outer.
        break

    # Getting mosaic from the rest of satmaps
    if mosaic:
        # (n - 2) satmaps to be processed |
        for n in range(len(satmaps) - 2):  # pylint: disable = W0612
            for satmap in satmaps:
                if satmap not in processed:
                    try:
                        mosaic = mosaic.mosaic(satmap)
                        processed += [satmap]
                        # Breaking the inner for loop
                        break
                    except Exception as err:
                        store_err += [f'{type(err).__name__}: {str(err)}']
    # Only keeping unique error messages
    store_err = list(set(store_err))

    # If at least one of the input files fails, show relevant message. Else
    # return the mosaic.
    if len(processed) != len(satmaps):
        # If only error is 'ValueError: Two data must overlap', then print on
        # screen
        overlap_err = "ValueError: Two data must overlap"
        if len(store_err) == 1 and store_err[0] == overlap_err:
            err_info = overlap_err + '\n'
        # Else print only non-overlap-related errors
        else:
            err_info = ''
            for err in store_err:
                # Only keeping non-overlap-related errors
                err_info += f'{err}\n' if err != overlap_err else ''
        sys.stderr.write("It was not possible to build a mosaic from the "
                         "specified files and resolution. The exceptions "
                         f"were:\n{err_info}")
        sys.exit(1)
    else:
        return mosaic


def today():
    ''' Downloads the latest image of the Aigean archive.

    For help in using this command, type in bash:
        $ aigean_today -h
    '''

    parser = ArgumentParser(description="Downloads the latest observation of "
                            "the archive.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--instrument', '-i', metavar='<instrument>',
                        default=None, type=str, help="Name of the instrument.")
    parser.add_argument('--saveplot', '-s', default=False, action='store_true',
                        help="Specifies whether to save the observation as a "
                        "PNG file.")
    arguments = parser.parse_args()
    instrument, saveplot = arguments.instrument, arguments.saveplot

    if saveplot and instrument == 'ecne':
        sys.stderr.write("Ecne files (containing measurements but not images) "
                         "can't be visualised.")
        sys.exit(1)

    if instrument:
        # Automatically lowercasing first letter of instrument
        if instrument[0].isupper():
            instrument = instrument[0].lower() + instrument[1:]

        # Checking the validity of the input
        if instrument not in ['lir', 'manannan', 'fand', 'ecne']:
            sys.stderr.write("Selected instrument must be either Lir, "
                             "Manannan, Fand or Ecne.")
            sys.exit(1)

        # Getting the running day's data (implicit in default query_isa
        # parameters)
        sys.stdout.write('Results from the query:\n')
        query = json.loads(query_isa(instrument=instrument).text)
        # Obtaining the most recent observation
        newest_obs = get_latest_obs(query)

    else:
        sys.stdout.write('Results from the query:\n')
        query = json.loads(query_isa().text)
        newest_obs = get_latest_obs(query)
        instrument = newest_obs['instrument']

    if saveplot and instrument == 'ecne':
        sys.stderr.write("Ecne files (containing measurements but not images) "
                         "can't be visualised.")
        sys.exit(1)

    # Changing to current working directory and downloading the file
    chdir(CWD)
    download_isa(newest_obs['filename'])

    # Downloading PNG if specified
    if saveplot:
        filename = get_satmap(newest_obs['filename']).visualise(save=True)
        sys.stdout.write(f'Name of saved PNG: {filename}')


def metadata():
    ''' Shows the metadata of the specified Aigean archive files.

    For help in using this command, type in bash:
        $ aigean_metadata -h
    '''

    parser = ArgumentParser(description="Shows the metadata information of "
                            "the specified file(s).",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('files', nargs='+', metavar='<filename>',
                        help="Name of the file(s).")
    arguments = parser.parse_args()
    files = arguments.files

    output_info(files, get_satmap, CWD)


def mosaic():
    ''' Downloads a mosaic from the specified Aigean archive files.

    For help in using this command, type in bash:
        $ aigean_mosaic -h
    '''

    parser = ArgumentParser(description="Generates a mosaic from the "
                            "specified imager files.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_1', nargs=1, metavar='<filename>',
                        help="Name of an imager file.")
    parser.add_argument('files_2', nargs='+', metavar='<filename>',
                        help="Name of an (or many) imager file(s).")
    parser.add_argument('--resolution', '-r', metavar='<resolution>',
                        default=None, type=int, help="Resolution of the "
                        "mosaic. If set, make sure it is compatible with "
                        "the given files.")
    arguments = parser.parse_args()
    resolution = arguments.resolution
    files = arguments.file_1 + arguments.files_2

    # Changing to current working directory and getting mosaic
    chdir(CWD)
    satmaps = list(map(get_satmap, files))
    mosaic = unordered_mosaic(satmaps, resolution)

    # Downloading mosaic as PNG
    filename = mosaic.visualise(save=True)
    sys.stdout.write(f'Name of saved PNG: {filename}')
