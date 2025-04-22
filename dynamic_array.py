"""
DynamicArray Implementation

This class implements a dynamic array with support for custom growth factors,
standard list operations, and Monoid properties.
"""

from functools import reduce
from typing import TypeVar, Generic, List, Callable, Any, Optional, Iterator, Union, overload

T = TypeVar('T')  # Define a type variable for generic typing
U = TypeVar('U')  # For transform functions

class DynamicArray(Generic[T]):
    """A dynamic array with custom growth factor and Monoid properties."""

    def __init__(self, growth_factor: int = 2):
        """
        Initialize the dynamic array.

        Parameters:
        growth_factor (int): Factor by which the array grows when full.
        """
        self.capacity: int = 1  # Initial capacity
        self.size: int = 0  # Number of elements
        self.data: List[Optional[T]] = [None] * self.capacity  # Internal storage
        self.growth_factor: int = growth_factor

    def _resize(self) -> None:
        """Resize the internal array when full."""
        new_capacity = self.capacity * self.growth_factor
        new_data: List[Optional[T]] = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def add(self, value: T) -> None:
        """Add a new element to the array."""
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def set(self, index: int, value: T) -> None:
        """Set an element at a specific index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        self.data[index] = value

    def get(self, index: int) -> T:
        """Retrieve an element by index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]  # type: ignore

    def remove(self, value: T) -> None:
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

    def __len__(self) -> int:
        """Return the number of elements in the array."""
        return self.size

    def member(self, value: T) -> bool:
        """Check if a value exists in the array."""
        for i in range(self.size):
            if self.data[i] == value:
                return True
        return False

    def reverse(self) -> None:
        """Reverse the array in-place."""
        for i in range(self.size // 2):
            self.data[i], self.data[self.size - 1 - i] = self.data[self.size - 1 - i], self.data[i]

    def from_list(self, lst: List[T]) -> None:
        """Initialize the dynamic array from a Python list."""
        # Calculate appropriate capacity to avoid unnecessary resizing
        self.capacity = max(len(lst), 1)
        # Make sure we have enough capacity with growth factor in mind
        while self.capacity < len(lst):
            self.capacity *= self.growth_factor
            
        self.size = len(lst)
        self.data = [None] * self.capacity  # Reset the data array
        
        for i in range(len(lst)):
            self.data[i] = lst[i]

    def to_list(self) -> List[T]:
        """Convert the dynamic array to a Python list."""
        return [self.data[i] for i in range(self.size)]  # type: ignore

    def filter(self, predicate: Callable[[T], bool]) -> None:
        """Filter elements based on a predicate in-place."""
        j = 0
        for i in range(self.size):
            if predicate(self.data[i]):  # type: ignore
                if i != j:
                    self.data[j] = self.data[i]
                j += 1
        
        # Clear remaining elements and update size
        for i in range(j, self.size):
            self.data[i] = None
        self.size = j

    def map(self, func: Callable[[T], U]) -> None:
        """Apply a function to all elements in-place."""
        for i in range(self.size):
            self.data[i] = func(self.data[i])  # type: ignore

    def reduce(self, func: Callable[[U, T], U], init_val: U) -> U:
        """Reduce the array to a single value."""
        result = init_val
        for i in range(self.size):
            result = func(result, self.data[i])  # type: ignore
        return result

    @classmethod
    def empty(cls, growth_factor: int = 2) -> 'DynamicArray[T]':
        """Return an empty DynamicArray (Monoid identity element)."""
        return cls(growth_factor)

    def concat(self, other: 'DynamicArray[T]') -> None:
        """
        Concatenate another DynamicArray in-place.
        This modifies the current array instead of creating a new one.
        """
        if not isinstance(other, DynamicArray):
            raise TypeError("Can only concatenate with another DynamicArray")
        
        # Ensure we have enough capacity
        required_capacity = self.size + other.size
        while self.capacity < required_capacity:
            self._resize()
            
        # Copy elements from other array
        for i in range(other.size):
            self.data[self.size + i] = other.data[i]
        
        # Update size
        self.size += other.size

    def __iter__(self) -> Iterator[T]:
        """Iterator support."""
        self._iter_index = 0
        return self

    def __next__(self) -> T:
        """Iterator next method."""
        if self._iter_index < self.size:
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        raise StopIteration
        
    def __eq__(self, other: object) -> bool:
        """Check equality with another DynamicArray."""
        if not isinstance(other, DynamicArray):
            return False
        if self.size != other.size:
            return False
        for i in range(self.size):
            if self.data[i] != other.data[i]:
                return False
        return True