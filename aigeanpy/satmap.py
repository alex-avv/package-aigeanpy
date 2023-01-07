import numpy as np

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


class Lir:
    '''
    Docstring
    '''

    # Extract Lir data (stored in .asdf file format) using Strategy Pattern
    def extract_data(self, _parameters:
                     'Parameters_Data_Type') -> 'Returns_Data_Type':
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


class Manannan:
    '''
    Docstring
    '''

    # Extract Manannan data (stored in .hdf5 file format) using Strategy
    # Pattern
    def extract_data(self, _parameters:
                     'Parameters_Data_Type') -> 'Returns_Data_Type':
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


class Fand:
    '''
    Docstring
    '''

    # Extract Fand data [stored in .zipfile(.npy, .json) file format] using
    # Strategy Pattern
    def extract_data(self, _parameters:
                     'Parameters_Data_Type') -> 'Returns_Data_Type':
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


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

    def mosaic(self,
               _parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
        '''
        Docstring
        '''

        ...
        raise NotImplementedError

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
