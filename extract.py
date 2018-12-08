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
    extracted_lines = []
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
            extracted_lines.append(current_line)

    if inside_wanted_section:
        raise exceptions.MissingEndOfSection(section)

    min_indentation_among_lines = 0xFFFFFFFF    
    for line in extracted_lines:
        stripped_line = line.lstrip(" \t")
        current_line_indentation = len(line) - len(stripped_line)

        if current_line_indentation < min_indentation_among_lines:
            min_indentation_among_lines = current_line_indentation
        
        if current_line_indentation == 0:
            break

    result = ""
    if min_indentation_among_lines == 0:
        good_lines = extracted_lines
    else:
        good_lines = []
        for line_to_strip in extracted_lines:
            good_lines.append(line_to_strip[min_indentation_among_lines:])

    return str().join(good_lines)