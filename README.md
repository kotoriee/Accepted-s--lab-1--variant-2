# Accepted - Lab 1 - Variant 2

This project implements a dynamic array using fixed-size chunks 
with a configurable growth factor.  
The dynamic array supports basic operations such as adding, 
retrieving, updating, and removing elements.  
It also provides efficient memory management by 
allocating additional chunks only when necessary.

---

## Project Structure

- `dynamic_array.py` -- Core implementation 
of the DynamicArray class.
- `test_dynamic_array.py` -- Unit tests 
for the DynamicArray class.
- `test_dynamic_array_property.py` -- Property tests 
for the DynamicArray class.
- `README.md` -- Project documentation.
---

## Features

- **PBT: `test_add`**  
  Tests the `add` method to ensure elements are correctly appended to the array.

- **PBT: `test_get_set`**  
  Validates the `get` and `set` methods for retrieving and updating elements.

- **PBT: `test_handle_none`**  
  Ensures the dynamic array can handle `None` values without errors.

- **PBT: `test_remove`**  
  Tests the `remove` method to confirm elements are removed and shifted correctly.

- **PBT: `test_iter`**  
  Verifies that the dynamic array supports iteration over its elements.

---

## Contribution

- **Cao Xinyang**: Provided the initial 
implementation of the `DynamicArray` class.
- **Xiong Shichi**: Collaborated with Cao 
Xinyang on refining the implementation and testing.

---

## Changelog

- 12.02.2025 - 1
  - Update README. 
- 10.02.2025 - 0
  - Initial

---

## Design notes

- <https://en.wikipedia.org/wiki/Dynamic_array>
