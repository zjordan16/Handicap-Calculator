"""
This module is used to convert the requirements.txt file into a usable format for the pyproject.toml requirements list.

Input: requirements.txt file
Output: formatted_requirements.txt file
"""

import re
import os
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

# Function to adjust formatting to "libName>=version"
def format_requirements(requirements_content):
    formatted_requirements = []
    version_pattern = re.compile(r"(==|>=|<=|~=)")

    for line in requirements_content.strip().splitlines():
        match = version_pattern.search(line)
        if match:
            specifier = match.group(1)
            lib, version = line.split(specifier)
            formatted_requirements.append(f'"{lib.strip()}>={version.strip()}"')
        else:
            formatted_requirements.append(f'"{line.strip()}"')

    return formatted_requirements


def process_requirements_file():
    requirements_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../requirements.txt')
    formatted_output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../requirements_formatted.txt')

    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        return

    detected_encoding = detect_encoding(requirements_file)

    with open(requirements_file, 'r', encoding=detected_encoding) as file:
        requirements_content = file.read()

    formatted_requirements = format_requirements(requirements_content)

    formatted_output = ",\n".join(formatted_requirements)

    with open(formatted_output_file, 'w', encoding='utf-8') as file:
        file.write(formatted_output)

    print(f"Formatted requirements saved to {formatted_output_file}")


# Run the process
if __name__ == "__main__":
    process_requirements_file()
