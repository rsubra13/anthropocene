"""
The :mod:`.classes` package provides the three most fundamental classes for
working with bibliographic data in anthropocene: the :class:`.Paper`\, the
:class:`.Corpus`\, and the :class:`.GraphCollection`\.

Classes for models can be found in :mod:`.model`\. Persistent classes (e.g. for 
data archiving) can be found in :mod:`.persistence`\.

.. autosummary::

   paper

"""

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('ERROR')

from paper import Paper,KeyPaper

