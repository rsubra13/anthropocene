"""
Description
------------
Reader for Web of Science field-tagged bibliographic data to extract the following fields.

TI - Title of each paper
DE - Keywords of each paper
UT - contains the WOS Id (unique ID) of each paper

Examples:
--------
TI High-precision dendro-C-14 dating of two cedar wood sequences from First
   Intermediate Period and Middle Kingdom Egypt and a small regional

DE Ipi-ha-ishutef; Senusret III; Sesostris III; Senwosret III; Egyptian
   chronology; Radiocarbon-wiggle-matching; Climate change;
   Dendrochronology; Cedar; Dahshur boats

UT WOS:000337013800039

"""

import os
import re
from ..classes import Paper,KeyPaper


# Web of Science functions
def parse(filepath):
    """
    Parse Web of Science field-tagged data.

    Parameters
    ----------
    filepath : string
        Filepath to the Web of Science plain text file.

    Returns
    -------
    wos_list : list
        A list of dictionaries each associated with a paper from the Web of
        Science with keys from docs/fieldtags.txt as encountered in the file;

    Raises
    ------
    KeyError : Key value which needs to be converted to an 'int' is not present.
    AttributeError :
    IOError : File at filepath not found, not readable, or empty.

    """
    wos_list = []

    paper_start_key = 'PT'
    paper_end_key = 'ER'


    #
    line_list = []
    try:
        with open(filepath, 'r') as f:
            line_list = f.read().splitlines()
    except IOError:  # File does not exist, or couldn't be read.
        raise IOError("File does not exist, or cannot be read.")

    if len(line_list) is 0:
        raise IOError("Unable to read filepath or filepath is empty.")
    # Convert the data in the file to a usable list of dictionaries.
    # Note: first two lines of file are not related to any paper therein.
    last_field_tag = paper_start_key  # initialize to something.
    for line in line_list[2:]:

        field_tag = line[:2]

        if field_tag == ' ':
            pass

        if field_tag == paper_start_key:
            # Then prepare for next paper.
            wos_dict = _new_wos_dict()

        if field_tag == paper_end_key:
            # Then add paper to our list.
            wos_list.append(wos_dict)

        # Handle keys like AU,AF,CR that continue over many lines.
        if field_tag == '  ':
            field_tag = last_field_tag

        # Add value for the key to the wos_dict: only for the five tags.
        try:
            if field_tag in ['DE', 'DI', 'TI', 'SO', 'UT','PY']:
                wos_dict[field_tag] += ' ' + str(line[3:])
            # Rest all will just get passed
            else:
                pass

        except (KeyError, TypeError, UnboundLocalError):
            wos_dict[field_tag] = str(line[3:])

        last_field_tag = field_tag
    # End line loop.

    # Define keys that should be lists instead of default string.
    list_keys = ['DE']
    delims = {'DE': ';'}

    # And convert the data at those keys into lists.
    for wos_dict in wos_list:
        for key in list_keys:
            delim = delims[key]
            try:
                key_contents = wos_dict[key]
                if delim != '\n':
                    wos_dict[key] = key_contents.split(delim)
                else:
                    wos_dict[key] = key_contents.splitlines()
            except KeyError:
                # One of the keys to be converted to a list didn't exist.
                pass
            except AttributeError:
                # Again a key didn't exist but it belonged to the wos
                # data_struct set of keys; can't split a None.
                pass

    return wos_list


def convert(wos_data):
    """
    Convert parsed field-tagged data to :class:`.Paper` instances.

    Convert a dictionary or list of dictionaries with keys from the
    Web of Science field tags into a :class:`.Paper` instance or list of
    :class:`.Paper` instances, the standard for anthropocene.
    
    Each :class:`.Paper` is tagged with an accession id for this conversion.

    Parameters
    ----------
    wos_data : list
        A list of dictionaries with keys from the WoS field tags.

    Returns
    -------
    papers : list
        A list of :class:`.Paper` instances.

    Examples
    --------

    .. code-block:: python

       >>> import anthropocene.readers as rd
       >>> wos_list = rd.wos.parse("/Path/to/data.txt")
       >>> papers = rd.wos.convert(wos_list)

    Notes
    -----
    Need to handle author name anomolies (case, blank spaces, etc.) that may
    make the same author appear to be two different authors in Networkx; this is
    important for any graph with authors as nodes.

    """



    # create a Paper for each wos_dict and append to this list
    papers = []
    print "wos_data type" , type(wos_data)
    #handle dict inputs by converting to a 1-item list
    if type(wos_data) is dict:
        print "yes its a dict", type(wos_data)
        wos_data = [wos_data]
        #print 'wos data \n' , wos_data



    # Define the direct relationships between WoS fieldtags and Paper keys.
    translator = _wos2paper_map()
    #print "wos_data::" , wos_data

    # Perform the key convertions
    for wos_dict in wos_data:
        paper = Paper()

        #direct translations
        for key in translator.iterkeys():
            paper[translator[key]] = wos_dict[key]
            #print "how many times"

        papers.append(paper)
    # End wos_dict for loop.

    return papers


def read(datapath):
    """
    Yields a list of :class:`.Paper` instances from a Web of Science data file.

    Parameters
    ----------
    datapath : string
        Filepath to the Web of Science field-tagged data file.

    Returns
    -------
    papers : list
        A list of :class:`.Paper` instances.
        
    Examples
    --------
    
    .. code-block:: python

       >>> import anthropocene.readers as rd
       >>> papers = rd.wos.read("/Path/to/data.txt")

    """
    # Added Try Except 
    try:
        wl = parse(datapath)
        papers = convert(wl)
    except IOError:
        raise IOError("Invalid path.")

    return papers


# [#60462784]
def from_dir(path):
    """
    Convenience function for generating a list of :class:`.Paper` from a
    directory of Web of Science field-tagged data files.

    Parameters
    ----------
    path : string
        Path to directory of field-tagged data files.

    Returns
    -------
    papers : list
        A list of :class:`.Paper` objects.

    Raises
    ------
    IOError
        Invalid path.
        
    Examples
    --------

    .. code-block:: python

       >>> import anthropocene.readers as rd
       >>> papers = rd.wos.from_dir("/Path/to/datadir")        

    """

    wos_list = []

    try:
        files = os.listdir(path)
    except IOError:
        raise IOError("Invalid path.")

    for f in files:
        if not f.startswith('.'):  # Ignore hidden files.
            try:
                wos_list += parse(path + "/" + f)
            except (IOError, UnboundLocalError):  # Ignore files that don't
                pass  # contain WoS data.
    papers = convert(wos_list)
    return papers


def _new_wos_dict():
    """
    Defines the set of field tags that will try to be converted, and intializes
    them to 'None'.

    Returns
    -------
    wos_dict : dict
        A wos_list dictionary with 'None' as default values for all keys.

    """
    wos_dict = {
        'DI': None,
        'TI': None,
        'PY': None,
        'SO': None,
        'UT': None,
        'DE': None,
        }

    return wos_dict


def _wos2paper_map():
    """
    Defines the direct relationships between the wos_dict and :class:`.Paper`.

    Returns
    -------
    translator : dict
        A 'translator' dictionary.

    """
    translator = {
        'DI': 'doi',
        'PY': 'date',
        'TI': 'atitle',
        'SO': 'jtitle',
        'UT': 'wosid',
        'DE': 'keywords'
        }

    return translator


# Custom Error Defined
class DataError(Exception):
    pass
        