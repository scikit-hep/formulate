# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from formulate.__main__ import parse_args


def test_root2numexpr_conversion():
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A)', '--to-numexpr'])
    assert result == '(A & B) | sqrt(A)'


def test_numexpr2root_conversion():
    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A)', '--to-root'])
    assert result == '(A && B) || TMath::Sqrt(A)'


def test_get_variables():
    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A) + 5.4**3.141592 ', '--variables'])
    assert result == 'A\nB'
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A) + 5.4**pi', '--variables'])
    assert result == 'A\nB'


def test_get_named_constants():
    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A)', '--named-constants'])
    assert result == ''
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A)', '--named-constants'])
    assert result == ''

    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A) + 5.4**3.141592', '--named-constants'])
    assert result == ''
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A) + 5.4**pi', '--named-constants'])
    assert result == 'PI'


def test_get_unnamed_constants():
    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A)', '--unnamed-constants'])
    assert result == ''
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A)', '--unnamed-constants'])
    assert result == ''

    result = parse_args(['--from-numexpr', '(A & B) | sqrt(A) + 5.4**3.141592', '--unnamed-constants'])
    assert result == '5.4\n3.141592'
    result = parse_args(['--from-root', '(A && B) || TMath::Sqrt(A) + 5.4**pi', '--unnamed-constants'])
    assert result == '5.4'


def test_invalid_args():
    with pytest.raises(SystemExit):
        parse_args(['--dsadasdsada'])
