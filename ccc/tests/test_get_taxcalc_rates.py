import numpy as np
import pytest
from ccc import get_taxcalc_rates as tc
from ccc.parameters import Specification


def test_get_calculator():
    '''
    Test the get_calculator() function
    '''
    calc1 = tc.get_calculator(True, 2019)
    assert calc1.current_year == 2019


def test_get_rates():
    '''
    Test of the get_rates() functions
    '''
    p = Specification()  # has default tax rates, with should equal TC
    test_dict = tc.get_rates(
        baseline=False, start_year=2019, reform={}, data='cps')
    for k, v in test_dict.items():
        assert(np.allclose(v, p.__dict__[k]))
