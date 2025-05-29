
#!/usr/bin/env python3
"""Unit test for utils.access_nested_map."""
import unittest
from parameterized import parameterized
from utils import access_nested_map  # Ensure correct import path

class TestAccessNestedMap(unittest.TestCase):
    """Tests access_nested_map function with various inputs."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Verifies correct return values from access_nested_map."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == "__main__":
    unittest.main()
