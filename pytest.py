import pytest
import hello
def test_add():
    a = 1
    b = 2
    assert(hello.add(a,b)==3)