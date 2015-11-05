# Copyright (c) 2012, GPy authors (see AUTHORS.txt).
# Licensed under the BSD 3-clause license (see LICENSE.txt)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from . import core
from . import models
from . import mappings
from . import inference
from . import util
from . import examples
from . import likelihoods
from . import testing
from . import kern
from . import plotting

# backwards compatibility
import sys
backwards_compatibility = ['lists_and_dicts', 'observable_array', 'ties_and_remappings', 'index_operations']
for bc in backwards_compatibility:
    sys.modules['GPy.core.parameterization.{!s}'.format(bc)] = getattr(core.parameterization, bc)


# Direct imports for convenience:
from .core import Model
from .core.parameterization import priors
from paramz import Param, Parameterized, ObsAr, transformations as constraints

from .__version__ import __version__

from numpy.testing import Tester
#@nottest
try:
    #Get rid of nose dependency by only ignoring if you have nose installed
    from nose.tools import nottest
    @nottest
    def tests(verbose=10):
        Tester(testing).test(verbose=verbose)
except:
    def tests(verbose=10):
        Tester(testing).test(verbose=verbose)

def load(file_or_path):
    """
    Load a previously pickled model, using `m.pickle('path/to/file.pickle)'

    :param file_name: path/to/file.pickle
    """
    # This is the pickling pain when changing _src -> src
    import inspect
    sys.modules['GPy.kern._src'] = kern.src  # @UndefinedVariable
    for name, module in inspect.getmembers(kern.src):  # @UndefinedVariable
        if not name.startswith('_'):
            sys.modules['GPy.kern._src.{}'.format(name)] = module
    try:
        import cPickle as pickle
        if isinstance(file_or_path, basestring):
            with open(file_or_path, 'rb') as f:
                m = pickle.load(f)
        else:
            m = pickle.load(file_or_path)
    except: # python3
        import pickle  # @Reimport
        if isinstance(file_or_path, str):
            with open(file_or_path, 'rb') as f:
                u = pickle._Unpickler(f)  # @UndefinedVariable
                u.encoding = 'latin1'
                m = u.load()
        else:
            u = pickle._Unpickler(file_or_path)  # @UndefinedVariable
            u.encoding = 'latin1'
            m = u.load()
    return m
