import shutil
from os.path import abspath
from os import system, remove
import unittest

from std_doc import ModuleToDoc


class TestDocstringWriterUtil(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        shutil.copy(src="test_files/test_input.py", dst="test_files/stable.py")

    @classmethod
    def tearDown(cls) -> None:
        shutil.copy(src="test_files/stable.py", dst="test_files/test_input.py")
        remove("test_files/stable.py")


class TestDirectly(TestDocstringWriterUtil):
    @classmethod
    def setUp(cls) -> None:
        super().setUp()
        cls.parser = ModuleToDoc(abspath("test_files/test_input.py"))

    def test_moduleDocstring_parsedCorrectly(self):
        assert self.parser._docstr_data['TEMP NOTES'] == ('TODO: move these notes into a section with a header\n'
                                                          'Unformatted Module docstring')

    def test_findClasses_foundClass(self):
        assert len(self.parser._classes) == 2
        assert self.parser._classes[0].name == "TestClass"
        assert self.parser._classes[1].name == "_LinkType"

    def test_classDocstring_parsedCorrectly(self):
        assert self.parser._classes[0]._docstr_data['FUNCTIONS'] == "- test_fn\n    - lorem\n    - ipsum"
        assert self.parser._classes[0]._docstr_data['PURPOSE'] == 'Class docstring'
        assert not self.parser._classes[0]._docstr_data.get('TEMP NOTES')

    def test_findFns_foundFns(self):
        assert len(self.parser._classes[0]._fns) == 3
        assert self.parser._classes[0]._fns[0].name == 'test_fn'
        assert self.parser._classes[0]._fns[1].name == 'undocumented_function'
        assert self.parser._classes[0]._fns[2].name == 'documented_function'

    def test_fnDocstring_parsedCorrectly(self):
        assert self.parser._classes[0]._fns[0].doc
        assert self.parser._classes[0]._fns[1].doc
        assert len(self.parser._classes[0]._fns[1]._parameters) == 0
        assert len(self.parser._classes[0]._fns[0]._parameters) == 2
        assert self.parser._classes[0]._fns[0]._param_names == ['parameter1', 'parameter2']

    def test_fnDoc_areCorrect(self):
        correct_docs = ("\n        "
                        "PURPOSE\n        "
                        "-------\n\n        "
                        "TODO: Document purpose for function undocumented_function\n\n")

        assert correct_docs == self.parser._classes[0]._fns[1].doc

    def test_writesFile(self):
        self.parser.export()
        with open("test_files/test_input.py", 'r') as mod_file:
            mod_file_lines = mod_file.readlines()
            with open("test_files/correct_output.py", 'r') as correct_file:
                correct_file_lines = correct_file.readlines()
                for i in range(len(mod_file_lines)):
                    assert mod_file_lines[i] == correct_file_lines[i]


class TestManyRuns(TestDocstringWriterUtil):
    def test_formattingOverSeveralRuns(self):
        for i in range(6):
            parser = ModuleToDoc(abspath("test_files/test_input.py"))
            parser.export()
        with open("test_files/test_input.py", 'r') as mod_file:
            mod_file_lines = mod_file.readlines()
            with open("test_files/correct_output.py", 'r') as correct_file:
                correct_file_lines = correct_file.readlines()
                for i in range(len(mod_file_lines)):
                    assert mod_file_lines[i] == correct_file_lines[i]
        pass


class TestCmdLine(TestDocstringWriterUtil):
    def test_runPythonFromCmd(self):
        script_path = abspath("../std_doc/docstring_writer.py")
        system(f"\"{script_path}\" -f test_files/test_input.py")
        pass
        with open("test_files/test_input.py", 'r') as mod_file:
            mod_file_lines = mod_file.readlines()
            with open("test_files/correct_output.py", 'r') as correct_file:
                correct_file_lines = correct_file.readlines()
                for i in range(len(mod_file_lines)):
                    assert mod_file_lines[i] == correct_file_lines[i]

    def test_formattingOverSeveralRuns(self):
        for i in range(6):
            self.test_runPythonFromCmd()
        pass


if __name__ == '__main__':
    unittest.main()
