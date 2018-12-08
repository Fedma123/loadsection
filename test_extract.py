import unittest
from extract import extract_section_from_file_given_jupyter_line
import exceptions
import unittest.mock
from parameterized import parameterized

class BaseFileSection:
    raw_content = ""
    expected_sections = {}

class MissingEndOfSectionFile:
    raw_content = """
    Line above section
    # SECTION miss BEGIN
    Line at the end of file
    """

class CorrectFileContentWithEmptySection:
    raw_content =  """
    This is a line above the section
    # SECTION empty BEGIN
    # SECTION empty END"""

    expected_sections = {
        "empty": ""
    }


class CorrectFileContentWithOneSection:
    raw_content =  """
    This is a line above the section
    # SECTION 1 BEGIN
    line in between 1
    line in between 2
    # SECTION 1 END"""

    expected_sections = {
        "1": """    line in between 1
    line in between 2\n"""
    }
        
    
class CorrectFileContentWithTwoSections:    
    raw_content = """
    This is a line above the section
    # SECTION alpha BEGIN
    line 1 in alpha section
    line 2 in alpha section
    # SECTION alpha END
    other lines not in sections
    # SECTION beta BEGIN
    line 1 in beta section
    line 2 in beta section
    # SECTION beta END
    """

    expected_sections = {
        "alpha": """    line 1 in alpha section
    line 2 in alpha section\n""",

        "beta":  """    line 1 in beta section
    line 2 in beta section\n"""
    }

class Test_Extract(unittest.TestCase):

    def test_if_line_is_empty_then_raises_empty_line_exception(self):
        with self.assertRaises(exceptions.EmptyLineException):
            extract_section_from_file_given_jupyter_line("")

    def test_if_line_has_one_argument_then_raises_arguments_amount_exception(self):
        with self.assertRaises(exceptions.ArgumentsAmountException):
            extract_section_from_file_given_jupyter_line("arg") 
    def test_if_line_has_more_than_2_args_then_raises_argument_amount_exception(self):
        with self.assertRaises(exceptions.ArgumentsAmountException):
            extract_section_from_file_given_jupyter_line("arg1 arg2 arg3")

    @parameterized.expand([
        ("1", "some_file.py",
         CorrectFileContentWithOneSection.raw_content,  
         CorrectFileContentWithOneSection.expected_sections["1"]
        ),
        ("alpha", "some_other_file.py",
         CorrectFileContentWithTwoSections.raw_content,
         CorrectFileContentWithTwoSections.expected_sections["alpha"]
        ),
        ("beta", "some_other_file.py",
         CorrectFileContentWithTwoSections.raw_content,
         CorrectFileContentWithTwoSections.expected_sections["beta"]
        ),
        ("empty", "some_empty_section_file.py",
         CorrectFileContentWithEmptySection.raw_content,
         CorrectFileContentWithEmptySection.expected_sections["empty"]
        )
    ])
    def test_if_file_has_specified_section_then_returns_lines_in_between(self, section, file_name, raw, expected):
        m = unittest.mock.mock_open(read_data=raw)
        result = ""
        jupyter_line = section + " " + file_name
        with unittest.mock.patch('builtins.open', m) as mp:            
            result = extract_section_from_file_given_jupyter_line(jupyter_line)

        self.assertEqual(result, expected)

    def test_if_file_does_not_have_end_of_section_then_raises_missing_end_of_section(self):
        m = unittest.mock.mock_open(read_data=MissingEndOfSectionFile.raw_content)
        with self.assertRaises(exceptions.MissingEndOfSection, kwargs="miss"):
            with unittest.mock.patch('builtins.open', m) as mp:
                extract_section_from_file_given_jupyter_line("miss missing.py")