from numpy import inf
import sys

def unordered_mosaic(satmaps, resolution = None):
    processed = []
    mosaic = None
    
    # Choosing the smallest resolution among the satmap list if not specified
    if not resolution:
        resolution = inf
        for satmap in satmaps:
            if satmap.meta['resolution'] < resolution:
                resolution = satmap.meta['resolution']    
    
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
                    store_err = err
        else:
            # Continuing if inner loop wasn't broken.
            continue
        # Inner loop was broken, breaking outer.
        break

    # Getting mosaic from the rest of satmaps
    if mosaic:
        for n in range(len(satmaps) - 2):  # (n - 2) satmaps to be processed
            for satmap in satmaps:
                if satmap not in processed:
                    try:
                        mosaic = mosaic.mosaic(satmap)
                        processed += [satmap]
                        # Breaking the inner for loop
                        break
                    except Exception as err:
                        store_err = err

    # If at least one of the input files fails, show relevant message. Else
    # return the mosaic.
    if len(processed) != len(satmaps):
        sys.stderr.write("It was not possible to build a mosaic from the "
                         "specified files and resolution. The exception was:"
                         f"\n\n{type(store_err).__name__}: {str(store_err)}")
        sys.exit(1)
    else:
        return mosaic


def today(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


def metadata(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError


def mosaic(_parameters: 'Parameters_Data_Type') -> 'Returns_Data_Type':
    '''
    Docstring
    '''

    ...
    raise NotImplementedError

# Small change in command module
