import unittest
import tempfile
import os
from src.analysis.parsing.python_parser import PythonParser

class TestPythonParser(unittest.TestCase):

    def setUp(self):
        # Create a temporary python file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        self.temp_file.write(b'"""Module docstring."""\n\ndef my_func(a: int) -> int:\n    """Function docstring."""\n    return a + 1\n\nclass MyClass:\n    """Class docstring."""\n    def my_method(self, b: str) -> str:\n        """Method docstring."""\n        return b\n')
        self.temp_file.close()
        self.parser = PythonParser()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_parse_success(self):
        # Act
        analysis = self.parser.parse(self.temp_file.name)

        # Assert
        self.assertEqual(analysis.file_path, self.temp_file.name)
        self.assertEqual(analysis.language, "Python")
        self.assertFalse(analysis.is_binary)
        
        self.assertEqual(len(analysis.elements), 2)
        
        # Check function
        func_element = analysis.elements[0]
        self.assertEqual(func_element.name, "my_func")
        self.assertEqual(func_element.docstring, 'Function docstring.')
        self.assertEqual(func_element.return_type, "int")

        # Check class
        class_element = analysis.elements[1]
        self.assertEqual(class_element.name, "MyClass")
        self.assertEqual(class_element.docstring, 'Class docstring.')
        
        self.assertEqual(len(class_element.methods), 1)
        method_element = class_element.methods[0]
        self.assertEqual(method_element.name, "my_method")
        self.assertEqual(method_element.docstring, 'Method docstring.')
        self.assertEqual(method_element.return_type, "str")

    def test_parse_syntax_error(self):
        # Arrange
        with open(self.temp_file.name, "wb") as f:
            f.write(b"def my_func(a: int) -> int:\n  return a +")

        # Act
        analysis = self.parser.parse(self.temp_file.name)

        # Assert
        self.assertEqual(analysis.file_path, self.temp_file.name)
        self.assertEqual(analysis.language, "Python")
        self.assertEqual(len(analysis.elements), 0)
        self.assertNotEqual(len(analysis.errors), 0)
        self.assertIn("Syntax error", analysis.errors[0].error)


if __name__ == '__main__':
    unittest.main()
