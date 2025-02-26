"""
DynamicArray Implementation

This class implements a dynamic array with support for custom growth factors,
standard list operations, and Monoid properties.
"""

from functools import reduce


class DynamicArray:
    """A dynamic array with custom growth factor and Monoid properties."""

    def __init__(self, growth_factor=2):
        """
        Initialize the dynamic array.

        Parameters:
        growth_factor (int): Factor by which the array grows when full.
        """
        self.capacity = 1  # Initial capacity
        self.size = 0  # Number of elements
        self.data = [None] * self.capacity  # Internal storage
        self.growth_factor = growth_factor

    def _resize(self):
        """Resize the internal array when full."""
        new_capacity = self.capacity * self.growth_factor
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def add(self, value):
        """Add a new element to the array."""
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def set(self, index, value):
        """Set an element at a specific index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        self.data[index] = value

    def get(self, index):
        """Retrieve an element by index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]

    def remove(self, value):
        """Remove an element by value, shifting elements left."""
        found = False
        for i in range(self.size):
            if self.data[i] == value:
                found = True
            if found and i < self.size - 1:
                self.data[i] = self.data[i + 1]
        if found:
            self.data[self.size - 1] = None
            self.size -= 1

    def __len__(self):
        """Return the number of elements in the array."""
        return self.size

    def member(self, value):
        """Check if a value exists in the array."""
        return value in self.data[:self.size]

    def reverse(self):
        """Reverse the array."""
        self.data[:self.size] = self.data[:self.size][::-1]

    def from_list(self, lst):
        """Initialize the dynamic array from a Python list."""
        self.capacity = max(len(lst), 1) * self.growth_factor
        self.size = len(lst)
        self.data = [None] * self.capacity
        for i in range(len(lst)):
            self.data[i] = lst[i]

    def to_list(self):
        """Convert the dynamic array to a Python list."""
        return self.data[:self.size]

    def filter(self, predicate):
        """Filter elements based on a predicate."""
        new_data = [x for x in self.data[:self.size] if predicate(x)]
        self.from_list(new_data)

    def map(self, func):
        """Apply a function to all elements."""
        for i in range(self.size):
            self.data[i] = func(self.data[i])

    def reduce(self, func, init_val):
        """Reduce the array to a single value."""
        return reduce(func, self.data[:self.size], init_val)

    def empty(self):
        """Return an empty DynamicArray (Monoid identity element)."""
        return DynamicArray(self.growth_factor)

    def concat(self, other):
        """Concatenate another DynamicArray."""
        if not isinstance(other, DynamicArray):
            raise TypeError("Can only concatenate with another DynamicArray")
        new_array = DynamicArray(self.growth_factor)
        new_array.from_list(self.to_list() + other.to_list())
        return new_array

    def __iter__(self):
        """Iterator support."""
        self._iter_index = 0
        return self

    def __next__(self):
        """Iterator next method."""
        if self._iter_index < self.size:
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        raise StopIteration
