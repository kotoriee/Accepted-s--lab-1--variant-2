"""
DynamicArray Implementation

This class implements a dynamic array with support for custom growth factors,
standard list operations, and Monoid properties.
"""

from functools import reduce
from typing import Any, List, Optional, Callable, Iterable, Iterator # Added imports

class DynamicArray:
    """A dynamic array with custom growth factor and Monoid properties."""

    def __init__(self, growth_factor: int = 2):
        """
        Initialize the dynamic array.

        Parameters:
        growth_factor (int): Factor by which the array grows when full. Default is 2.
        """
        if not isinstance(growth_factor, int) or growth_factor <= 1:
            raise ValueError("Growth factor must be an integer greater than 1")
        self.capacity: int = 1  # Initial capacity
        self.size: int = 0  # Number of elements
        self.data: List[Optional[Any]] = [None] * self.capacity  # Internal storage
        self.growth_factor: int = growth_factor
        self._iter_index: int = 0 # Initialize iterator index

    def _resize(self) -> None:
        """Resize the internal array when full."""
        new_capacity = self.capacity * self.growth_factor
        # Handle potential overflow if capacity becomes extremely large
        if new_capacity <= self.capacity:
             new_capacity = self.capacity + 1 # Minimal increase if multiplication overflows or doesn't increase

        new_data: List[Optional[Any]] = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def add(self, value: Any) -> None:
        """Add a new element to the end of the array."""
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def set(self, index: int, value: Any) -> None:
        """Set an element at a specific index."""
        if not 0 <= index < self.size:
            raise IndexError("Index out of bounds")
        self.data[index] = value

    def get(self, index: int) -> Any:
        """Retrieve an element by index."""
        if not 0 <= index < self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]

    def remove(self, value: Any) -> None:
        """Remove the first occurrence of an element by value, shifting elements left."""
        found_index = -1
        for i in range(self.size):
            # Handle potential comparison issues (e.g., NaN != NaN)
            # This basic check works for most standard types including None
            if self.data[i] == value:
                 # Special check for NaN if needed, assuming standard float NaN behavior
                 # import math
                 # if isinstance(value, float) and math.isnan(value):
                 #    if isinstance(self.data[i], float) and math.isnan(self.data[i]):
                 #        found_index = i
                 #        break
                 # else:
                 found_index = i
                 break # Found the first occurrence

        if found_index != -1:
            # Shift elements left
            for i in range(found_index, self.size - 1):
                self.data[i] = self.data[i + 1]
            self.data[self.size - 1] = None  # Clear the last element slot
            self.size -= 1
        # else: value not found, do nothing or raise error? Current behavior: do nothing.

    def __len__(self) -> int:
        """Return the number of elements in the array."""
        return self.size

    def member(self, value: Any) -> bool:
        """Check if a value exists in the array."""
        # Consider NaN comparison if necessary
        for i in range(self.size):
            if self.data[i] == value:
                 # Add NaN check here if required, similar to remove()
                 return True
        return False
        # Alternative using 'in', might be slightly slower for large arrays if not optimized
        # return value in self.data[:self.size]

    def reverse(self) -> None:
        """Reverse the array in-place."""
        left, right = 0, self.size - 1
        while left < right:
            self.data[left], self.data[right] = self.data[right], self.data[left]
            left += 1
            right -= 1
        # Alternative using slicing (creates a temporary reversed slice):
        # self.data[:self.size] = self.data[:self.size][::-1]

    def from_list(self, lst: List[Any]) -> None:
        """Initialize or overwrite the dynamic array from a Python list."""
        list_len = len(lst)
        # Ensure capacity is sufficient, potentially pre-allocate more
        required_capacity = max(list_len, 1) # Need at least 1 even for empty list
        if required_capacity > self.capacity:
             # Resize based on growth factor for better amortization,
             # instead of just matching list_len
             new_capacity = self.capacity
             while new_capacity < required_capacity:
                 new_capacity *= self.growth_factor
                 # Handle potential overflow
                 if new_capacity <= self.capacity:
                     new_capacity = required_capacity # Fallback if growth factor fails
                     break
             self.capacity = new_capacity
             self.data = [None] * self.capacity

        # Copy elements directly
        for i in range(list_len):
            self.data[i] = lst[i]

        # Clear any remaining old elements if the new list is shorter
        for i in range(list_len, self.size):
            self.data[i] = None

        self.size = list_len


    def to_list(self) -> List[Any]:
        """Convert the dynamic array to a Python list."""
        return list(self.data[:self.size]) # Create a new list copy

    def filter(self, predicate: Callable[[Any], bool]) -> None:
        """Filter elements in-place based on a predicate."""
        # This implementation modifies the array in-place
        write_index = 0
        for read_index in range(self.size):
            element = self.data[read_index]
            if predicate(element):
                if write_index != read_index:
                    self.data[write_index] = element
                write_index += 1
        # Clear remaining elements
        for i in range(write_index, self.size):
            self.data[i] = None
        self.size = write_index

    def map(self, func: Callable[[Any], Any]) -> None:
        """Apply a function to all elements in-place."""
        for i in range(self.size):
            self.data[i] = func(self.data[i])

    def reduce(self, func: Callable[[Any, Any], Any], initial_value: Any) -> Any:
        """Reduce the array to a single value using a function and initial value."""
        # Uses Python's built-in reduce for efficiency
        return reduce(func, self.data[:self.size], initial_value)

    @classmethod
    def empty(cls, growth_factor: int = 2) -> 'DynamicArray':
        """Return an empty DynamicArray (Monoid identity element)."""
        # Note: Standard Monoid identity is typically immutable.
        # This returns a new empty instance.
        return cls(growth_factor)

    def concat(self, other: 'DynamicArray') -> None:
        """
        Concatenate another DynamicArray onto this one (mutable).
        Appends elements from 'other' to the end of 'self'.
        """
        if not isinstance(other, DynamicArray):
            raise TypeError("Can only concatenate with another DynamicArray")

        # Ensure enough capacity in self
        required_capacity = self.size + other.size
        if required_capacity > self.capacity:
            new_capacity = self.capacity
            while new_capacity < required_capacity:
                new_capacity *= self.growth_factor
                # Handle potential overflow
                if new_capacity <= self.capacity:
                    new_capacity = required_capacity
                    break
            self._resize_to(new_capacity) # Helper function for specific capacity

        # Append elements from other
        for i in range(other.size):
            self.data[self.size + i] = other.data[i]
        self.size += other.size

    # Helper for concat to resize to a specific capacity if needed
    def _resize_to(self, new_capacity: int) -> None:
        """Resize the internal array to a specific new capacity."""
        if new_capacity < self.size:
             raise ValueError("New capacity cannot be smaller than current size")
        if new_capacity == self.capacity:
             return # No change needed

        new_data: List[Optional[Any]] = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def copy(self) -> 'DynamicArray':
        """Return a shallow copy of the dynamic array."""
        new_array = DynamicArray(self.growth_factor)
        new_array.size = self.size
        new_array.capacity = self.capacity
        # Create a shallow copy of the data list
        new_array.data = list(self.data) # Use list() for shallow copy
        return new_array

    def __iter__(self) -> Iterator[Any]:
        """Iterator support."""
        self._iter_index = 0
        return self

    def __next__(self) -> Any:
        """Iterator next method."""
        if self._iter_index < self.size:
            value = self.data[self._iter_index] # Direct access is fine here
            self._iter_index += 1
            return value
        # Reset index for potential future iterations? Optional.
        # self._iter_index = 0
        raise StopIteration

    def __str__(self) -> str:
        """Return a string representation of the array."""
        return str(self.to_list())

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"DynamicArray(size={self.size}, capacity={self.capacity}, data={self.to_list()})"

    # Optional: Implement __eq__ for easier testing comparison
    def __eq__(self, other: object) -> bool:
        """Check equality based on content."""
        if not isinstance(other, DynamicArray):
            return NotImplemented
        # Compare size and elements
        if self.size != other.size:
            return False
        # Element-wise comparison, handles NaN correctly if using math.isnan
        for i in range(self.size):
             val1 = self.data[i]
             val2 = other.data[i]
             # Basic equality check
             if val1 != val2:
                 # Handle NaN specifically if needed
                 # import math
                 # if isinstance(val1, float) and math.isnan(val1) and \
                 #    isinstance(val2, float) and math.isnan(val2):
                 #    continue # Both are NaN, treat as equal for this context
                 return False
        return True
