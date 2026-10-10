import unittest

from multi_value_map import MultiValueMap


class TestMultiValueMap(unittest.TestCase):
    def test_add_single_value(self):
        m = MultiValueMap()
        m.add("k", 1)
        self.assertEqual(m["k"], [1])

    def test_add_multiple_values_same_key(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 2)
        self.assertEqual(m["k"], [1, 2])

    def test_add_preserves_duplicate_values(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 1)
        self.assertEqual(m["k"], [1, 1])

    def test_get_one_returns_first(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 2)
        self.assertEqual(m.get_one("k"), 1)

    def test_get_one_missing_key_is_none(self):
        m = MultiValueMap()
        self.assertIsNone(m.get_one("missing"))

    def test_get_all_returns_copy(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 2)
        result = m.get_all("k")
        self.assertEqual(result, [1, 2])
        result.append(999)
        self.assertEqual(m["k"], [1, 2])

    def test_get_all_missing_key_is_empty_list(self):
        m = MultiValueMap()
        self.assertEqual(m.get_all("missing"), [])

    def test_remove_value(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 2)
        m.remove("k", 1)
        self.assertEqual(m["k"], [2])

    def test_remove_value_deletes_key_when_list_empty(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.remove("k", 1)
        self.assertNotIn("k", m)
        self.assertEqual(m.get_all("k"), [])
        self.assertIsNone(m.get_one("k"))

    def test_remove_only_first_occurrence(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.add("k", 1)
        m.remove("k", 1)
        self.assertEqual(m["k"], [1])

    def test_remove_missing_key_raises_key_error(self):
        m = MultiValueMap()
        with self.assertRaises(KeyError):
            m.remove("missing", 1)

    def test_remove_missing_value_raises_value_error(self):
        m = MultiValueMap()
        m.add("k", 1)
        with self.assertRaises(ValueError):
            m.remove("k", 999)

    def test_iteration_yields_keys(self):
        m = MultiValueMap()
        m.add("a", 1)
        m.add("b", 2)
        self.assertEqual(sorted(m), ["a", "b"])

    def test_len_counts_keys(self):
        m = MultiValueMap()
        m.add("a", 1)
        m.add("a", 2)
        m.add("b", 3)
        self.assertEqual(len(m), 2)

    def test_bool_empty_is_false(self):
        m = MultiValueMap()
        self.assertFalse(m)

    def test_bool_nonempty_is_true(self):
        m = MultiValueMap()
        m.add("a", 1)
        self.assertTrue(m)

    def test_add_then_get_all_after_empty_key_removed(self):
        m = MultiValueMap()
        m.add("k", 1)
        m.remove("k", 1)
        m.add("k", 5)
        self.assertEqual(m.get_all("k"), [5])

    def test_get_all_copy_is_independent_across_calls(self):
        m = MultiValueMap()
        m.add("k", 1)
        first = m.get_all("k")
        second = m.get_all("k")
        first.append(2)
        self.assertEqual(second, [1])


if __name__ == "__main__":
    unittest.main()
