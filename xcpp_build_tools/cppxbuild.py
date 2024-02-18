import argparse
import json
import os
import shutil
from . import cmake_utils
from . import utilx
from .os_build_scripts import posix_make as mkx
#from os_specific import build_ops

class XBuild:
    def __init__(self) -> None:
        self.config_file = 'cppxbuildconfig.json'
        self.config = None
        self.cmake_build_command = None
        self.cmake_configure_command = None
        self.run = False
        self.do_build = True
        self.myenv = myenv = dict(os.environ)

    def _load_config(self) -> None:
        if not os.path.exists(self.config_file):
            raise utilx.MissingFileError(self.config_file, "build.py setup_default")
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)

        self.build_type_dir = self.config['debugdir'] if self.config['currentConfig'] == 'debug' else self.config['optdir']
        self.build_dir = self.config['builddir']
        self._generate_cmake_commands()

        for envvars in self.config['env']:
            myenv[envvars['name']] = envvars['value'] # Change this to a different driver!

    def _target_dir(self, target) -> str:
        return os.path.join(self.build_dir, target['path'], self.build_type_dir)
    
    def _generate_cmake_commands(self): 
        self.cmake_configure_command = [self.config['cmake']]
        for variable in self.config['default_cmake_variables']:
            self.cmake_configure_command.append(f"-D{variable['name']}={variable['value']}")

        self.cmake_build_command = [self.config['cmake']]

    def _apply_action(self, action):
        self.cmake_configure_command.append(f"-D{action['value']}")

    def _get_or_create_config(self) -> dict:
        if not os.path.exists(self.config_file):
            # Find CMakeLists.txt files and parse project names
            targets = cmake_utils.find_cmake_projects(os.getcwd())
            default_config = {
                "cmake":"cmake",
                "currentConfig":"opt",
                "builddir": "build",
                "debugdir": "Debug",
                "optdir": "Release",
                "targets": targets,
                "cmake_actions": [],
                "default_cmake_variables" : [], 
                "env": []
            }
            with open(self.config_file, 'w') as file:
                json.dump(default_config, file, indent=4)
        else:
            print("Config file already exists!")
    def handle_arguments(self, args):
        if not args:
            print("No args")
            return

        if 'no-build' in args:
            self.do_build = False
            args.remove('no-build')

        if 'run' in args:
            self.run = True
            args.remove('run')

        if 'setup_default' in args:
            self._get_or_create_config()
            args.remove('setup_default')

        self._load_config()

        if 'clean' in args:
            self.clean_build_directory()
            args.remove('clean')
        
        if 'all' in args:
            self.build_all_targets()
            args.remove('all')
        
        for arg in args:
            # Attempt to find a matching target
            target = next((t for t in self.config['targets'] if t['name'] == arg), None)
            if target is not None:
                self.build_target(target)
                continue  # Proceed to the next arg

            # Attempt to find a matching action
            action = next((a for a in self.config['cmake_actions'] if a['name'] == arg), None)
            if action is not None:
                self.apply_action(action)
                continue  # Proceed to the next arg

            # If neither, print an error
            print(f"Invalid argument: {arg}")


    def clean_build_directory(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
            print(f"Cleaned build directory: {self.build_dir}")

    def build_target(self, target):
        target_dir = self._target_dir(target)
        if self.do_build:
            mkx.configure_target(target, target_dir, self.cmake_configure_command)
            mkx.build_target(target, target_dir, self.cmake_build_command)
        if self.run:
            self.run_target(target, target_dir)

    def build_all_targets(self):
        for target in self.config['targets']:
            self.build_target(target)

    def run_target(self, target, target_dir):
        mkx.run_target(target, target_dir, self.myenv)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Build system for C++ projects using CMake.")
    parser.add_argument('commands', nargs='*', help="Commands, targets to build, or actions to apply. Use 'all' to build all targets.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    xbuild = XBuild()
    xbuild.handle_arguments(args.commands)
