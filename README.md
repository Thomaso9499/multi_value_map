# multi_value_map

A map where each key is associated with a list of values, providing `add`, `remove`, and retrieval operations without manual list management.

```python
from multi_value_map import MultiValueMap

m = MultiValueMap()
m.add("color", "red")
m.add("color", "blue")

m.get_one("color")    # "red"
m.get_all("color")    # ["red", "blue"]

m.remove("color", "red")
m.get_all("color")    # ["blue"]
```

## Why this exists

When a key maps to several values (HTTP query parameters, HTTP headers, grouped records), the boilerplate of checking whether a key exists, creating a list, appending, and pruning empty lists repeats across every codebase. This library wraps that into a small class with three operations: `add`, `remove`, and two getters.

The class subclasses `dict` so the keys are directly iterable and `len`/`in` work as expected. The trade-off is that `m[key]` returns the live internal list, not a copy; callers who mutate it bypass the accounting that `add`/`remove` perform (deleting a key when its list becomes empty). The supported path is the named methods; `get_all` returns a copy for callers who want safe read access.

## Edge cases

- `add` allows duplicate values: this is a list, not a set. Ordering and repetition are preserved.
- `remove` raises `KeyError` for a missing key (following Python's `dict`/`list` convention) and `ValueError` if the key exists but the value is not present (following `list.remove`). When the last value is removed, the key is deleted automatically.
- `get_one` returns `None` for both missing keys and keys whose value list is empty (which should not happen via the supported API, but can if the internal list is mutated directly).
