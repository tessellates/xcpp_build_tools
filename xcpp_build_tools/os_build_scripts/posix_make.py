import json
import os
import subprocess


def configure_target(target, build_dir, bcmake_configure_command) -> None:
    cmake_configure_command = bcmake_configure_command.copy()
    target_build_dir = os.path.join(build_dir, target['name'])
    if not os.path.exists(target_build_dir):
        os.makedirs(target_build_dir)
    cmake_configure_command.extend(["-S", target['path'], "-B", target_build_dir])
    print(f"Configuring {target['name']}: {' '.join(cmake_configure_command)}")
    subprocess.run(cmake_configure_command, check=True)

def build_target(target, build_dir, bcmake_build_command) -> None:
    cmake_build_command = bcmake_build_command.copy()
    target_build_dir = os.path.join(build_dir, target['name'])
    cmake_build_command.extend(["--build", target_build_dir, "--", "-j8"])
    print(f"Building {target['name']}: {' '.join(cmake_build_command)}")
    subprocess.run(cmake_build_command, check=True)

def run_target(target, build_dir, myenv) -> None:
    target_app_dir = os.path.join(build_dir, target['name'])
    try:
        cmd = os.path.join(".", target_app_dir, "main")
        subprocess.Popen( cmd, shell = True, env=myenv )
        print(f"Ran '{cmd}'")
        return
    except Exception as e:
        pass
    
    try:
        cmd = os.path.join(".", target_app_dir, target['exe'])
        subprocess.Popen( cmd, shell = True, env=myenv )
        print(f"Ran '{cmd}'")
        return
    except Exception as e:
        pass

    print(f"Failed to run {target['name']} no valid 'exe' value or not named default value: 'main'")