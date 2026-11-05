import unittest

from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_calculator_usage_instructions(self):
        result = run_python_file("calculator", "main.py")
        print(f"Test 1:\n{result}")

    def test_run_calculator(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(f"Test 2:\n{result}")

    def test_run_calculator_tests(self):
        result = run_python_file("calculator", "tests.py")
        print(f"Test 3:\n{result}")

    def test_file_outside_dir(self):
        result = run_python_file("calculator", "../main.py")
        print(f"Test 4: {result}")

    def test_non_existent_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(f"Test 5: {result}")

    def test_wrong_file_format(self):
        result = run_python_file("calculator", "lorem.txt")
        print(f"Test 6: {result}")


if __name__ == "__main__":
    unittest.main()
