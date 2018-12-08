
class EmptyLineException(Exception):
    def __init__(self):
        super().__init__("Line cannotbe empty")

class ArgumentsAmountException(Exception):
    def __init__(self):
        super().__init__("2 arguments are needed")

class MissingEndOfSection(Exception):
    def __init__(self, section_name):
        super().__init__("Missing end of section " + section_name)