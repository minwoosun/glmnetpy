import logging
import warnings

from typing import Literal
from dataclasses import (dataclass,
                         field)
   
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import check_X_y

from .gaussnet import FastNetMixin
from .docstrings import (make_docstring,
                         add_dataclass_docstring)

from ._fishnet import fishnet as fishnet_dense
from ._fishnet import spfishnet as fishnet_sparse

@dataclass
class FishNet(FastNetMixin):

    univariate_beta: bool = True
    type_logistic: Literal['Newton', 'modified_Newton'] = 'Newton'
    _dense = fishnet_dense
    _sparse = fishnet_sparse

    # private methods

    def _check(self, X, y):

        if np.any(y < 0):
            raise ValueError("negative responses encountered;  not permitted for Poisson family")
        return super()._check(X, y)

    def _wrapper_args(self,
                      design,
                      y,
                      sample_weight,
                      offset,
                      exclude=[]):
        
        if offset is None:
            offset = 0. * y

        _args = super()._wrapper_args(design,
                                      y,
                                      sample_weight,
                                      offset,
                                      exclude=exclude)

        _args['g'] = np.asfortranarray(offset.reshape((-1,1)))
        return _args

