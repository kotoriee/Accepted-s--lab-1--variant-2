from hypothesis import given, strategies as st
from dynamic_array import DynamicArray


# Generate lists with ints and None
@given(st.lists(st.one_of(st.integers(), st.none())))
def test_dynamic_array(lst):
    """Test from_list() and to_list() equivalence."""
    arr = DynamicArray(chunk_size=4, growth_factor=2)
    arr.from_list(lst)

    # Ensure data consistency
    assert arr.to_list() == lst
    assert arr.size == len(lst)
