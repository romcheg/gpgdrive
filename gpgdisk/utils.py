import os
import subprocess


def get_full_path(self, partial):
    if partial.startswith("/"):
        partial = partial[1:]
    path = os.path.join(self.root, partial)

    return path


def execute(cmd):
    """Executes a command

    :return: (exit_code, stdout, stderr)

    """
    obj = subprocess.Popen(cmd.split(' '))
    stdout, stderr = obj.communicate()
    ret_code = obj.returncode

    return ret_code, stdout, stderr
