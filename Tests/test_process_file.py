from pathlib import Path
from unittest.mock import patch
from llvm_parser import Compiler, Parser

from Classes.process_file import FileProcessor
from Tests.utils import create_mock_object


@patch("Classes.process_file.Compiler")
def test_create_var_map(mock_compiler_class):
    mock_compiler_instance = create_mock_object(
        Compiler,
        "CompilerMock",
        mock_returns=[("compile_file",
                        Path("Tests/mock_files/mock_debug_file.ll"))])

    mock_compiler_class.return_value = mock_compiler_instance

    file_processor = FileProcessor("")

    variables_map = file_processor.create_var_map()

    assert variables_map == {'p': '%0', 'personPtr': '%1', 'test': '%2'}


@patch("Classes.process_file.Parser")
@patch("Classes.process_file.Compiler")
def test_process_file(mock_compiler_class, mock_parser_class):
    mock_compiler_instance = create_mock_object(
        Compiler,
        "CompilerMock",
        mock_returns=[("compiled_file_exists", False),
                       ("compile_file",
                        Path("Tests/mock_files/mock_compile_file.ll")),
                       ("rm_compiled_file", None)])

    mock_compiler_class.return_value = mock_compiler_instance

    mock_parser_instance = create_mock_object(Parser,
                                              "ParserMock",
                                              mock_returns=[("parse_file", {
                                                  "mock_instruction":
                                                  "mock_value"
                                              })])

    mock_parser_class.return_value = mock_parser_instance

    file_processor = FileProcessor("")

    parse_result = file_processor.process_file()

    assert parse_result == {"mock_instruction": "mock_value"}

    mock_compiler_instance.compile_file.assert_called_once_with(Path(""))
    mock_parser_instance.parse_file.assert_called_once_with(
        Path("Tests/mock_files/mock_compile_file.ll"))
