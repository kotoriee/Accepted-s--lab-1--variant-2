"""
DynamicArray Implementation
"""


class DynamicArray:
    """
    A dynamic array using fixed-size chunks
    with a configurable growth factor.
    """

    def __init__(self, chunk_size=4, growth_factor=2):
        """
        Initialize a dynamic array.

        Parameters:
        chunk_size (int): The size of each memory chunk.
        growth_factor (int): The factor
        by which the number of chunks grows.
        """
        self.chunk_size = chunk_size
        self.growth_factor = growth_factor
        self.chunks = [[None] * chunk_size]  # Initialize first chunk
        self.size = 0

    def _resize(self):
        """Allocate a new chunk when needed."""
        new_chunk = [None] * self.chunk_size
        self.chunks.append(new_chunk)

    def add(self, value):
        """Add an element to the array."""
        if self.size % self.chunk_size == 0 and self.size > 0:
            self._resize()

        chunk_index = self.size // self.chunk_size
        element_index = self.size % self.chunk_size
        self.chunks[chunk_index][element_index] = value
        self.size += 1

    def get(self, index):
        """Retrieve an element by index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        chunk_index = index // self.chunk_size
        element_index = index % self.chunk_size
        return self.chunks[chunk_index][element_index]

    def set(self, index, value):
        """Set an element at a specific index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        chunk_index = index // self.chunk_size
        element_index = index % self.chunk_size
        self.chunks[chunk_index][element_index] = value

    def remove(self, index):
        """
        Remove an element at a specific index,
        shifting elements left.
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        for i in range(index, self.size - 1):
            chunk_index = i // self.chunk_size
            element_index = i % self.chunk_size
            next_chunk_index = (i + 1) // self.chunk_size
            next_element_index = (i + 1) % self.chunk_size
            self.chunks[chunk_index][element_index] = \
            self.chunks[next_chunk_index][next_element_index]

        last_chunk_index = (self.size - 1) // self.chunk_size
        last_element_index = (self.size - 1) % self.chunk_size
        self.chunks[last_chunk_index][last_element_index] = None
        self.size -= 1

    def to_list(self):
        """Convert the dynamic array to a regular Python list."""
        return [self.get(i) for i in range(self.size)]

    def from_list(self, lst):
        """Load elements from a Python list."""
        self.chunks = [[None] * self.chunk_size \
        for _ in range((len(lst) // self.chunk_size) + 1)]
        self.size = 0
        for item in lst:
            self.add(item)

    def __iter__(self):
        """Enable iteration over the dynamic array."""
        self._iter_index = 0
        return self

    def __next__(self):
        """Iterator next method."""
        if self._iter_index < self.size:
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        raise StopIteration
