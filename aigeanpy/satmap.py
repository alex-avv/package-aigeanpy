def earth_to_pixel(Parameters: Parameters_Data_Type) -> Returns_Data_Type:
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


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
    '''
    Docstring
    '''

    def __init__(self, Parameters):
        if File_Is_From_Lir:
            self.data, self.meta = Lir().extract_data(Parameters)

        elif File_Is_From_Manannan:
            self.data, self.meta = Manannan().extract_data(Parameters)

        elif File_Is_From_Fand:
            self.data, self.meta = Fand().extract_data(Parameters)   

        else:
            raise ValueError("File couldn't be linked to Lir, Manannan or Fand imagers")

        # self.data member variable – npy array
        # self.meta member variable – dictionary

        # self.fov member variable – tuple
        # self.centre member variable – tuple
        # self.shape member variable – tuple

        # self.instrument member variable?
        # self.resolution member variable?
        # self.day member variable?
        # self.observatory member variable?
        raise NotImplementedError

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
