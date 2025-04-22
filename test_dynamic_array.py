import math
import pytest # Import pytest for potential fixture usage if needed
from hypothesis import given, strategies as st, settings, assume
from typing import Any, List

from dynamic_array import DynamicArray

# Helper strategy to generate lists with comparable types for testing
# Excludes NaN by default unless explicitly handled, as NaN!=NaN complicates direct list comparison
comparable_st = st.one_of(st.integers(), st.text(), st.booleans(), st.none(),
                          st.floats(allow_nan=False, allow_infinity=False))
list_st = st.lists(comparable_st)

# Strategy to build DynamicArray instances from lists
dynamic_array_st = st.builds(lambda lst: DynamicArray.from_list(lst) or DynamicArray(), list_st)


def test_add():
    """Test add() method."""
    arr = DynamicArray()
    arr.add(3)
    assert arr.to_list() == [3]
    arr.add(None)
    arr.add("hello")
    assert arr.to_list() == [3, None, "hello"]


def test_set_get():
    """Test set() and get() methods."""
    arr = DynamicArray()
    arr.add(1)
    arr.set(0, 5)
    assert arr.get(0) == 5
    with pytest.raises(IndexError):
        arr.get(1)
    with pytest.raises(IndexError):
        arr.set(1, 10)


def test_remove():
    """Test remove() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 2, None, 4, None])
    arr.remove(2) # Remove first 2
    assert arr.to_list() == [1, 3, 2, None, 4, None]
    arr.remove(None) # Remove first None
    assert arr.to_list() == [1, 3, 2, 4, None]
    arr.remove(1)
    assert arr.to_list() == [3, 2, 4, None]
    arr.remove(4)
    assert arr.to_list() == [3, 2, None]
    # Test removing non-existent value (should do nothing)
    arr.remove(99)
    assert arr.to_list() == [3, 2, None]


def test_remove_nan():
    """Test removing NaN values."""
    arr = DynamicArray()
    arr.from_list([1.0, float('nan'), 2.0, float('nan')])
    arr.remove(float('nan'))
    assert len(arr) == 3
    # Check remaining elements carefully due to NaN comparison issues
    remaining = arr.to_list()
    assert remaining[0] == 1.0
    assert remaining[1] == 2.0
    assert isinstance(remaining[2], float) and math.isnan(remaining[2])


def test_len():
    """Test __len__() method."""
    arr = DynamicArray()
    assert len(arr) == 0
    arr.add(1)
    arr.add(2)
    assert len(arr) == 2
    arr.remove(1)
    assert len(arr) == 1


def test_member():
    """Test member() method."""
    arr = DynamicArray()
    arr.add(3)
    arr.add(None)
    arr.add(float('nan'))
    assert arr.member(3) is True
    assert arr.member(5) is False
    assert arr.member(None) is True
    assert arr.member(float('nan')) is True
    assert arr.member(float('inf')) is False


def test_reverse():
    """Test reverse() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, None, 5])
    arr.reverse()
    assert arr.to_list() == [5, None, 3, 2, 1]
    arr.reverse()
    assert arr.to_list() == [1, 2, 3, None, 5]
    # Test reversing empty and single-element arrays
    empty_arr = DynamicArray()
    empty_arr.reverse()
    assert empty_arr.to_list() == []
    single_arr = DynamicArray()
    single_arr.add(10)
    single_arr.reverse()
    assert single_arr.to_list() == [10]


def test_filter():
    """Test filter() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 4, None, 5, 6])
    arr.filter(lambda x: isinstance(x, int) and x % 2 == 0)
    assert arr.to_list() == [2, 4, 6]
    # Test filtering that results in empty array
    arr.filter(lambda x: x > 100)
    assert arr.to_list() == []


def test_map():
    """Test map() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.map(lambda x: x * 2 if isinstance(x, int) else x)
    assert arr.to_list() == [2, 4, 6]
    arr.map(str)
    assert arr.to_list() == ["2", "4", "6"]


def test_reduce():
    """Test reduce() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 4])
    assert arr.reduce(lambda acc, x: acc + x, 0) == 10
    assert arr.reduce(lambda acc, x: acc * x, 1) == 24
    # Test with initial value
    assert arr.reduce(lambda acc, x: acc + str(x), "Numbers: ") == "Numbers: 1234"
    # Test on empty array
    empty_arr = DynamicArray()
    assert empty_arr.reduce(lambda acc, x: acc + x, 100) == 100


def test_none_values():
    """Test storing and retrieving None values."""
    arr = DynamicArray()
    arr.add(None)
    assert arr.get(0) is None
    assert len(arr) == 1
    arr.set(0, 1)
    arr.add(None)
    assert arr.to_list() == [1, None]
    assert arr.member(None) is True
    arr.remove(None)
    assert arr.to_list() == [1]
    assert arr.member(None) is False


def test_mixed_types():
    """Test storing elements of different types."""
    arr = DynamicArray()
    arr.add(1)        # Integer
    arr.add("hello")  # String
    arr.add(3.14)     # Float
    arr.add(None)     # None
    arr.add(True)     # Boolean
    assert arr.to_list() == [1, "hello", 3.14, None, True]
    assert len(arr) == 5
    assert arr.get(1) == "hello"
    assert arr.get(3) is None


def test_equality():
    """Test __eq__ method."""
    arr1 = DynamicArray()
    arr1.from_list([1, 2, 3])
    arr2 = DynamicArray()
    arr2.from_list([1, 2, 3])
    arr3 = DynamicArray()
    arr3.from_list([1, 2, 4])
    arr4 = DynamicArray()
    arr4.from_list([1, 2])

    assert arr1 == arr2
    assert arr1 != arr3
    assert arr1 != arr4
    assert arr1 != [1, 2, 3] # Compare with different type

    # Test with NaN
    arr_nan1 = DynamicArray()
    arr_nan1.from_list([1.0, float('nan')])
    arr_nan2 = DynamicArray()
    arr_nan2.from_list([1.0, float('nan')])
    arr_nan3 = DynamicArray()
    arr_nan3.from_list([1.0, 2.0])

    assert arr_nan1 == arr_nan2
    assert arr_nan1 != arr_nan3


# --- Monoid Law Tests ---

def test_monoid_identity_empty():
    """Test Monoid identity element (empty())."""
    assert DynamicArray.empty().to_list() == []
    assert len(DynamicArray.empty()) == 0


@settings(max_examples=200)
@given(list_st)
def test_pbt_monoid_identity_law(lst: List[Any]):
    """Property-based test for Monoid identity law (a • e = a and e • a = a)."""
    # Create array from list
    arr = DynamicArray()
    arr.from_list(lst)

    # Test a • e = a
    arr_copy_left = arr.copy()
    empty_arr = DynamicArray.empty()
    arr_copy_left.concat(empty_arr) # arr_copy_left is modified
    assert arr_copy_left == arr, f"Identity law (left) failed: {arr_copy_left} != {arr}"

    # Test e • a = a
    arr_copy_right = arr.copy()
    empty_arr_concat = DynamicArray.empty()
    empty_arr_concat.concat(arr_copy_right) # empty_arr_concat is modified
    assert empty_arr_concat == arr, f"Identity law (right) failed: {empty_arr_concat} != {arr}"


@settings(max_examples=100)
@given(list_st, list_st, list_st)
def test_pbt_monoid_associativity_law(list_a: List[Any], list_b: List[Any], list_c: List[Any]):
    """Property-based test for Monoid associativity law (a • b) • c = a • (b • c)."""
    a = DynamicArray(); a.from_list(list_a)
    b = DynamicArray(); b.from_list(list_b)
    c = DynamicArray(); c.from_list(list_c)

    # Calculate (a • b) • c
    ab = a.copy()
    ab.concat(b) # ab = a • b
    ab_c = ab.copy()
    ab_c.concat(c) # ab_c = (a • b) • c

    # Calculate a • (b • c)
    bc = b.copy()
    bc.concat(c) # bc = b • c
    a_bc = a.copy()
    a_bc.concat(bc) # a_bc = a • (b • c)

    assert ab_c == a_bc, f"Associativity failed:\n(a.b).c = {ab_c.to_list()}\na.(b.c) = {a_bc.to_list()}"


# --- Original Hypothesis Test (Adapted) ---

# Strategy for potentially problematic values including NaN
mixed_st = st.one_of(st.integers(), st.text(),
                     st.floats(allow_nan=True, allow_infinity=False), # Allow NaN, exclude Inf
                     st.booleans(), st.none())
list_mixed_st = st.lists(mixed_st)

@settings(max_examples=500, deadline=None) # Increase examples and remove deadline if slow
@given(list_mixed_st)
def test_hypothesis_from_list_to_list(lst: List[Any]):
    """Test property-based input with Hypothesis, focusing on from_list/to_list roundtrip."""
    arr = DynamicArray()
    arr.from_list(lst)

    # Ensure the list representation matches the original list (handle NaN)
    retrieved_list = arr.to_list()
    assert len(retrieved_list) == len(lst), "Lengths do not match"

    for i in range(len(lst)):
        original = lst[i]
        retrieved = retrieved_list[i]
        if isinstance(original, float) and math.isnan(original):
            assert isinstance(retrieved, float) and math.isnan(retrieved), \
                f"NaN mismatch at index {i}"
        else:
            assert original == retrieved, \
                f"Value mismatch at index {i}: expected {original}, got {retrieved}"

    # Ensure the length reported by __len__ matches
    assert len(arr) == len(lst), "Length from __len__ does not match"

    # Check each element individually using get() (handle NaN)
    for i in range(len(lst)):
        element = lst[i]
        retrieved_element = arr.get(i)

        if isinstance(element, float) and math.isnan(element):
            assert isinstance(retrieved_element, float) and math.isnan(retrieved_element), \
                f"NaN mismatch via get() at index {i}"
        else:
            assert retrieved_element == element, \
                f"Value mismatch via get() at index {i}: expected {element}, got {retrieved_element}"
