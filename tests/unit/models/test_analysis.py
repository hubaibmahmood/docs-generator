from src.models.analysis import (
    AnalysisError,
    ClassElement,
    CodeAnalysisResult,
    Dependency,
    ExtractedElement,
    FileAnalysis,
    FunctionElement,
    MethodElement,
)


def test_method_element_creation():
    method = MethodElement(name="test_method", docstring="Doc", return_type="int")
    assert method.name == "test_method"
    assert method.docstring == "Doc"
    assert method.return_type == "int"

def test_method_element_defaults():
    method = MethodElement(name="another_method")
    assert method.name == "another_method"
    assert method.docstring is None
    assert method.return_type is None

def test_function_element_creation():
    func = FunctionElement(name="test_function", docstring="A function", return_type="str")
    assert func.name == "test_function"
    assert func.docstring == "A function"
    assert func.return_type == "str"

def test_function_element_defaults():
    func = FunctionElement(name="another_function")
    assert func.name == "another_function"
    assert func.docstring is None
    assert func.return_type is None

def test_class_element_creation():
    method1 = MethodElement(name="method1")
    class_elem = ClassElement(name="TestClass", docstring="A class", methods=[method1])
    assert class_elem.name == "TestClass"
    assert class_elem.docstring == "A class"
    assert len(class_elem.methods) == 1
    assert class_elem.methods[0].name == "method1"

def test_class_element_defaults():
    class_elem = ClassElement(name="AnotherClass")
    assert class_elem.name == "AnotherClass"
    assert class_elem.docstring is None
    assert class_elem.methods == []

def test_extracted_element_union():
    func_elem = FunctionElement(name="test_func")
    class_elem = ClassElement(name="TestClass")

    extracted_func: ExtractedElement = func_elem
    extracted_class: ExtractedElement = class_elem

    assert isinstance(extracted_func, FunctionElement)
    assert isinstance(extracted_class, ClassElement)

def test_dependency_creation():
    dep = Dependency(package_name="requests", source_file="requirements.txt", version_specifier="==2.28.1")
    assert dep.package_name == "requests"
    assert dep.source_file == "requirements.txt"
    assert dep.version_specifier == "==2.28.1"

def test_dependency_defaults():
    dep = Dependency(package_name="flask", source_file="pyproject.toml")
    assert dep.package_name == "flask"
    assert dep.source_file == "pyproject.toml"
    assert dep.version_specifier is None

def test_analysis_error_creation():
    error = AnalysisError(file_path="/src/main.py", error="Syntax error at line 10")
    assert error.file_path == "/src/main.py"
    assert error.error == "Syntax error at line 10"

def test_file_analysis_creation():
    func_elem = FunctionElement(name="my_func")
    dep1 = Dependency(package_name="numpy", source_file="requirements.txt")
    file_analysis = FileAnalysis(
        file_path="/src/file.py",
        file_type="Python",
        language="Python",
        elements=[func_elem],
        dependencies=[dep1],
        is_binary=False,
    )
    assert file_analysis.file_path == "/src/file.py"
    assert file_analysis.file_type == "Python"
    assert file_analysis.language == "Python"
    assert len(file_analysis.elements) == 1
    assert file_analysis.elements[0].name == "my_func"
    assert len(file_analysis.dependencies) == 1
    assert file_analysis.dependencies[0].package_name == "numpy"
    assert not file_analysis.is_binary

def test_file_analysis_defaults():
    file_analysis = FileAnalysis(
        file_path="/src/binary_file",
        file_type="Binary",
        language="None",
        is_binary=True,
    )
    assert file_analysis.file_path == "/src/binary_file"
    assert file_analysis.file_type == "Binary"
    assert file_analysis.language == "None"
    assert file_analysis.elements == []
    assert file_analysis.dependencies == []
    assert file_analysis.is_binary is True

def test_code_analysis_result_creation():
    file_tree_data = {"src": {"file.py": {}}}
    file_analysis_data = {
        "/src/file.py": FileAnalysis(file_path="/src/file.py", file_type="Python", language="Python")
    }
    error_data = [AnalysisError(file_path="/src/bad_file.py", error="Parse error")]

    result = CodeAnalysisResult(
        file_tree=file_tree_data,
        file_analysis=file_analysis_data,
        errors=error_data,
    )
    assert result.file_tree == file_tree_data
    assert "/src/file.py" in result.file_analysis
    assert len(result.errors) == 1
    assert result.errors[0].file_path == "/src/bad_file.py"

def test_code_analysis_result_defaults():
    result = CodeAnalysisResult()
    assert result.file_tree == {}
    assert result.file_analysis == {}
    assert result.errors == []
