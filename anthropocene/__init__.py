"""
Anthropocene is based on Tethne.


"""

from classes import *
from readers import *


import logging
logging.basicConfig(filename=None, format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel('INFO')