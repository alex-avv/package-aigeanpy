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
        
    def __add__(self,
                _parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
        # For collating the two SatMap objects’ data?
        pass

    def __sub__(self,
                _parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
        # For subtracting the two SatMap objects’ data?
        pass

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
