import exceptions

def extract_section_from_file_given_jupyter_line(line):
    if line == "":
        raise exceptions.EmptyLineException()

    args = line.split()
    if len(args) != 2:
        raise exceptions.ArgumentsAmountException()

    section = args[0]
    begin_section_str = "# SECTION " + section + " BEGIN"
    end_section_str = "# SECTION " + section + " END"
    filename = args[1]

    lines = []
    extracted_lines = ""
    inside_wanted_section = False
    with open(filename, "r") as f:
        lines = f.readlines()

    for current_line in lines:
        if begin_section_str in current_line:
            inside_wanted_section = True
            continue
        elif inside_wanted_section and end_section_str in current_line:
            inside_wanted_section = False
            break
        
        if inside_wanted_section:
            extracted_lines += current_line

    if inside_wanted_section:
        raise exceptions.MissingEndOfSection(section)
        
    return extracted_lines