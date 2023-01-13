import numpy as np
from skimage import transform

def earth_to_pixel_tuple(x, y, resolution):
    """change earth coordinate to pixel coordinate

    Parameters
    ----------
    x : tuple
        earth coordinate, xcoords
    y : tuple
        earth coordinate, ycoords
    resolution : int
        data resolution

    Returns
    -------
    tuple
        pixel coordinate, xcoords
    tuple
        pixel coordinate, ycoords. Positive y-values going downwards
    """    
    # change earth coords to the pixel coords by dividing resolution and move the coords to the origin
    pixel_xcoords = (earth_to_pixel(x[0], y[0], resolution)[0], earth_to_pixel(x[1], y[1], resolution)[0])
    # Filp the Y-axis to achieve: In the top-left corner and positive y-values going downwards. 
    pixel_ycoords = (abs(earth_to_pixel(x[1], y[1], resolution)[1]), abs(earth_to_pixel(x[0], y[0], resolution)[1]))
    return pixel_xcoords, pixel_ycoords

def earth_to_pixel(x, y, resolution):
    """change earth coordinate to pixel coordinate

    Parameters
    ----------
    x : int
        earth coordinate, xcoords
    y : int
        earth coordinate, ycoords
    resolution : int
        data resolution

    Returns
    -------
    int
        pixel coordinate, xcoords
    int
        pixel coordinate, ycoords
    """    
    return x//resolution, y//resolution 

def pixel_to_earth_tuple(x, y, resolution):
    """change pixel coordinate to earth coordinate

    Parameters
    ----------
    x : tuple
        pixel coordinate, xcoords
    y : tuple
        pixel coordinate, ycoords
    resolution : int
        data resolution

    Returns
    -------
    tuple
        earth coordinate, xcoords
    tuple
        earth coordinate, ycoords
    """    
    # change earth coords to the pixel coords by dividing resolution and move the coords to the origin
    xcoords = (pixel_to_earth(x[0], y[0], resolution)[0], pixel_to_earth(x[1], y[1], resolution)[0])
    # Filp the Y-axis to achieve: In the top-left corner and positive y-values going downwards. 
    ycoords = (pixel_to_earth(x[0], y[0], resolution)[1], pixel_to_earth(x[1], y[1], resolution)[1])
    return xcoords, ycoords

def pixel_to_earth(x, y, resolution):
    """change pixel coordinate to earth coordinate

    Parameters
    ----------
    x : int
        pixel coordinate, xcoords
    y : int
        pixel coordinate, ycoords
    resolution : int
        data resolution

    Returns
    -------
    int
        earth coordinate, xcoords
    int
        earth coordinate, ycoords
    """    
    return x*resolution, y*resolution


def get_satmap(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


class SatMap:
    def __init__(self, meta, data):
        """initial the SatMap class

        Parameters
        ----------
        meta : dict
            including info of data. keys including ('archive','instrument','observatory','resolution','xcoords','ycoords','obs_time', 'extra')
        data : array
            data
        
        Raises
        ------
        TypeError
            Meta must in dict type
        TypeError
            Data must in np.ndarray type
        """      
        if type(meta) is not dict:
            raise TypeError('Meta must in dict type')
        if type(data) is not np.ndarray:
            raise TypeError('Data must in np.ndarray type')
        self.meta = meta
        self.data = data
        self.fov = (meta['xcoords'][1] - meta['xcoords'][0], meta['ycoords'][1] - meta['ycoords'][0])
        self.shape = data.shape
        self.centre = (int((meta['xcoords'][1] + meta['xcoords'][0])/2), int((meta['ycoords'][1] + meta['ycoords'][0])/2))
        self.extra = False
                  
    def __add__(self,another_satmap):
        """do the object adding

        Parameters
        ----------
        another_satmap : SatMap
            another SatMap object

        Returns
        -------
        SatMap
            a new object that have been added

        Raises
        ------
        error
            _description_
        ValueError
            if the 2 satmap have different resolution, raise error
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
        data = np.zeros((pixel_data_y[1]-pixel_data_y[0], pixel_data_x[1]-pixel_data_x[0]))
        data[pixel_self_y[0]:pixel_self_y[1], pixel_self_x[0]:pixel_self_x[1]] = self.data
        data[pixel_another_y[0]:pixel_another_y[1], pixel_another_x[0]:pixel_another_x[1]] = another_satmap.data

        # copy the data info from the addend, but update the new coords
        meta = self.meta.copy()
        meta['ycoords'] = data_coords_y
        meta['xcoords'] = data_coords_x

        # generate a new SatMap object and return
        setmap  = type(self)(meta, data)
        return setmap

    def __sub__(self, another_satmap):
        """do the object subtract

        Parameters
        ----------
        another_satmap : SatMap
            another SatMap object


        Returns
        -------
        SatMap
            a new object that have been subtracted
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

        Parameters
        ----------
        another_satmap : SatMap
            another SatMap object
        resolution : int, optional
            the resolution of the desired data, by default None
        padding : bool, optional
            a flag determines whether emtpy space is reserved, by default True

        Returns
        -------
        SatMap
            a new object that have been added
        """        
        # if the resolution is not specified, choose the smaller resolution
        if resolution == None:
            resolution = min(self.meta['resolution'], another_satmap.meta['resolution'])

        # rescale the data, but use different function for up-sampling and down-sampling
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
            # mosaic added with padding=True
            setmap_padding = setmap_self + setmap_another
            # get the intersection coords
            intersect_coords_x = (max(setmap_self.meta['xcoords'][0], setmap_another.meta['xcoords'][0]),min(setmap_self.meta['xcoords'][1], setmap_another.meta['xcoords'][1]))
            intersect_coords_y = (max(setmap_self.meta['ycoords'][0], setmap_another.meta['ycoords'][0]),min(setmap_self.meta['ycoords'][1], setmap_another.meta['ycoords'][1]))
            # earth distance from new object top left to the origin(0,0)
            offset = (setmap_padding.meta['xcoords'][0],setmap_padding.meta['ycoords'][1])
            
            # change earth coords to pixel coords
            pixel_data_x, pixel_data_y = earth_to_pixel(intersect_coords_x, intersect_coords_y, offset, resolution)
            pixel_pad_x, pixel_pad_y = earth_to_pixel(setmap_padding.meta['xcoords'], setmap_padding.meta['ycoords'], offset, resolution)
            pixel_self_x, pixel_self_y = earth_to_pixel(setmap_self.meta['xcoords'], setmap_self.meta['ycoords'], offset, resolution)
            pixel_another_x, pixel_another_y = earth_to_pixel(setmap_another.meta['xcoords'], setmap_another.meta['ycoords'], offset, resolution)

            # 4 conditions. and shape=['xcoords', 'ycoords'] of each condition.
            # shape_1 is: Intercept the overlap area horizontally in the mosaic added data
            # shape_2 is: Intercept the overlap area vertically in the mosaic added data
            # shape_3 is: The 'self.data' is the largest after up-sampling or down-sampling
            # shape_4 is: The 'another_satmap.data' is the largest after up-sampling or down-sampling
            shape_1 = [pixel_data_x, pixel_pad_y]
            shape_2 = [pixel_pad_x, pixel_data_y]
            shape_3 = [pixel_self_x, pixel_self_y]
            shape_4 = [pixel_another_x, pixel_another_y]
            # list of 4 condition coords
            shape = [shape_1, shape_2, shape_3, shape_4]
            
            # get the index of maximum area by multiplying the length and width of the data
            index = np.argmax(np.array([(shape[i][0][1]-shape[i][0][0])*(shape[i][1][1]-shape[i][1][0]) for i in range(len(shape))]))
            # get the coords of max area
            max_coords_x = shape[index][0]
            max_coords_y = shape[index][1]

            # import data from mosaic added data into the non-empty mosaic added data
            data = setmap_padding.data[max_coords_y[0]:max_coords_y[1], max_coords_x[0]:max_coords_x[1]]

            # change the pixel coords to the pixel coords
            earth_xcoords, earth_ycoords = earth_to_pixel(max_coords_x, max_coords_y, offset, resolution)

            # copy the data info from the addend, but update the new coords
            meta = setmap_self.meta.copy()
            meta['ycoords'] = earth_ycoords
            meta['xcoords'] = earth_xcoords

            # generate a new SatMap object and return
            setmap  = type(self)(meta, data)
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
