import math
import copy
from typing import List

import pytest
from hypothesis import given, strategies as st

from dynamic_array import DynamicArray


def test_add():
    """Test add() method."""
    arr = DynamicArray()
    arr.add(3)
    assert arr.to_list() == [3]
    assert arr.size == 1


def test_set_get():
    """Test set() and get() methods."""
    arr = DynamicArray()
    arr.add(1)
    arr.set(0, 5)
    assert arr.get(0) == 5

    # Test index error
    with pytest.raises(IndexError):
        arr.get(1)

    with pytest.raises(IndexError):
        arr.set(1, 10)


def test_remove():
    """Test remove() method."""
    arr = DynamicArray()
    arr.add(1)
    arr.add(2)
    arr.add(3)
    arr.remove(2)
    assert arr.to_list() == [1, 3]
    assert arr.size == 2

    # Remove non-existent element
    arr.remove(5)
    assert arr.to_list() == [1, 3]
    assert arr.size == 2


def test_size():
    """Test size() method."""
    arr = DynamicArray()
    assert arr.size == 0
    arr.add(1)
    arr.add(2)
    assert arr.size == 2
    assert len(arr) == 2


def test_member():
    """Test member() method."""
    arr = DynamicArray()
    arr.add(3)
    assert arr.member(3) is True
    assert arr.member(5) is False

    # Edge cases
    arr.add(None)
    assert arr.member(None) is True


def test_reverse():
    """Test reverse() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.reverse()
    assert arr.to_list() == [3, 2, 1]

    # Test with even number of elements
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 4])
    arr.reverse()
    assert arr.to_list() == [4, 3, 2, 1]

    # Test with single element
    arr = DynamicArray()
    arr.add(1)
    arr.reverse()
    assert arr.to_list() == [1]

    # Test with empty array
    arr = DynamicArray()
    arr.reverse()
    assert arr.to_list() == []


def test_filter():
    """Test filter() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 4])
    arr.filter(lambda x: x % 2 == 0)
    assert arr.to_list() == [2, 4]

    # Test with all elements matching
    arr = DynamicArray()
    arr.from_list([2, 4, 6])
    arr.filter(lambda x: x % 2 == 0)
    assert arr.to_list() == [2, 4, 6]

    # Test with no elements matching
    arr = DynamicArray()
    arr.from_list([1, 3, 5])
    arr.filter(lambda x: x % 2 == 0)
    assert arr.to_list() == []


def test_map():
    """Test map() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.map(lambda x: x * 2)
    assert arr.to_list() == [2, 4, 6]

    # Test with type transformation
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.map(str)
    assert arr.to_list() == ['1', '2', '3']

    # Test with empty array
    arr = DynamicArray()
    arr.map(lambda x: x * 2)
    assert arr.to_list() == []


def test_reduce():
    """Test reduce() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    assert arr.reduce(lambda acc, x: acc + x, 0) == 6

    # Test with non-numeric values
    arr = DynamicArray()
    arr.from_list(['a', 'b', 'c'])
    assert arr.reduce(lambda acc, x: acc + x, '') == 'abc'

    # Test with empty array
    arr = DynamicArray()
    assert arr.reduce(lambda acc, x: acc + x, 0) == 0


def test_none_values():
    """Test storing and retrieving None values."""
    arr = DynamicArray()
    arr.add(None)
    assert arr.get(0) is None  # Verify None is retrieved correctly
    arr.set(0, 1)
    arr.add(None)
    assert arr.to_list() == [1, None]

    # Test filtering with None
    arr = DynamicArray()
    arr.from_list([1, None, 2, None, 3])
    arr.filter(lambda x: x is not None)
    assert arr.to_list() == [1, 2, 3]


def test_from_to_list():
    """Test from_list and to_list methods."""
    # Empty list
    arr = DynamicArray()
    arr.from_list([])
    assert arr.to_list() == []
    assert arr.size == 0

    # Regular list
    arr = DynamicArray()
    lst = [1, 2, 3, 4, 5]
    arr.from_list(lst)
    assert arr.to_list() == lst
    assert arr.size == len(lst)

    # Large list to test resizing
    arr = DynamicArray(growth_factor=2)
    lst = list(range(100))
    arr.from_list(lst)
    assert arr.to_list() == lst
    assert arr.size == len(lst)


def test_monoid_identity():
    """Test Monoid identity element (empty())."""
    # Identity element with empty array
    arr = DynamicArray()
    empty_arr = DynamicArray.empty()

    # Test left identity
    left_concat = copy.deepcopy(empty_arr)
    left_concat.concat(arr)
    assert left_concat.to_list() == arr.to_list()

    # Test right identity
    right_concat = copy.deepcopy(arr)
    right_concat.concat(empty_arr)
    assert right_concat.to_list() == arr.to_list()

    # Test with non-empty array
    arr = DynamicArray()
    arr.from_list([1, 2, 3])

    left_concat = copy.deepcopy(DynamicArray.empty())
    left_concat.concat(arr)
    assert left_concat.to_list() == [1, 2, 3]

    right_concat = copy.deepcopy(arr)
    right_concat.concat(DynamicArray.empty())
    assert right_concat.to_list() == [1, 2, 3]


def test_mixed_types():
    """Test storing elements of different types."""
    arr = DynamicArray()
    arr.add(1)        # Integer
    arr.add("hello")  # String
    arr.add(3.14)     # Float
    arr.add(None)     # None
    assert arr.to_list() == [1, "hello", 3.14, None]

    # Test operations on mixed types
    arr.reverse()
    assert arr.to_list() == [None, 3.14, "hello", 1]

    # Test filtering on mixed types
    arr = DynamicArray()
    arr.from_list([1, "hello", 3.14, None, 5])
    arr.filter(lambda x: isinstance(x, (int, float)) and x is not None)
    assert arr.to_list() == [1, 3.14, 5]


def test_monoid_associativity():
    """Test Monoid associativity (a • b) • c = a • (b • c)."""
    a = DynamicArray()
    a.from_list([1, 2])

    b = DynamicArray()
    b.from_list([3])

    c = DynamicArray()
    c.from_list([4, 5])

    # (a • b) • c
    left_assoc1 = copy.deepcopy(a)
    left_assoc1.concat(b)
    left_assoc_result = copy.deepcopy(left_assoc1)
    left_assoc_result.concat(c)

    # a • (b • c)
    right_assoc1 = copy.deepcopy(b)
    right_assoc1.concat(c)
    right_assoc_result = copy.deepcopy(a)
    right_assoc_result.concat(right_assoc1)

    assert left_assoc_result.to_list() == right_assoc_result.to_list()
    assert left_assoc_result.to_list() == [1, 2, 3, 4, 5]


def test_iterator():
    """Test iterator functionality."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])

    # Test manual iteration
    it = iter(arr)
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 3
    with pytest.raises(StopIteration):
        next(it)

    # Test for-loop iteration
    result = []
    for item in arr:
        result.append(item)
    assert result == [1, 2, 3]

    # Test with empty array
    arr = DynamicArray()
    it = iter(arr)
    with pytest.raises(StopIteration):
        next(it)


@given(st.lists(st.one_of(st.integers(), st.text(),
                          st.floats(allow_nan=True), st.none())))
def test_hypothesis(lst):
    """Test property-based input with Hypothesis,
    including mixed types and None."""
    arr = DynamicArray()
    arr.from_list(lst)

    # Ensure the list representation matches the original list
    assert arr.to_list() == lst, "Lists do not match"

    # Ensure the length matches
    assert len(arr) == len(lst), "Lengths do not match"

    # Check each element individually
    for i in range(len(lst)):
        element = lst[i]
        retrieved_element = arr.get(i)

        if element is None:
            # Use 'is' for None comparison
            assert retrieved_element is None, \
                (f"Element at index {i} should be None "
                 f"but got {retrieved_element}")
        elif isinstance(element, float) and math.isnan(element):
            # Handle NaN separately
            assert isinstance(retrieved_element, float) and math.isnan(
                retrieved_element), \
                f"Both values should be NaN at index {i}"
        else:
            # For other types, use equality check
            assert retrieved_element == element, \
                (f"Values at index {i} do not match:"
                 f" {retrieved_element} vs {element}")


@given(st.lists(st.integers()),
       st.lists(st.integers()),
       st.lists(st.integers()))
def test_monoid_pbt(lst1, lst2, lst3):
    """Property-based test for Monoid laws."""
    a = DynamicArray()
    a.from_list(lst1)

    b = DynamicArray()
    b.from_list(lst2)

    c = DynamicArray()
    c.from_list(lst3)

    # Test identity element
    empty = DynamicArray.empty()

    left_identity = copy.deepcopy(empty)
    left_identity.concat(a)
    assert left_identity.to_list() == a.to_list(), "Left identity failed"

    right_identity = copy.deepcopy(a)
    right_identity.concat(empty)
    assert right_identity.to_list() == a.to_list(), "Right identity failed"

    # Test associativity
    # (a • b) • c
    ab = copy.deepcopy(a)
    ab.concat(b)
    abc1 = copy.deepcopy(ab)
    abc1.concat(c)

    # a • (b • c)
    bc = copy.deepcopy(b)
    bc.concat(c)
    abc2 = copy.deepcopy(a)
    abc2.concat(bc)

    assert abc1.to_list() == abc2.to_list(), "Associativity failed"


@given(st.lists(st.one_of(st.integers(), st.text(),
                          st.floats(allow_nan=True), st.none())))
def test_concat_pbt(lst):
    """Property-based test for concat operation."""
    # Split the list in two parts
    mid = len(lst) // 2
    first_half = lst[:mid]
    second_half = lst[mid:]

    # Create arrays from the two halves
    arr1 = DynamicArray()
    arr1.from_list(first_half)

    arr2 = DynamicArray()
    arr2.from_list(second_half)

    # Concatenate the arrays
    arr1.concat(arr2)

    # Check the result
    assert arr1.to_list() == lst, "Concatenation failed"
    assert arr1.size == len(lst), "Size after concatenation is incorrect"

    