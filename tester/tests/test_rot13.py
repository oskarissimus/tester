import pytest

from tester.rot13 import rot13

def test_rot13():
    assert rot13('hello') == 'uryyb'
