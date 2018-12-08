from IPython.core.magic import Magics, magics_class, line_magic
from IPython import get_ipython
from extract import extract_section_from_file_given_jupyter_line

@magics_class
class MyMagics(Magics):

    @line_magic
    def loadsection(self, line):
        extracted_lines = extract_section_from_file_given_jupyter_line(line)
        self.shell.set_next_input('# %loadsection {}\n{}'.format(line, extracted_lines), replace=True)

ip = get_ipython()
ip.register_magics(MyMagics)