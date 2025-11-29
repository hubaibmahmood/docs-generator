import logging

from tree_sitter_language_pack import get_parser

from src.analysis.parsing.base_parser import BaseParser
from src.common.exceptions import ParsingError
from src.models.analysis import AnalysisError, ClassElement, FileAnalysis, FunctionElement, MethodElement

logger = logging.getLogger(__name__)

class PythonParser(BaseParser):
    """
    Parser for Python source code using tree-sitter.
    """
    def __init__(self):
        """
        Initializes the PythonParser with the tree-sitter python grammar.
        """
        self.parser = get_parser("python")

    @property
    def supported_file_extensions(self) -> set[str]:
        return {".py", ".pyw"}

    def parse(self, file_path: str) -> FileAnalysis:
        """
        Parses a Python file and extracts code elements.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            FileAnalysis: The analysis result containing extracted elements and errors.
        
        Raises:
            ParsingError: If the file cannot be read.
        """
        logger.info(f"Attempting to parse Python file: {file_path}")
        try:
            with open(file_path, "rb") as f:
                content = f.read()
        except OSError as e:
            logger.error(f"IOError while reading file {file_path}: {e}")
            raise ParsingError(f"Could not read file {file_path}: {e}")

        tree = self.parser.parse(content)
        root_node = tree.root_node

        elements = []
        errors = []

        if root_node.has_error:
            error_msg = "Syntax error detected by tree-sitter"
            logger.warning(f"File {file_path} has syntax errors: {error_msg}")
            errors.append(AnalysisError(file_path=file_path, error=error_msg))
        else:
            for node in root_node.children:
                if node.type == "function_definition":
                    func_element = self._extract_function(node, content)
                    elements.append(func_element)
                    logger.debug(f"Extracted function: {func_element.name} from {file_path}")
                elif node.type == "class_definition":
                    class_element = self._extract_class(node, content)
                    elements.append(class_element)
                    logger.debug(f"Extracted class: {class_element.name} from {file_path}")

        logger.info(f"Finished parsing Python file: {file_path}")
        return FileAnalysis(
            file_path=file_path,
            file_type="Python",
            language="Python",
            elements=elements,
            dependencies=[], # Placeholder for now
            is_binary=False,
            errors=errors,
        )

    def _extract_function(self, node, content: bytes) -> FunctionElement:
        """
        Extracts a function definition from a tree-sitter node.
        """
        name_node = node.child_by_field_name("name")
        name = content[name_node.start_byte:name_node.end_byte].decode("utf-8")

        body_node = node.child_by_field_name("body")
        docstring = self._get_docstring(body_node, content)

        return_type = None
        return_type_node = node.child_by_field_name("return_type")
        if return_type_node:
            return_type = content[return_type_node.start_byte:return_type_node.end_byte].decode("utf-8")

        return FunctionElement(name=name, docstring=docstring, return_type=return_type)

    def _extract_class(self, node, content: bytes) -> ClassElement:
        """
        Extracts a class definition from a tree-sitter node.
        """
        name_node = node.child_by_field_name("name")
        name = content[name_node.start_byte:name_node.end_byte].decode("utf-8")

        body_node = node.child_by_field_name("body")
        docstring = self._get_docstring(body_node, content)

        methods = []
        if body_node:
            for child in body_node.children:
                if child.type == "function_definition": # Methods are function definitions inside a class
                    methods.append(self._extract_method(child, content))

        return ClassElement(name=name, docstring=docstring, methods=methods)

    def _extract_method(self, node, content: bytes) -> MethodElement:
        """
        Extracts a method definition from a tree-sitter node.
        """
        name_node = node.child_by_field_name("name")
        name = content[name_node.start_byte:name_node.end_byte].decode("utf-8")

        body_node = node.child_by_field_name("body")
        docstring = self._get_docstring(body_node, content)

        return_type = None
        return_type_node = node.child_by_field_name("return_type")
        if return_type_node:
            return_type = content[return_type_node.start_byte:return_type_node.end_byte].decode("utf-8")

        return MethodElement(name=name, docstring=docstring, return_type=return_type)

    def _get_docstring(self, body_node, content: bytes) -> str | None:
        """
        Extracts the docstring from a function or class body.
        """
        if not body_node:
            return None

        # Check for multiline string literal as first child of the body
        # or an expression statement containing a string literal
        if body_node.children:
            first_child = body_node.children[0]
            if first_child.type == 'expression_statement':
                # Check if the expression statement contains a string
                if first_child.children and first_child.children[0].type == 'string':
                    string_node = first_child.children[0]
                    # Extract the raw string, then unquote it
                    raw_docstring = content[string_node.start_byte:string_node.end_byte].decode("utf-8")
                    # Basic unquoting for common Python string literals
                    if raw_docstring.startswith(('"""', "'''")) and raw_docstring.endswith(('"""', "'''")):
                        return raw_docstring[3:-3]
                    elif raw_docstring.startswith(('"', "'")) and raw_docstring.endswith(('"', "'")):
                        return raw_docstring[1:-1]
            elif first_child.type == 'string': # Direct string literal (less common for docstrings but possible)
                raw_docstring = content[first_child.start_byte:first_child.end_byte].decode("utf-8")
                if raw_docstring.startswith(('"""', "'''")) and raw_docstring.endswith(('"""', "'''")):
                    return raw_docstring[3:-3]
                elif raw_docstring.startswith(('"', "'")) and raw_docstring.endswith(('"', "'")):
                    return raw_docstring[1:-1]
        return None
