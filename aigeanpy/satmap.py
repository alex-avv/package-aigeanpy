# Disabling missing-class-docstring, consider-using-dict-items,
# too-many-branches, too-many-locals, too-many-statements, unused-import and
# bare-except
# pylint: disable = C0115, C0206, R0912, R0914, R0915, W0611, W0702
import json
import h5py
import asdf
import zipfile
import numpy as np
from io import BytesIO
from matplotlib import pyplot as plt
import skimage
from skimage import transform
import os
from pathlib import Path


def _earth_to_pixel_tuple(x, y, resolution):
    """ Change earth coordinate to pixel coordinate.

    Parameters
    ----------
    x : tuple
        Earth coordinate, xcoords.
    y : tuple
        Earth coordinate, ycoords.
    resolution : int
        Data resolution

    Returns
    -------
    tuple
        Pixel coordinate, xcoords.
    tuple
        Pixel coordinate, ycoords. Positive y-values going downwards.
    """
    # change earth coords to the pixel coords by dividing resolution and move
    # the coords to the origin
    pixel_xcoords = (earth_to_pixel(x[0], y[0], resolution)[0],
                     earth_to_pixel(x[1], y[1], resolution)[0])
    # Filp the Y-axis to achieve: In the top-left corner and positive y-values
    # going downwards.
    pixel_ycoords = (earth_to_pixel(x[0], y[0], resolution)[1],
                     earth_to_pixel(x[1], y[1], resolution)[1])
    return pixel_xcoords, pixel_ycoords


def earth_to_pixel(x, y, resolution):
    """ Change earth coordinate to pixel coordinate.

    Parameters
    ----------
    x : int
        Earth coordinate, xcoords.
    y : int
        Earth coordinate, ycoords.
    resolution : int
        Data resolution.

    Returns
    -------
    int
        Pixel coordinate, xcoords.
    int
        Pixel coordinate, ycoords.

    Examples
    --------
    >>> from aigeanpy.satmap import earth_to_pixel
    >>> x = 10
    >>> y = 20
    >>> resolution = 5
    >>> earth_to_pixel(x,y,resolution)
    (2, 4)
    """
    return x // resolution, y // resolution


def _pixel_to_earth_tuple(x, y, resolution):
    """ Change pixel coordinate to earth coordinate.

    Parameters
    ----------
    x : tuple
        Pixel coordinate, xcoords.
    y : tuple
        Pixel coordinate, ycoords.
    resolution : int
        Data resolution.

    Returns
    -------
    tuple
        Earth coordinate, xcoords.
    tuple
        Earth coordinate, ycoords.
    """
    # change earth coords to the pixel coords by dividing resolution and move
    # the coords to the origin
    xcoords = (pixel_to_earth(x[0], y[0], resolution)[0],
               pixel_to_earth(x[1], y[1], resolution)[0])
    # Filp the Y-axis to achieve: In the top-left corner and positive y-values
    # going downwards.
    ycoords = (pixel_to_earth(x[0], y[0], resolution)[1],
               pixel_to_earth(x[1], y[1], resolution)[1])
    return xcoords, ycoords


def pixel_to_earth(x, y, resolution):
    """ Change pixel coordinate to earth coordinate.

    Parameters
    ----------
    x : int
        Pixel coordinate, xcoords.
    y : int
        Pixel coordinate, ycoords.
    resolution : int
        Data resolution.

    Returns
    -------
    int
        Earth coordinate, xcoords.
    int
        Earth coordinate, ycoords.

    Examples
    --------
    >>> from aigeanpy.satmap import pixel_to_earth
    >>> x = 10
    >>> y = 20
    >>> resolution = 5
    >>> pixel_to_earth(x,y,resolution)
    (50, 100)
    """
    return x * resolution, y * resolution


class SatMapFactory():
    def get_satmap_obj(self, filename):
        """ Create a SatMap object through data file for SatMap factory.

        Parameters
        ----------
        filename : str
            The name of the file holding the data information.

        Returns
        -------
        SatMap
            Generate a a SatMap object.

        Raises
        ------
        ValueError
            File must match given file name.

        Examples
        --------
        >>> from aigeanpy.satmap import SatMapFactory
        >>> satMapFactory = SatMapFactory()
        >>> filename = 'aigean_fan_20230112_074702.zip'
        >>> fand = satMapFactory.get_satmap_obj(filename)
        >>> fand.meta
        {'archive': 'ISA', 'instrument': 'Fand', 'observatory': 'Aigean', \
'resolution': 5, 'xcoords': (600, 825), 'ycoords': (150, 200), \
'obs_date': '2023-01-12 07:47:02'}
        """
        meta = {}
        data = []
        file_path_abs = None
        try:
            file_path_abs = sorted(Path().rglob(filename))[0]
        except IndexError as e:
            raise ValueError("No matching file can be found")

        satmap = None

        # if it is a HDF5 file, call the get_hdf5 function
        if 'hdf5' in filename:
            meta, data = get_hdf5(file_path_abs)
            satmap = Manannan(meta, data)

        # if it is a ASDF file, call the get_asdf function
        elif 'asdf' in filename:
            meta, data = get_asdf(file_path_abs)
            satmap = Lir(meta, data)

        # if it is a zip file, call the get_zip function
        elif 'zip' in filename:
            meta, data = get_zip(file_path_abs)
            satmap = Fand(meta, data)

        return satmap


def get_satmap(filename):
    """ Create a SatMap object through SatMap Factory.

    Parameters
    ----------
    filename : str
        The name of the file holding the data information.

    Returns
    -------
    SatMap
        Generate a a SatMap object.

    Examples
    --------
    >>> from aigeanpy.satmap import get_satmap
    >>> filename = 'aigean_fan_20230112_074702.zip'
    >>> get_satmap(filename).meta
    {'archive': 'ISA', 'instrument': 'Fand', 'observatory': 'Aigean', \
'resolution': 5, 'xcoords': (600, 825), 'ycoords': (150, 200), \
'obs_date': '2023-01-12 07:47:02'}
    """
    # create a SatMap object calling SatMap Factory
    satMapFactory = SatMapFactory()
    satmap = satMapFactory.get_satmap_obj(filename)

    return satmap


def get_hdf5(file_path):
    """ Get meta and data from file.

    Parameters
    ----------
    file_path : str
        The file path of the file holding the data information.

    Returns
    -------
    dict
        Including info of data. keys including ('archive', 'instrument',
        'observatory', 'resolution', 'xcoords', 'ycoords', 'obs_time')
    array
        Data array.
    """
    with h5py.File(file_path, 'r') as f:
        for key in f.keys():
            data = np.array(f[key]['data'])
            meta = meta_generate(f[key].attrs)
    return meta, data


def get_asdf(file_path):
    """ Get meta and data from file.

    Parameters
    ----------
    file_path : str
        The file path of the file holding the data information.

    Returns
    -------
    dict
        Including info of data. keys including ('archive', 'instrument',
        'observatory', 'resolution', 'xcoords', 'ycoords', 'obs_time')
    array
        Data array.
    """
    with asdf.open(file_path, 'r') as f:
        meta = meta_generate(f)
        data = np.array(f['data'])
    return meta, data


def get_zip(file_path):
    """ Get meta and data from file.

    Parameters
    ----------
    file_path : str
        The file path of the file holding the data information.

    Returns
    -------
    dict
        including info of data. keys including ('archive', 'instrument',
        'observatory', 'resolution', 'xcoords', 'ycoords', 'obs_time')
    array
        Data array.
    """
    with zipfile.ZipFile(file_path, 'r') as f:
        file_json = json.load(BytesIO(f.read(f.namelist()[2])))
        meta = meta_generate(file_json)
        data = np.load(BytesIO(f.read(f.namelist()[4])))
    return meta, data


def meta_generate(meta_origin):
    """ Generate meta data.

    Parameters
    ----------
    meta_origin : dict
        A dict with multiple informations.

    Returns
    -------
    dict
        A dict including info of data. keys including ('archive', 'instrument',
        'observatory','resolution','xcoords','ycoords','obs_time')
    """
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


class SatMap:
    """
    SatMap class contains meta-data and figure data for three imagers, Lir,
    Manannan and Fand.

    Attributes
    ----------
    meta : dict
        Including info of meta-data. keys including ('archive', 'instrument',
        'observatory', 'resolution', 'xcoords', 'ycoords', 'obs_date')
    data : array
        Data to generate the corresponding figure.

    Methods
    -------
    __init__(meta, data)
        Initialize the SatMap class with corresponding meta-data and figure
        data.
    __add__(another_satmap)
        Add the other Satmap object to current Satmap object.
    __sub__(another_satmap)
        Subtract this Satmap with the other input Satmap.
    mosaic(another_satmap, resolution=None, padding=True)
        Do the more complex Satmap object adding.
    visualise(self, save=False, save_path='')
        Visualise this Satmap object with correponding figure data attribute.
    """

    def __init__(self, meta, data):
        """ Initiate the SatMap class.

        Parameters
        ----------
        meta : dict
            Including info of meta-data. keys including ('archive',
            'instrument', 'observatory', 'resolution', 'xcoords', 'ycoords',
            'obs_date')
        data : array
            Data.

        Raises
        ------
        TypeError
            Meta must in dict type
        TypeError
            Data must in np.ndarray type
        """
        if not isinstance(meta, dict):
            raise TypeError('Meta must in dict type')
        if not isinstance(data, np.ndarray):
            raise TypeError('Data must in np.ndarray type')
        self.meta = meta
        self.data = data
        self.fov = (meta['xcoords'][1] - meta['xcoords'][0],
                    meta['ycoords'][1] - meta['ycoords'][0])
        self.shape = data.shape
        self.centre = (int((meta['xcoords'][1] + meta['xcoords'][0]) / 2),
                       int((meta['ycoords'][1] + meta['ycoords'][0]) / 2))
        self.extra = False

    def __add__(self, another_satmap):
        """ Do the object adding.

        Parameters
        ----------
        another_satmap : SatMap
            Another SatMap object.

        Returns
        -------
        SatMap
            A new object that have been added.

        Raises
        ------
        TypeError
            Another_satmap must in SatMap type
        ValueError
            Different instrument cannot be added
        ValueError
            2 data must in the same day
        """
        if not isinstance(another_satmap, SatMap):
            raise TypeError('Another_satmap must in SatMap type')
        if self.meta['resolution'] != another_satmap.meta['resolution']:
            raise ValueError('Different instrument cannot be added')
        if self.meta['obs_date'][:10] != another_satmap.meta['obs_date'][:10]:
            raise ValueError('2 data must in the same day')

        # earth coords of the new object
        data_ex = (min(self.meta['xcoords'][0],
                       another_satmap.meta['xcoords'][0]),
                   max(self.meta['xcoords'][1],
                       another_satmap.meta['xcoords'][1]))
        data_ey = (min(self.meta['ycoords'][0],
                       another_satmap.meta['ycoords'][0]),
                   max(self.meta['ycoords'][1],
                       another_satmap.meta['ycoords'][1]))
        # earth distance from new object bottom left to the origin(0,0)
        offset = (data_ex[0], data_ey[0])
        # get resolution from object
        resolution = self.meta['resolution']

        # earth coords without offset
        data_ex_offset = (data_ex[0]-offset[0], data_ex[1]-offset[0])
        data_ey_offset = (data_ey[0]-offset[1], data_ey[1]-offset[1])
        self_ex_offset = (self.meta['xcoords'][0]-offset[0],
                          self.meta['xcoords'][1]-offset[0])
        self_ey_offset = (self.meta['ycoords'][0]-offset[1],
                          self.meta['ycoords'][1]-offset[1])
        another_ex_offset = (another_satmap.meta['xcoords'][0]-offset[0],
                             another_satmap.meta['xcoords'][1]-offset[0])
        another_ey_offset = (another_satmap.meta['ycoords'][0]-offset[1],
                             another_satmap.meta['ycoords'][1]-offset[1])

        # change earth coords to pixel coords
        data_px, data_py = _earth_to_pixel_tuple(data_ex_offset,
                                                 data_ey_offset, resolution)
        self_px, self_py = _earth_to_pixel_tuple(self_ex_offset,
                                                 self_ey_offset, resolution)
        another_px, another_py = _earth_to_pixel_tuple(another_ex_offset,
                                                       another_ey_offset,
                                                       resolution)

        # generate empty added data
        data = np.zeros((data_py[1] - data_py[0], data_px[1] - data_px[0]))
        data[self_py[0]:self_py[1], self_px[0]:self_px[1]] = self.data
        data[another_py[0]:another_py[1],
             another_px[0]:another_px[1]] = another_satmap.data

        # copy the data info from the addend, but update the new coords
        meta = self.meta.copy()
        meta['ycoords'] = data_ey
        meta['xcoords'] = data_ex

        # generate a new SatMap object and return
        new_satmap = type(self)(meta, data)
        # update attributes for new SatMap
        new_satmap.fov = (meta['xcoords'][1] - meta['xcoords'][0],
                          meta['ycoords'][1] - meta['ycoords'][0])
        new_satmap.shape = data.shape
        new_satmap.centre = (
            int((meta['xcoords'][1] + meta['xcoords'][0]) / 2),
            int((meta['ycoords'][1] + meta['ycoords'][0]) / 2))
        new_satmap.extra = True
        return new_satmap

    def __sub__(self, another_satmap):
        """ Do the object subtract.

        Parameters
        ----------
        another_satmap : SatMap
            Another SatMap object.

        Returns
        -------
        SatMap
            A new object that have been subtracted.

        Raises
        ------
        TypeError
            Another_satmap must in SatMap type
        ValueError
            Different instrument cannot be added
        ValueError
            2 data must in different days
        ValueError
            Two data must overlap
        """
        # if type(another_satmap) is not SatMap:
        if not isinstance(another_satmap, SatMap):
            raise TypeError('Another_satmap must in SatMap type')
        if self.meta['resolution'] != another_satmap.meta['resolution']:
            raise ValueError('Different instrument cannot be subtracted')
        if self.meta['obs_date'][:10] == another_satmap.meta['obs_date'][:10]:
            raise ValueError('2 data must in different days')
        # earth coords of the new object
        data_ex = (max(self.meta['xcoords'][0],
                       another_satmap.meta['xcoords'][0]),
                   min(self.meta['xcoords'][1],
                       another_satmap.meta['xcoords'][1]))
        data_ey = (max(self.meta['ycoords'][0],
                       another_satmap.meta['ycoords'][0]),
                   min(self.meta['ycoords'][1],
                       another_satmap.meta['ycoords'][1]))

        if not (data_ex[1] > data_ex[0] and data_ey[1] > data_ey[0]):
            raise ValueError('Two data must overlap')
        # earth distance from new object bottom left to the origin(0,0)
        offset = (data_ex[0], data_ey[0])

        # get resolution from object
        resolution = self.meta['resolution']

        # earth coords without offset
        data_ex_offset = (data_ex[0]-offset[0], data_ex[1]-offset[0])
        data_ey_offset = (data_ey[0]-offset[1], data_ey[1]-offset[1])
        self_ex_offset = (self.meta['xcoords'][0]-offset[0],
                          self.meta['xcoords'][1]-offset[0])
        self_ey_offset = (self.meta['ycoords'][0]-offset[1],
                          self.meta['ycoords'][1]-offset[1])
        another_ex_offset = (another_satmap.meta['xcoords'][0] - offset[0],
                             another_satmap.meta['xcoords'][1] - offset[0])
        another_ey_offset = (another_satmap.meta['ycoords'][0] - offset[1],
                             another_satmap.meta['ycoords'][1] - offset[1])

        # change earth coords to pixel coords
        data_px, data_py = _earth_to_pixel_tuple(data_ex_offset,
                                                 data_ey_offset, resolution)
        self_px, self_py = _earth_to_pixel_tuple(self_ex_offset,
                                                 self_ey_offset, resolution)
        another_px, another_py = _earth_to_pixel_tuple(another_ex_offset,
                                                       another_ey_offset,
                                                       resolution)

        # generate empty subtracted data
        data = np.zeros((data_py[1] - data_py[0], data_px[1] - data_px[0]))
        # find the pixel coordinates of the overlaps on the original data
        self_offset = (max(0, -self_py[0]), max(0, -self_px[0]))
        # import data from origin data into the empty subtracted data
        data = self.data[self_offset[0]:data_py[1] + self_offset[0],
                         self_offset[1]:data_px[1] + self_offset[1]]

        # find the pixel coordinates of the overlaps on another original data
        another_offset = (max(0, -another_py[0]), max(0, -another_px[0]))
        # import data from another_data into the empty subtracted data, and
        # subtract 2 data
        data = data - another_satmap.data[another_offset[0]:data_py[1] +
                                          another_offset[0],
                                          another_offset[1]:data_px[1] +
                                          another_offset[1]]

        # copy the data info from the addend, but update the new coords
        meta = self.meta.copy()
        meta['ycoords'] = data_ey
        meta['xcoords'] = data_ex

        # generate a new SatMap object and return
        new_satmap = type(self)(meta, data)
        # update attributes for new SatMap
        new_satmap.fov = (meta['xcoords'][1] - meta['xcoords'][0],
                          meta['ycoords'][1] - meta['ycoords'][0])
        new_satmap.shape = data.shape
        new_satmap.centre = (
            int((meta['xcoords'][1] + meta['xcoords'][0]) / 2),
            int((meta['ycoords'][1] + meta['ycoords'][0]) / 2))
        new_satmap.extra = True

        return new_satmap

    def mosaic(self, another_satmap, resolution=None, padding=True):
        """ Do the more complex object adding.

        Parameters
        ----------
        another_satmap : SatMap
            Another SatMap object.
        resolution : int, optional
            The resolution of the desired data, by default None.
        padding : bool, optional
            A flag determines whether emtpy space is reserved, by default True.

        Returns
        -------
        SatMap
            A new object that have been added.

        Raises
        ------
        TypeError
            Another_satmap must in SatMap type
        TypeError
            Padding must be True or False
        ValueError
            Two data must overlap
        TypeError
            Resolution must be int type
        ValueError
            Resolution must larger than 0
        """
        if not isinstance(another_satmap, SatMap):
            raise TypeError('Another_satmap must in SatMap type')
        if not isinstance(padding, bool):
            raise TypeError('Padding must be True or False')

        # check whether it is overlap
        data_ex = (max(self.meta['xcoords'][0],
                       another_satmap.meta['xcoords'][0]),
                   min(self.meta['xcoords'][1],
                       another_satmap.meta['xcoords'][1]))
        data_ey = (max(self.meta['ycoords'][0],
                       another_satmap.meta['ycoords'][0]),
                   min(self.meta['ycoords'][1],
                       another_satmap.meta['ycoords'][1]))
        if not (data_ex[1] > data_ex[0] and data_ey[1] > data_ey[0]):
            raise ValueError('Two data must overlap')

        # if the resolution is not specified, choose the smaller resolution
        if resolution is None:
            resolution = min(self.meta['resolution'],
                             another_satmap.meta['resolution'])
        else:
            if isinstance(resolution, int):
                raise TypeError('Resolution must be int type')
            if resolution <= 0:
                raise ValueError('Resolution must larger than 0')

        # rescale the data, up-sampling or down-sampling
        data_self = transform.rescale(self.data, self.meta['resolution']/resolution)
        data_another = transform.rescale(another_satmap.data, another_satmap.meta['resolution']/resolution)

        # copy the data info from the addend, but update the new resolution
        meta_self = self.meta.copy()
        meta_self['resolution'] = resolution
        # generate a new SatMap object
        setmap_self = type(self)(meta_self, data_self)

        # copy the data info from the addend, but update the new resolution
        meta_another = another_satmap.meta.copy()
        meta_another['resolution'] = resolution
        # generate a new SatMap object
        setmap_another = type(another_satmap)(meta_another, data_another)

        # if padding, call the __add__ function
        if padding:
            setmap = setmap_self + setmap_another
        # if without padding, generate the max non-empty data
        else:
            # mosaic added with padding=True
            setmap_padding = setmap_self + setmap_another

            # get the intersection coords
            intersect_coords_x = (max(setmap_self.meta['xcoords'][0],
                                      setmap_another.meta['xcoords'][0]),
                                  min(setmap_self.meta['xcoords'][1],
                                      setmap_another.meta['xcoords'][1]))
            intersect_coords_y = (max(setmap_self.meta['ycoords'][0],
                                      setmap_another.meta['ycoords'][0]),
                                  min(setmap_self.meta['ycoords'][1],
                                      setmap_another.meta['ycoords'][1]))
            # earth distance from new object bottom left to the origin(0,0)
            offset = (setmap_padding.meta['xcoords'][0],
                      setmap_padding.meta['ycoords'][0])

            data_ex_offset = (intersect_coords_x[0]-offset[0],
                              intersect_coords_x[1]-offset[0])
            data_ey_offset = (intersect_coords_y[0]-offset[1],
                              intersect_coords_y[1]-offset[1])
            added_ex_offset = (setmap_padding.meta['xcoords'][0]-offset[0],
                               setmap_padding.meta['xcoords'][1]-offset[0])
            added_ey_offset = (setmap_padding.meta['ycoords'][0]-offset[1],
                               setmap_padding.meta['ycoords'][1]-offset[1])
            self_ex_offset = (self.meta['xcoords'][0]-offset[0],
                              self.meta['xcoords'][1]-offset[0])
            self_ey_offset = (self.meta['ycoords'][0]-offset[1],
                              self.meta['ycoords'][1]-offset[1])
            another_ex_offset = (another_satmap.meta['xcoords'][0]-offset[0],
                                 another_satmap.meta['xcoords'][1]-offset[0])
            another_ey_offset = (another_satmap.meta['ycoords'][0]-offset[1],
                                 another_satmap.meta['ycoords'][1]-offset[1])

            # change earth coords to pixel coords
            data_px, data_py = _earth_to_pixel_tuple(data_ex_offset,
                                                     data_ey_offset,
                                                     resolution)
            added_px, added_py = _earth_to_pixel_tuple(added_ex_offset,
                                                       added_ey_offset,
                                                       resolution)
            self_px, self_py = _earth_to_pixel_tuple(self_ex_offset,
                                                     self_ey_offset,
                                                     resolution)
            another_px, another_py = _earth_to_pixel_tuple(another_ex_offset,
                                                           another_ey_offset,
                                                           resolution)

            # 4 conditions. and shape=['pixel_xcoords', 'pixel_ycoords'] of
            # each condition.
            # shape_1 is: Intercept the overlap area horizontally in the mosaic
            # added data
            # shape_2 is: Intercept the overlap area vertically in the mosaic
            # added data
            # shape_3 is: The 'self.data' is the largest after up-sampling or
            # down-sampling
            # shape_4 is: The 'another_satmap.data' is the largest after
            # up-sampling or down-sampling
            shape_1 = [data_px, added_py]
            shape_2 = [added_px, data_py]
            shape_3 = [self_px, self_py]
            shape_4 = [another_px, another_py]
            # list of 4 condition coords
            shape = [shape_1, shape_2, shape_3, shape_4]

            # get the index of maximum area by multiplying the length and width
            # of the data
            index = np.argmax(np.array(
                [(shape[i][0][1] - shape[i][0][0]) *
                 (shape[i][1][1] - shape[i][1][0])
                 for i in range(len(shape))]))

            # get the coords of max area
            max_coords_x = shape[index][0]
            max_coords_y = shape[index][1]

            # import data from mosaic added data into the non-empty mosaic
            # added data
            data = setmap_padding.data[max_coords_y[0]:max_coords_y[1],
                                       max_coords_x[0]:max_coords_x[1]]

            # change the pixel coords to the earth coords
            earth_xcoords, earth_ycoords = _pixel_to_earth_tuple(max_coords_x,
                                                                 max_coords_y,
                                                                 resolution)

            # copy the data info from the addend, but update the new coords
            meta = setmap_self.meta.copy()
            meta['xcoords'] = (earth_xcoords[0] + offset[0],
                               earth_xcoords[1] + offset[0])
            # meta['ycoords'] = (offset[1] - earth_ycoords[1],
            # offset[1] - earth_ycoords[0])
            meta['ycoords'] = (earth_ycoords[0] + offset[1],
                               earth_ycoords[1] + offset[1])

            # generate a new SatMap object and return
            setmap = type(self)(meta, data)

            # update attributes for new SatMap
            setmap.fov = (meta['xcoords'][1] - meta['xcoords'][0],
                          meta['ycoords'][1] - meta['ycoords'][0])
            setmap.shape = data.shape
            setmap.centre = (
                ((meta['xcoords'][1] + meta['xcoords'][0]) // 2),
                ((meta['ycoords'][1] + meta['ycoords'][0]) // 2))
        setmap.extra = True
        return setmap

    def visualise(self, save=False, save_path=''):
        """ Visualise the data.

        Parameters
        ----------
        save : bool, optional
            Choose plot the figure or show the figure, by default False.
        save_path : str, optional
            The path figure saved, by default ''.

        Raises
        ------
        TypeError
            Save must in bool type
        TypeError
            Save_path must be a str
        """
        if not isinstance(save, bool):
            raise TypeError('Save must in bool type')
        if not isinstance(save_path, str):
            raise TypeError('Save_path must be a str')
        plt.imshow(self.data, origin='lower',
                   extent=[self.meta['xcoords'][0], self.meta['xcoords'][1],
                           self.meta['ycoords'][0], self.meta['ycoords'][1]])
        if self.extra:
            extra = '_extra'
        else:
            extra = ''
        date_time = self.meta['obs_date'].split(' ')
        date = ''.join(date_time[0].split('-'))
        time = ''.join(date_time[1].split(':'))
        filename = str(self.meta['observatory']) + '_' + str(
            self.meta['instrument']) + '_' + date + '_' + time + extra + '.png'
        if save:
            plt.savefig(os.path.join(save_path, filename))
        else:
            plt.show()


class Lir(SatMap):
    pass


class Manannan(SatMap):
    pass


class Fand(SatMap):
    pass
