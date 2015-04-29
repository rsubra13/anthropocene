"""

"""

import logging
from collections import OrderedDict
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

class Paper(dict):
    """

    Internal Representation of WOS fields.

    ===========     =====   ====================================================
    Field           Type    Description
    ===========     =====   ====================================================
    atitle          str     Article title.
    jtitle          str     Journal title or abbreviated title.
    date            int     Article date of publication.
    doi             str     Digital Object Identifier.
    wosid           str     Web of Science UT fieldtag value.
    ===========     =====   ====================================================

    None values are also allowed for all fields.
    """

    def __init__(self):
        # Default values.
        fields = {
            'aulast':None,
            'auinit':None,
            'auuri':None,
            'atitle':None,
            'jtitle':None,
            'date':None,
            'doi':None,
            'wosid':None,   # ISI Web of Science
            'keywords':None}

        for k,v in fields.iteritems():
            dict.__setitem__(self, k, v)

        # Fields that require list values.
        self.list_fields = [ 'aulast',
                             'auinit',
                             'auuri',
                             'keywords' ]

        # Fields that require string values.
        self.string_fields = [ 'atitle',
                               'jtitle',
                               'doi',
                               'wosid','date']

        # Fields that require int values.
        #self.int_fields = ['date']


    def __setitem__(self, key, value):
        """
        Enforces limited vocabulary of keys and corresponding data types for
        values.
        """

        vt = type(value)
        ks = str(key)


        if key not in self.keys():
            raise KeyError(ks + " is not a valid key in Paper.")
        elif key in self.list_fields and vt is not list and value is not None:
            raise ValueError("Value for field '"+ ks +"' must be a list.")
        elif key in self.string_fields and vt is not str \
                and vt is not unicode and value is not None:
            raise ValueError("Value for field '"+ ks +"' must be a string.")
        # elif key in self.int_fields and vt is not int and value is not None:
        #     raise ValueError("Value for field '"+ ks +"' must be an integer.")
        else:
            dict.__setitem__(self, key, value)


class KeyPaper(dict):
    """

    Internal Representation of WOS fields.

    ===========     =====   ====================================================
    Field           Type    Description
    ===========     =====   ====================================================
    atitle          str     Article title.
    jtitle          str     Journal title or abbreviated title.
    date            int     Article date of publication.
    doi             str     Digital Object Identifier.
    wosid           str     Web of Science UT fieldtag value.
    ===========     =====   ====================================================

    None values are also allowed for all fields.
    """

    def __init__(self):
        # Default values.
        fields = {

           
            'date':None,
            'count':None,
            'keywords':None}

        for k,v in fields.iteritems():
            dict.__setitem__(self, k, v)

        # Fields that require list values.
        #self.list_fields = [ 'keywords' ]

        # Fields that require string values.
        self.string_fields = ['keywords','date']

        # Fields that require int values.
        self.int_fields = ['count']


    def __setitem__(self, key, value):
        """
        Enforces limited vocabulary of keys and corresponding data types for
        values.
        """

        vt = type(value)
        ks = str(key)


        if key not in self.keys():
            raise KeyError(ks + " is not a valid key in KeyPaper.")
        # elif key in self.list_fields and vt is not list and value is not None:
        #     raise ValueError("Value for field '"+ ks +"' must be a list.")
        elif key in self.string_fields and vt is not str \
                and vt is not unicode and value is not None:
            raise ValueError("Value for field '"+ ks +"' must be a string.")
        # elif key in self.int_fields and vt is not int and value is not None:
        #     raise ValueError("Value for field '"+ ks +"' must be an integer.")
        else:
            dict.__setitem__(self, key, value)

