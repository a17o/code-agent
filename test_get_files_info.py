import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_current_directory(self) -> None:
        dir = "."
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:\n{result}\n")

    def test_file_name(self) -> None:
        dir = "pkg"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:\n{result}\n")

    def test_non_existent_directory(self) -> None:
        dir = "/bin"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:\n{result}\n")

    def test_parent_directory(self) -> None:
        dir = "../"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:\n{result}\n")


if __name__ == "__main__":
    unittest.main()
