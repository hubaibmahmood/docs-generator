import os

from src.analysis.parsing.base_parser import BaseParser
from src.analysis.parsing.python_parser import PythonParser


class ParserFactory:
    """
    Factory class to manage and retrieve appropriate parsers for different file types.
    """
    _parsers: list[BaseParser] = []

    @classmethod
    def register_parser(cls, parser: BaseParser):
        """
        Registers a new parser instance.

        Args:
            parser (BaseParser): The parser instance to register.
        """
        cls._parsers.append(parser)

    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser | None:
        """
        Retrieves a compatible parser for the given file path based on extension.

        Args:
            file_path (str): The path of the file to find a parser for.

        Returns:
            Optional[BaseParser]: A compatible parser instance, or None if no match is found.
        """
        _, file_extension = os.path.splitext(file_path)
        for parser in cls._parsers:
            if file_extension.lower() in parser.supported_file_extensions:
                return parser
        return None

# Register parsers
ParserFactory.register_parser(PythonParser())
