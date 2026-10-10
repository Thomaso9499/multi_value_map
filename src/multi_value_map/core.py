from __future__ import annotations

from typing import Dict, Hashable, Iterator, List, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class MultiValueMap(Dict[K, List[V]]):
    """A mapping where each key is associated with a list of values.

    Subclassing ``dict`` keeps the interface small and familiar while giving
    direct access to the underlying value-lists when callers need them. The
    trade-off is that direct ``map[key]`` access returns the live list rather
    than a defensive copy: callers who mutate it bypass the append/remove
    accounting. For the common case (append, get, remove, iterate) the methods
    here are the supported path.
    """

    def __init__(self) -> None:
        super().__init__()

    def add(self, key: K, value: V) -> None:
        """Append ``value`` to the list stored at ``key``.

        Creates the key if absent. Silently allows duplicates, because the
        structure is a list of values, not a set: ordering and repetition can
        carry meaning for the caller.
        """
        values = self.get(key)
        if values is None:
            values = []
            self[key] = values
        values.append(value)

    def remove(self, key: K, value: V) -> None:
        """Remove the first occurrence of ``value`` from ``key``.

        Raises ``KeyError`` if the key is absent, preserving the Python
        convention that removing from a missing container is an error rather
        than a silent no-op. Raises ``ValueError`` if the key exists but the
        value is not present, mirroring ``list.remove``.
        """
        values = self[key]
        values.remove(value)
        if not values:
            del self[key]

    def get_one(self, key: K) -> V | None:
        """Return the first value for ``key``, or ``None`` if absent.

        Returns ``None`` rather than raising for both the missing-key and
        empty-list cases, so callers can treat "no values" uniformly.
        """
        values = self.get(key)
        if not values:
            return None
        return values[0]

    def get_all(self, key: K) -> List[V]:
        """Return a copy of every value for ``key``, empty list if absent.

        A copy is returned so the caller cannot mutate the internal list by
        accident. If mutation of the live list is desired, use ``map[key]``
        directly.
        """
        values = self.get(key)
        if not values:
            return []
        return list(values)

    def __iter__(self) -> Iterator[K]:
        return super().__iter__()

    def __len__(self) -> int:
        return super().__len__()
