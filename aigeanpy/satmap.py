def earth_to_pixel(x, y, offset, resolution):
    # offset is the pixel distance from coordinate xy top left to the origin
    offset = (offset[0] // resolution, offset[1] // resolution)

    # pixel coords, change earth coords to the pixel coords by dividing resolution
    # and move the coords to the origin
    pixel_xcoords = (x[0] // resolution-offset[0], x[1] // resolution-offset[0])
    # Filp the Y-axis to achieve: In the top-left corner and positive y-values going downwards. 
    pixel_ycoords = (abs(y[1] // resolution-offset[1]), abs(y[0] // resolution-offset[1]))

    # return pixel coords, type=tuple
    return (pixel_xcoords, pixel_ycoords)


def pixel_to_earth(Parameters: Parameters_Data_Type) -> Returns_Data_Type:
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


def get_satmap(Parameters: Parameters_Data_Type) -> Returns_Data_Type:
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
    def extract_data(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


class Manannan:
    '''
    Docstring
    '''

    # Extract Manannan data (stored in .hdf5 file format) using Strategy Pattern
    def extract_data(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


class Fand:
    '''
    Docstring
    '''

    # Extract Fand data [stored in .zipfile(.npy, .json) file format] using Strategy Pattern
    def extract_data(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        '''
        Docstring
        '''

        ...
        raise NotImplementedError


class SatMap:
    def __init__(self, meta, data, shape, fov, centre):
        self.meta = meta
        self.data = data
        self.shape = shape
        self.fov = fov
        self.centre = centre

    def __add__(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        # For collating the two SatMap objects’ data?
        pass

    def __sub__(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        # For subtracting the two SatMap objects’ data?
        pass

    def mosaic(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        '''
        Docstring
        '''

        ...
        raise NotImplementedError

    def visualise(self, Parameters: Parameters_Data_Type) -> Returns_Data_Type:
        '''
        Docstring
        '''

        ...
        raise NotImplementedError

    def __str__(self) -> Returns_Data_Type:
        # For printing object information
        # using >>> print(SatMap object)?
        pass
