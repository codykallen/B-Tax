import os
import tempfile
import pytest
from ccc.parameters import Specification, revision_warnings_errors


def test_create_specification_object():
    spec = Specification()
    assert spec


def test_update_specification_with_dict():
    cyr = 2020
    spec = Specification(year=cyr)
    new_spec_dict = {
        'profit_rate': 0.4,
        'm': 0.5
    }
    spec.update_specification(new_spec_dict)
    assert spec.profit_rate == 0.4
    assert spec.m == 0.5
    assert len(spec.errors) == 0


def test_update_specification_with_json():
    cyr = 2020
    spec = Specification(year=cyr)
    new_spec_json = """
    {
    "profit_rate": [
        {
            "year": 2020,
            "value": 0.4
        }
    ],
    "m": [
        {
            "year": 2020,
            "value": 0.5
        }
    ]
    }
    """
    spec.update_specification(new_spec_json)
    assert spec.profit_rate == 0.4
    assert spec.m == 0.5
    assert len(spec.errors) == 0


def test_update_bad_revision1():
    spec = Specification()
    # profit rate has an upper bound at 1.0
    revs = {
        'profit_rate': [{'year': spec.year, 'value': 1.2}]
    }
    spec.update_specification(revs, raise_errors=False)
    assert len(spec.errors) > 0
    first_line = spec.errors['profit_rate'][0]
    print(first_line)
    expected_first_line =\
        'profit_rate[year=2019] 1.2 > max 1.0 '
    assert first_line == expected_first_line


def test_update_bad_revsions2():
    spec = Specification()
    # Pick a category for depreciation that is out of bounds
    revs = {
        'profit_rate': 0.5,
        'DeprecSystem_3yr': 'not_a_deprec_system'}
    spec.update_specification(revs, raise_errors=False)
    assert len(spec.errors) > 0
    first_line = spec.errors['DeprecSystem_3yr'][0]
    print('First line = ', first_line)
    expected_first_line = (
        'DeprecSystem_3yr "not_a_deprec_system" must be in list of '
        'choices GDS, ADS, Economic.'
    )
    assert first_line == expected_first_line


def test_revision_warnings_errors():
    revs_dict_good = {'profit_rate': [{'year': 2020, 'value': 0.30}]}
    e_w = revision_warnings_errors(revs_dict_good)
    assert len(e_w['warnings']) == 0
    assert len(e_w['errors']) == 0
    revs_dict_bad = {'profit_rate': [{'year': 2020, 'value': -0.10}]}
    e_w = revision_warnings_errors(revs_dict_bad)
    assert len(e_w['warnings']) == 0
    assert len(e_w['errors']) > 0
