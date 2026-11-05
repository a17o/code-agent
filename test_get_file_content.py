import unittest
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def test_file_truncated(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertGreaterEqual(len(result), 10_000)
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")

    def test_expected_file(self):
        result = get_file_content("calculator", "main.py")
        print(f"Success, content: {result}")

    def test_nested_file(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(f"Success, content: {result}")

    def test_non_existent_dir(self):
        result = get_file_content("calculator", "bin/cat")
        print(f"{result}")

    def test_non_existent_file(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(f"{result}")


if __name__ == "__main__":
    unittest.main()
