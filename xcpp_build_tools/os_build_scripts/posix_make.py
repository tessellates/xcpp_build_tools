import json
import os
import subprocess


def configure_target(target, target_dir, bcmake_configure_command) -> None:
    cmake_configure_command = bcmake_configure_command.copy()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    cmake_configure_command.extend(["-S", target['path'], "-B", target_dir])
    print(f"Configuring {target['name']}: {' '.join(cmake_configure_command)}")
    subprocess.run(cmake_configure_command, check=True)

def build_target(target, target_dir, bcmake_build_command) -> None:
    cmake_build_command = bcmake_build_command.copy()
    cmake_build_command.extend(["--build", target_dir, "--", "-j8"])
    print(f"Building {target['name']}: {' '.join(cmake_build_command)}")
    subprocess.run(cmake_build_command, check=True)

def run_target(target, target_dir, myenv) -> None:
    try:
        cmd = os.path.join(".", target_dir, "main")
        subprocess.Popen( cmd, shell = True, env=myenv )
        print(f"Ran '{cmd}'")
        return
    except Exception as e:
        pass
    
    try:
        cmd = os.path.join(".", target_dir, target['exe'])
        subprocess.Popen( cmd, shell = True, env=myenv )
        print(f"Ran '{cmd}'")
        return
    except Exception as e:
        pass

    print(f"Failed to run {target['name']} no valid 'exe' value or not named default value: 'main'")