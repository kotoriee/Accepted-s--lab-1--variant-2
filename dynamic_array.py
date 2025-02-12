class DynamicArray:
    """A dynamic array with custom growth factor and Monoid properties."""

    def __init__(self, growth_factor=2):
        self.capacity = 1
        self.size = 0
        self.data = [None] * self.capacity
        self.growth_factor = growth_factor

    def _resize(self):
        new_capacity = self.capacity * self.growth_factor
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def add(self, value):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def set(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        self.data[index] = value

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]

    def remove(self, value):
        found = False
        for i in range(self.size):
            if self.data[i] == value:
                found = True
            if found and i < self.size - 1:
                self.data[i] = self.data[i + 1]
        if found:
            self.data[self.size - 1] = None
            self.size -= 1

    def size(self):
        return self.size

    def member(self, value):
        return value in self.data[:self.size]

    def reverse(self):
        self.data[:self.size] = self.data[:self.size][::-1]

    def from_list(self, lst):
        self.capacity = max(len(lst), 1) * self.growth_factor
        self.size = len(lst)
        self.data = [None] * self.capacity
        for i in range(len(lst)):
            self.data[i] = lst[i]

    def to_list(self):
        return self.data[:self.size]

    def filter(self, predicate):
        new_data = [x for x in self.data[:self.size] if predicate(x)]
        self.from_list(new_data)

    def map(self, func):
        for i in range(self.size):
            self.data[i] = func(self.data[i])

    def reduce(self, func, init_val):
        """Custom reduce implementation without functools."""
        acc = init_val
        for i in range(self.size):
            acc = func(acc, self.data[i])
        return acc

    def empty(self):
        return DynamicArray(self.growth_factor)

    def concat(self, other):
        if not isinstance(other, DynamicArray):
            raise TypeError("Can only concatenate with another DynamicArray")
        new_array = DynamicArray(self.growth_factor)
        new_array.from_list(self.to_list() + other.to_list())
        return new_array

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < self.size:
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        raise StopIteration
