import io
import json
import zipfile
import numpy as np
import requests
import h5py
import asdf
from pathlib import Path
from skimage import transform


def earth_to_pixel(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


def pixel_to_earth(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


def get_satmap(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError

def meta_generate(meta_origin):
    """generate meta data

    Parameters
    ----------
    meta_origin : dict
        a dict with multiple informations

    Returns
    -------
    dict
        a dict including info of data. keys including ('archive','instrument','observatory','resolution','xcoords','ycoords','obs_time')
    """    
    meta = {}
    # meta contain following keys
    meta_list = ['archive','instrument','observatory','resolution','xcoords','ycoords']
    for key in meta_list:
        # update the information to the meta
        try:
            meta.update({key:meta_origin[key]})
        # update with an empty value if the file do not contain the key
        except:
            meta.update({key:''})

    # change coords into tuple, the type of each element is int
    meta['xcoords'] = tuple(map(int,meta['xcoords']))
    meta['ycoords'] = tuple(map(int,meta['ycoords']))
    # combine the date and time
    meta.update({'obs_date':meta_origin['date']+' '+meta_origin['time']})
    return meta

class FileFormatter:
    def __init__(self, url):
        self.url = url

    def download_file(self, path):
        response = requests.get(self.url, allow_redirects=True)
        path = Path(path)
        path.write_bytes(response.content)

    def format_file_values(self, key_value_pair):
        return {
                "instrument": key_value_pair["instrument"], 
                "observatory": key_value_pair["observatory"],
                "resolution": key_value_pair["resolution"], 
                "xcoords": key_value_pair["xcoords"],
                "ycoords": key_value_pair["ycoords"], 
                "obs_time": key_value_pair["time"]
            }

    def extract_data(self):
        raise NotImplementedError


class Lir(FileFormatter):
    '''
    Docstring
    '''
    # Extract Lir data (stored in .asdf file format) using Strategy Pattern
    def extract_data(self) -> SatMap:
        '''
        Docstring
        '''

        self.download_file("test.asdf")
        with asdf.open("test.asdf") as f:
            meta = self.format_file_values(f)
            dataset = np.array(f["data"])
            return SatMap(meta, dataset)


class Manannan(FileFormatter):
    '''
    Docstring
    '''

    # Extract Manannan data (stored in .hdf5 file format) using Strategy
    # Pattern
    def extract_data(self) -> SatMap:
        '''
        Docstring
        '''

        self.download_file("test.hdf5")
        with h5py.File("test.hdf5", "r") as f:
            attributes = f["observation"].attrs
            dataset = np.array(f['observation'].get("data"))
            meta = self.format_file_values(attributes)
            
            return SatMap(meta, dataset)

            
class Fand(FileFormatter):
    '''
    Docstring
    '''

    # Extract Fand data [stored in .zipfile(.npy, .json) file format] using
    # Strategy Pattern
    def extract_data(self) -> SatMap:
        '''
        Docstring
        '''
        self.download_file("test.zip")
        with zipfile.ZipFile("test.zip", "r") as files:
            meta = self.format_file_values(json.loads(files.read("metadata.json")))
            dataset = np.load(io.BytesIO(files.read("observation.npy")))
            return SatMap(meta, dataset)


class SatMap:
    def __init__(self, meta, data):
        """initial

        Args:
            meta (dict): including info of data. keys including ('archive','instrument','observatory','resolution','xcoords','ycoords','obs_time')
            data (ndarray): data
        """
        self.meta = meta
        self.data = data
        self.fov = (meta['xcoords'][1] - meta['xcoords'][0], meta['ycoords'][1] - meta['ycoords'][0])
        self.shape = data.shape
        self.centre = (int((meta['xcoords'][1] + meta['xcoords'][0])/2), int((meta['ycoords'][1] + meta['ycoords'][0])/2))
        
    def __add__(self,another_satmap):
        """do the object adding

        Args:
            another_satmap (SatMap): another satmap object

        Raises:
            ValueError: if the 2 satmap have different resolution, raise error

        Returns:
            SatMap: a new object that have been added
        """        
        if self.meta['resolution'] != another_satmap.meta['resolution']:
            raise ValueError('Different instrument cannot be added')

        # earth coords of the new object
        data_coords_x = (min(self.meta['xcoords'][0], another_satmap.meta['xcoords'][0]),max(self.meta['xcoords'][1], another_satmap.meta['xcoords'][1]))
        data_coords_y = (min(self.meta['ycoords'][0], another_satmap.meta['ycoords'][0]),max(self.meta['ycoords'][1], another_satmap.meta['ycoords'][1]))
        # earth distance from new object top left to the origin(0,0)
        offset = (data_coords_x[0],data_coords_y[1])
        # get resolution from object
        resolution =  self.meta['resolution']
        
        # change earth coords to pixel coords
        pixel_data_x, pixel_data_y = earth_to_pixel(data_coords_x, data_coords_y, offset, resolution)
        pixel_self_x, pixel_self_y = earth_to_pixel(self.meta['xcoords'], self.meta['ycoords'], offset, resolution)
        pixel_another_x, pixel_another_y = earth_to_pixel(another_satmap.meta['xcoords'], another_satmap.meta['ycoords'], offset, resolution)

        # generate empty added data
        data_1 = np.zeros((pixel_data_y[1]-pixel_data_y[0], pixel_data_x[1]-pixel_data_x[0]))
        data_2 = np.zeros((pixel_data_y[1]-pixel_data_y[0], pixel_data_x[1]-pixel_data_x[0]))
        # import data from 2 data into the empty added data
        data_1[pixel_self_y[0]:pixel_self_y[1], pixel_self_x[0]:pixel_self_x[1]] = self.data
        data_2[pixel_another_y[0]:pixel_another_y[1], pixel_another_x[0]:pixel_another_x[1]] = another_satmap.data
        data = data_1 + data_2

        # copy the data info from the addend, but update the new coords
        meta = self.meta.copy()
        meta['ycoords'] = data_coords_y
        meta['xcoords'] = data_coords_x

        # generate a new SatMap object and return
        setmap  = type(self)(meta, data)
        return setmap

    def __sub__(self, another_satmap):
        """do the object subtract

        Args:
            another_satmap (SatMap): another satmap object

        Raises:
            ValueError: _description_

        Returns:
            SatMap: a new object that have been added
        """     
        # earth coords of the new object
        data_coords_x = (max(self.meta['xcoords'][0], another_satmap.meta['xcoords'][0]),min(self.meta['xcoords'][1], another_satmap.meta['xcoords'][1]))
        data_coords_y = (max(self.meta['ycoords'][0], another_satmap.meta['ycoords'][0]),min(self.meta['ycoords'][1], another_satmap.meta['ycoords'][1]))
        # earth distance from new object top left to the origin(0,0)
        offset = (data_coords_x[0],data_coords_y[1])
        # get resolution from object
        resolution =  self.meta['resolution']
        
        # change earth coords to pixel coords
        pixel_data_x, pixel_data_y = earth_to_pixel(data_coords_x, data_coords_y, offset, resolution)
        pixel_self_x, pixel_self_y = earth_to_pixel(self.meta['xcoords'], self.meta['ycoords'], offset, resolution)
        pixel_another_x, pixel_another_y = earth_to_pixel(another_satmap.meta['xcoords'], another_satmap.meta['ycoords'], offset, resolution)

        # generate empty subtracted data
        data = np.zeros((pixel_data_y[1]-pixel_data_y[0], pixel_data_x[1]-pixel_data_x[0]))
        # find the pixel coordinates of the overlaps on the original data
        self_offset = (max(0,-pixel_self_y[0]), max(0,-pixel_self_x[0]))
        # import data from origin data into the empty subtracted data
        data = self.data[self_offset[0]:pixel_data_y[1]+self_offset[0], self_offset[1]:pixel_data_x[1]+self_offset[1]]

        # find the pixel coordinates of the overlaps on another original data
        another_offset = (max(0,-pixel_another_y[0]), max(0,-pixel_another_x[0]))
        # import data from another_data into the empty subtracted data, and subtract 2 data
        data = data - another_satmap.data[another_offset[0]:pixel_data_y[1]+another_offset[0], another_offset[1]:pixel_data_x[1]+another_offset[1]]

        # copy the data info from the addend, but update the new coords
        meta = self.meta.copy()
        meta['ycoords'] = data_coords_y
        meta['xcoords'] = data_coords_x

        # generate a new SatMap object and return
        setmap  = type(self)(meta, data)
        return setmap

    def mosaic(self,another_satmap,resolution=None,padding=True):
        """do the more complex object adding

        Args:
            another_satmap (SatMap): another satmap object
            resolution (int, optional): the resolution of the desired data. Defaults to None.
            padding (bool, optional): a flag determines whether emtpy space is reserved. Defaults to True.

        Returns:
            SatMap: a new object that have been added
        """      
        # if the resolution is not specified, choose the smaller resolution
        if resolution == None:
            resolution = min(self.meta['resolution'], another_satmap.meta['resolution'])

        # rescale the data, and use different function for up-sampling and down-sampling
        if resolution <self.meta['resolution']:
            data_self = transform.rescale(self.data, self.meta['resolution']/resolution)
        else:
            data_self = transform.downscale_local_mean(self.data, resolution//self.meta['resolution'])
        if resolution < another_satmap.meta['resolution']:
            data_another = transform.rescale(another_satmap.data, another_satmap.meta['resolution']/resolution)
        else:
            data_another = transform.downscale_local_mean(another_satmap.data, resolution//another_satmap.meta['resolution'])

        # copy the data info from the addend, but update the new resolution
        meta_self = self.meta.copy()
        meta_self['resolution'] = resolution
        # generate a new SatMap object
        setmap_self  = type(self)(meta_self, data_self)

        # copy the data info from the addend, but update the new resolution
        meta_another = another_satmap.meta.copy()
        meta_another['resolution'] = resolution
        # generate a new SatMap object
        setmap_another  = type(another_satmap)(meta_another, data_another)

        # if padding, call the __add__ function
        if padding:
            setmap = setmap_self + setmap_another

        # if without padding, generate the max non-empty data
        else:
            setmap_padding = setmap_self + setmap_another
            intersect_coords_x = (max(self.meta['xcoords'][0], another_satmap.meta['xcoords'][0]),min(self.meta['xcoords'][1], another_satmap.meta['xcoords'][1]))
            intersect_coords_y = (max(self.meta['ycoords'][0], another_satmap.meta['ycoords'][0]),min(self.meta['ycoords'][1], another_satmap.meta['ycoords'][1]))
        
        return setmap

    def visualise(self,
                  _parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
        '''
        Docstring
        '''

        ...
        raise NotImplementedError

    def __str__(self) -> 'Returns_Data_Type':
        # For printing object information
        # using >>> print(SatMap object)?
        pass
