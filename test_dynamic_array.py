import pytest
from dynamic_array import DynamicArray


def test_add():
    """Test add() method."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.add(5)
    arr.add(10)
    assert arr.to_list() == [5, 10]


def test_get_set():
    """Test get() and set() methods."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.add(1)
    arr.add(2)
    arr.set(1, 5)
    assert arr.get(1) == 5
    assert arr.get(0) == 1


def test_handle_none():
    """Test handling of None values."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.add(None)
    arr.add(10)
    assert arr.get(0) is None
    assert arr.get(1) == 10


def test_remove():
    """Test remove() method."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.add(1)
    arr.add(2)
    arr.add(3)
    arr.remove(1)
    assert arr.to_list() == [1, 3]


def test_iter():
    """Test iteration support."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.add(1)
    arr.add(2)
    arr.add(3)
    elements = [x for x in arr]
    assert elements == [1, 2, 3]
