# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from formulate.__main__ import parse_args


def test_basic():
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A)', '--to-numexpr'])
    assert result == '(A & B) | sqrt(A)'

    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A)', '--to-root'])
    assert result == '(A && B) || TMath::Sqrt(A)'


def test_invalid_args():
    with pytest.raises(SystemExit):
        parse_args(['--dsadasdsada'])
