# cmake_utils.py
import os

def find_cmake_projects(start_path) -> list:
    targets = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        if 'CMakeLists.txt' in files:
            cmake_path = os.path.join(root, 'CMakeLists.txt')
            project_name = parse_project_name(cmake_path)
            if project_name:
                # Convert the absolute path to a relative path
                relative_path = os.path.relpath(root, start_path)
                targets.append({"name": project_name, "path": relative_path})
    return targets

def parse_project_name(file_path) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('project('):
                # Extracting the project name, considering potential VERSION specifier
                components = line.split('project(')[1].split(')')[0].split()
                if components:
                    return components[0].strip('"').strip("'")
    return ""
