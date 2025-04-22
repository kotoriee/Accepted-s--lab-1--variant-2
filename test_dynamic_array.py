import math
import copy
import pytest
from hypothesis import given, strategies as st, settings, assume
from typing import List, Any, Callable, TypeVar, cast

from dynamic_array import DynamicArray

# Type variable for generic test functions
T = TypeVar('T')

# Define strategies for different types
int_st = st.integers(min_value=-1000, max_value=1000)
float_st = st.floats(allow_nan=False, allow_infinity=False,
                     min_value=-1000, max_value=1000)
text_st = st.text(max_size=100)
bool_st = st.booleans()
none_st = st.none()

# Create a strategy for basic comparable values
comparable_st = st.one_of(int_st, float_st, text_st, bool_st, none_st)

# Strategy for lists of comparable values
list_st = st.lists(comparable_st, max_size=100)


# Strategy to build DynamicArray instances directly
@st.composite  # type: ignore
def dynamic_array_st(draw: Callable[[st.SearchStrategy[Any]], Any],
                     elements: st.SearchStrategy[Any] 
                     = comparable_st) -> DynamicArray[Any]:
    """Strategy to generate DynamicArray instances."""
    lst = draw(st.lists(elements, max_size=100))
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list(lst)
    return arr


# Basic unit tests
def test_add() -> None:
    """Test add() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.add(3)
    assert arr.to_list() == [3]
    arr.add(None)
    arr.add("hello")
    assert arr.to_list() == [3, None, "hello"]


def test_set_get() -> None:
    """Test set() and get() methods."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.add(1)
    arr.set(0, 5)
    assert arr.get(0) == 5
    with pytest.raises(IndexError):
        arr.get(1)
    with pytest.raises(IndexError):
        arr.set(1, 10)


def test_remove() -> None:
    """Test remove() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list([1, 2, 3, 2, None, 4, None])
    arr.remove(2)  # Remove first 2
    assert arr.to_list() == [1, 3, 2, None, 4, None]
    arr.remove(None)  # Remove first None
    assert arr.to_list() == [1, 3, 2, 4, None]
    arr.remove(1)
    assert arr.to_list() == [3, 2, 4, None]
    arr.remove(4)
    assert arr.to_list() == [3, 2, None]
    # Test removing non-existent value (should do nothing)
    arr.remove(99)
    assert arr.to_list() == [3, 2, None]


def test_len() -> None:
    """Test __len__() method."""
    arr: DynamicArray[Any] = DynamicArray()
    assert len(arr) == 0
    arr.add(1)
    arr.add(2)
    assert len(arr) == 2
    arr.remove(1)
    assert len(arr) == 1


def test_member() -> None:
    """Test member() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.add(3)
    arr.add(None)
    assert arr.member(3) is True
    assert arr.member(5) is False
    assert arr.member(None) is True


def test_reverse() -> None:
    """Test reverse() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list([1, 2, 3, None, 5])
    arr.reverse()
    assert arr.to_list() == [5, None, 3, 2, 1]
    arr.reverse()
    assert arr.to_list() == [1, 2, 3, None, 5]
    # Test reversing empty and single-element arrays
    empty_arr: DynamicArray[Any] = DynamicArray()
    empty_arr.reverse()
    assert empty_arr.to_list() == []
    single_arr: DynamicArray[Any] = DynamicArray()
    single_arr.add(10)
    single_arr.reverse()
    assert single_arr.to_list() == [10]


def test_filter() -> None:
    """Test filter() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list([1, 2, 3, 4, None, 5, 6])
    arr.filter(lambda x: isinstance(x, int) and x % 2 == 0)
    assert arr.to_list() == [2, 4, 6]
    # Test filtering that results in empty array
    arr.filter(lambda x: x > 100)
    assert arr.to_list() == []


def test_map() -> None:
    """Test map() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list([1, 2, 3])
    arr.map(lambda x: x * 2 if isinstance(x, int) else x)
    assert arr.to_list() == [2, 4, 6]
    arr.map(str)
    assert arr.to_list() == ["2", "4", "6"]


def test_reduce() -> None:
    """Test reduce() method."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list([1, 2, 3, 4])
    assert arr.reduce(lambda acc, x: acc + x, 0) == 10
    assert arr.reduce(lambda acc, x: acc * x, 1) == 24
    # Test with initial value
    assert arr.reduce(
        lambda acc, x: acc + str(x), "Numbers: "
    ) == "Numbers: 1234"
    # Test on empty array
    empty_arr: DynamicArray[Any] = DynamicArray()
    assert empty_arr.reduce(lambda acc, x: acc + x, 100) == 100


def test_none_values() -> None:
    """Test storing and retrieving None values."""
    arr: DynamicArray[Any] = DynamicArray()
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


def test_mixed_types() -> None:
    """Test storing elements of different types."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.add(1)        # Integer
    arr.add("hello")  # String
    arr.add(3.14)     # Float
    arr.add(None)     # None
    arr.add(True)     # Boolean
    assert arr.to_list() == [1, "hello", 3.14, None, True]
    assert len(arr) == 5
    assert arr.get(1) == "hello"
    assert arr.get(3) is None


def test_equality() -> None:
    """Test __eq__ method."""
    arr1: DynamicArray[Any] = DynamicArray()
    arr1.from_list([1, 2, 3])
    arr2: DynamicArray[Any] = DynamicArray()
    arr2.from_list([1, 2, 3])
    arr3: DynamicArray[Any] = DynamicArray()
    arr3.from_list([1, 2, 4])
    arr4: DynamicArray[Any] = DynamicArray()
    arr4.from_list([1, 2])

    assert arr1 == arr2
    assert arr1 != arr3
    assert arr1 != arr4
    assert arr1 != [1, 2, 3]  # Compare with different type


# --- Monoid Law Tests ---

def test_monoid_identity_empty() -> None:
    """Test Monoid identity element (empty())."""
    assert DynamicArray.empty().to_list() == []
    assert len(DynamicArray.empty()) == 0


@settings(max_examples=200)  # type: ignore
@given(dynamic_array_st())  # type: ignore
def test_monoid_identity_law(arr: DynamicArray[Any]) -> None:
    """
    Property-based test for Monoid identity law:
    - Identity element e with a • e = a and e • a = a
    """
    # Get a copy of the original array for comparison
    original = copy.deepcopy(arr)

    # Test a • e = a (right identity)
    right_identity = copy.deepcopy(arr)
    right_identity.concat(DynamicArray.empty())
    assert right_identity == original, "Right identity law failed"

    # Test e • a = a (left identity)
    left_identity: DynamicArray[Any] = DynamicArray.empty()
    left_identity.concat(arr)
    assert left_identity == original, "Left identity law failed"


@settings(max_examples=100)  # type: ignore
@given(dynamic_array_st(), dynamic_array_st(),
       dynamic_array_st())  # type: ignore
def test_monoid_associativity_law(
    a: DynamicArray[Any], b: DynamicArray[Any], c: DynamicArray[Any]
) -> None:
    """
    Property-based test for Monoid associativity law:
    - (a • b) • c = a • (b • c)
    """
    # Calculate (a • b) • c
    ab = copy.deepcopy(a)
    ab.concat(b)
    ab_c = copy.deepcopy(ab)
    ab_c.concat(c)

    # Calculate a • (b • c)
    bc = copy.deepcopy(b)
    bc.concat(c)
    a_bc = copy.deepcopy(a)
    a_bc.concat(bc)

    # Compare the results directly
    assert ab_c == a_bc, f"Associativity law failed"


# --- Roundtrip Tests ---

@settings(max_examples=200)  # type: ignore
@given(list_st)  # type: ignore
def test_from_list_to_list_roundtrip(lst: List[Any]) -> None:
    """Test that from_list() followed by to_list() preserves the original list."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list(lst)
    assert arr.to_list() == lst


@settings(max_examples=200)  # type: ignore
@given(dynamic_array_st())  # type: ignore
def test_copy_preserves_content(arr: DynamicArray[Any]) -> None:
    """Test that copy() creates an independent but equal copy."""
    copied = copy.deepcopy(arr)
    # Verify equality
    assert copied == arr

    # Verify independence (modifying one doesn't affect the other)
    if len(arr) > 0:
        copied.add(999)
        assert copied != arr


# --- Iterator Tests ---

@settings(max_examples=200)  # type: ignore
@given(list_st)  # type: ignore
def test_iterator(lst: List[Any]) -> None:
    """Test that iterating through the array works correctly."""
    arr: DynamicArray[Any] = DynamicArray()
    arr.from_list(lst)

    # Collect elements via iteration
    iterated_elements: List[Any] = []
    for item in arr:
        iterated_elements.append(item)

    # Compare with the original list
    assert iterated_elements == lst
