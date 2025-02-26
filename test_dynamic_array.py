import math

from hypothesis import given, strategies as st

from dynamic_array import DynamicArray


def test_add():
    """Test add() method."""
    arr = DynamicArray()
    arr.add(3)
    assert arr.to_list() == [3]


def test_set_get():
    """Test set() and get() methods."""
    arr = DynamicArray()
    arr.add(1)
    arr.set(0, 5)
    assert arr.get(0) == 5


def test_remove():
    """Test remove() method."""
    arr = DynamicArray()
    arr.add(1)
    arr.add(2)
    arr.add(3)
    arr.remove(2)
    assert arr.to_list() == [1, 3]


def test_size():
    """Test size() method."""
    arr = DynamicArray()
    arr.add(1)
    arr.add(2)
    assert arr.size == 2


def test_member():
    """Test member() method."""
    arr = DynamicArray()
    arr.add(3)
    assert arr.member(3) is True
    assert arr.member(5) is False


def test_reverse():
    """Test reverse() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.reverse()
    assert arr.to_list() == [3, 2, 1]


def test_filter():
    """Test filter() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3, 4])
    arr.filter(lambda x: x % 2 == 0)
    assert arr.to_list() == [2, 4]


def test_map():
    """Test map() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.map(lambda x: x * 2)
    assert arr.to_list() == [2, 4, 6]


def test_reduce():
    """Test reduce() method."""
    arr = DynamicArray()
    arr.from_list([1, 2, 3])
    assert arr.reduce(lambda acc, x: acc + x, 0) == 6


def test_none_values():
    """Test storing and retrieving None values."""
    arr = DynamicArray()
    arr.add(None)
    assert arr.get(0) is None  # Verify None is retrieved correctly
    arr.set(0, 1)
    arr.add(None)
    assert arr.to_list() == [1, None]


def test_monoid_identity():
    """Test Monoid identity element (empty())."""
    arr = DynamicArray()
    assert arr.empty().to_list() == []


def test_mixed_types():
    """Test storing elements of different types."""
    arr = DynamicArray()
    arr.add(1)        # Integer
    arr.add("hello")  # String
    arr.add(3.14)     # Float
    arr.add(None)     # None
    assert arr.to_list() == [1, "hello", 3.14, None]


def test_monoid_associativity():
    """Test Monoid associativity (a • b) • c = a • (b • c)."""
    arr1 = DynamicArray()
    arr1.from_list([1, 2])
    arr2 = DynamicArray()
    arr2.from_list([3])
    arr3 = DynamicArray()
    arr3.from_list([4, 5])

    assert arr1.concat(arr2).concat(arr3).to_list() == \
           arr1.concat(arr2.concat(arr3)).to_list()


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
