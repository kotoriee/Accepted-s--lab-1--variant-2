# Accepted - Lab 1 - Variant 2

This project implements a dynamic array using fixed-size chunks
with a configurable growth factor.
The dynamic array supports basic operations such as adding,
retrieving, updating, and removing elements.
It also provides efficient memory management by
allocating additional chunks only when necessary.

---

## Project Structure

- `dynamic_array.py`
  Core implementation
  of the DynamicArray class.
- `test_dynamic_array.py`
  Unit tests and Property-Based tests
  for the DynamicArray class.
- `README.md`
  Project documentation.

---

## Features

- **PBT: `test_add`**
  Tests the `add` method to ensure elements are correctly appended to the
  dynamic array and that resizing works as expected.
- **PBT: `test_set_get`**
  Validates the `set` and `get` methods for retrieving and updating elements at
  specific indices, ensuring index boundaries are respected.
- **PBT: `test_handle_none`**
  Ensures the dynamic array can store, retrieve, and process `None` values
  without errors.
- **PBT: `test_remove`**
  Tests the `remove` method to confirm elements are correctly removed, and the
  remaining elements shift left as expected.
- **PBT: `test_member`**
  Verifies that the `member` method correctly determines whether a given value
  exists in the dynamic array.
- **PBT: `test_reverse`**
  Tests the `reverse` method to ensure that the order of elements is correctly reversed.
- **PBT: `test_filter`**
  Validates that `filter` correctly removes elements that do not satisfy the given
  predicate while maintaining the correct order.
- **PBT: `test_map`**
  Ensures `map` applies a transformation function to all elements in the array and
  correctly updates their values.
- **PBT: `test_reduce`**
  Confirms that `reduce` accumulates elements using a specified function and
  initial value, producing the correct result.
- **PBT: `test_monoid_identity`**
  Ensures that `empty()` returns a valid identity element for the dynamic array
  in the context of Monoid properties.
- **PBT: `test_monoid_associativity`**
  Validates the Monoid associativity property, ensuring that concatenation
  satisfies `(a • b) • c = a • (b • c)`.
- **PBT: `test_iter`**
  Verifies that the dynamic array supports iteration and that iterating over
  the structure produces the correct sequence of elements.
- **PBT: `test_hypothesis`**
  Uses property-based testing to confirm that converting a list to a `DynamicArray`
  and back to a list preserves all elements correctly.
- **PBT: `test_none_values`**
  Testing inputs of type None.
- **PBT: `test_mixed_types`**
  Testing various types of data input. 

---

## Contribution

- **Cao Xinyang**: Provided the initial
  implementation of the `DynamicArray` class.
- **Xiong Shichi**: Collaborated with Cao
  Xinyang on refining the implementation and testing.

---

## Changelog

- 26.02.2025 - 3  
   - Added tests for None and other types of data, optimized hypothesis test, updated readme file.
- 12.02.2025 - 2  
   - Added missing methods, added missing unit tests and Property-based tests.
- 12.02.2025 - 1  
   - Update README.
- 10.02.2025 - 0  
   - Initial

---

## Design notes

- <https://en.wikipedia.org/wiki/Dynamic_array>
