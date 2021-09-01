from numpy import rad2deg
from .InsertionHeuristic import *

from .KRegret import *
from .KRegretPDPTW import *

from .RandomInsertion import *
from .RandomInsertionPDPTW import *

from .RemovalHeuristic import *

from .RandomRemoval import *
from .RandomRemovalPDPTW import *

from .WorstRemoval import *
from .WorstRemovalPDPTW import *

from .ShawRemoval import * 
from .ShawRemovalPDPTW import * 

__all__ = [
    "InsertionHeuristic",
    "KRegret",
    "KRegretPDPTW",
    "RandomInsertion",
    "RandomInsertionPDPTW",
    "RemovalHeuristic",
    "RandomRemoval",
    "RandomRemovalPDPTW",
    "WorstRemoval",
    "WorstRemovalPDPTW",
    "ShawRemoval",
    "ShawRemovalPDPTW"
]