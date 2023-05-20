"""
SPDX-FileCopyrightText: 2023 Jason Scheffel <contact@jasonscheffel.com>
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (C) 2023 Jason Scheffel

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import subprocess
import time
from argparse import Namespace

from alive_progress import alive_bar, config_handler
from argopt import argopt

# temp location, ill figure something out later
config_handler.set_global(length=79, spinner="classic", bar="classic")


def run_command(cmd: list[str]) -> dict[str, str | int]:
    """
    Run a command the return the stdout, stderr, and returncode.
    """
    cmd_out = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return {
        "stdout": cmd_out.stdout,
        "stderr": cmd_out.stderr,
        "returncode": cmd_out.returncode,
    }


def get_time() -> str:
    """
    Get the current time in the specified format and return it.
    """
    return time.strftime("%Y-%m-%d-%Z %H:%M:%S", time.localtime())


def create_log_file(
    args: Namespace, save_path: str, dir_count: int, file_count: int
) -> None:
    """
    Create the log file for the program.

    Contains information regarding stats about the directory to be scraped like
    how many folders are in it.

    Also contains information about the arguments used to run the program.
    """
    log_file_name = f"metatree_log_{get_time()}.yml"
    log_file_path = os.path.join(save_path, log_file_name)

    with open(log_file_path, "w") as log_file:
        log_file.write(f"Date: {get_time()}\n")

        log_file.write("\n")

        log_file.write(f"Input Directory: {args.input}\n")
        log_file.write(f"Output Directory: {args.output}\n")
        log_file.write(f"Log File: {log_file_path}\n")

        log_file.write("\n")

        log_file.write(f"Absolute number of Folders: {dir_count}\n")
        log_file.write(f"Absolute number of Files: {file_count}\n")
        log_file.write(f"Final number of Folders: {dir_count}\n")
        log_file.write(f"Final number of Files: {file_count}\n")

        log_file.write("\n")

        log_file.write(f"Used arguments: {args}\n")

        log_file.write("#")


def get_file_info(args: Namespace, file_name: str) -> dict:
    """
    Defining a file as a file or directory.

    Returns a dictionary containing information regarding the file.

    The key is what program is used to get the information and the value
    is the actual information.
    """

    def _get_stat():
        """
        Get the information from the stat command.
        """
        pass

    def _get_exiftool():
        """
        Get the information from the exiftool command.
        """
        pass

    return {}


def recreate_dir(args: Namespace, input_path: str, output_path: str) -> None:
    """
    Recreate the directory structure of the input directory in the output dir.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # get the amount of folders in the input directory
    # including the input directory itself too :)
    num_folders = run_command(
        ["find", input_path, "-type", "d", "-print", "|", "wc", "-l"]
    ).get("stdout")

    # get the number of files in the input directory
    num_files = run_command(
        ["find", input_path, "-type", "f", "-print", "|", "wc", "-l"]
    ).get("stdout")

    # ignore type because we know it will be an int.
    num_folders = int(num_folders)  # type: ignore
    num_files = int(num_files)  # type: ignore

    # put the log file in the output Directory
    create_log_file(args, output_path, num_folders, num_files)

    with alive_bar(num_folders, title="Folders") as folders_bar:
        # Iterate through the input directory
        for root, _, files in os.walk(input_path):
            # Recreate the directory structure in the output directory
            relative_path = os.path.relpath(root, input_path)
            output_dir = os.path.join(output_path, relative_path)

            # Not sure if this is necessary
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Create a .yml file with the parent directory's name
            parent_dir_name = os.path.basename(root)
            parent_yml_file = f"PARENT_{parent_dir_name}.yml"
            parent_yml_path = os.path.join(output_dir, parent_yml_file)
            open(parent_yml_path, "w").close()

            # Update the progress bar for folders
            folders_bar()

    with alive_bar(num_files, title="Files") as files_bar:
        # Iterate through the files in the input directory
        for root, _, files in os.walk(input_path):
            for file in files:
                # Add .yml to the end of the file names
                # and create empty files in the output directory
                new_file_name = f"{file}.yml"
                new_file_path = os.path.join(output_dir, new_file_name)
                open(new_file_path, "w").close()

                # Update the progress bar for files
                files_bar()


def main(args: Namespace) -> None:
    recreate_dir(args, args.input, args.output)


def docstring() -> str:
    return """Hello

Usage:
    metatree.py <input> <output>

Arguments:
    -h, --help            Show this help message and exit.
    -v, --version         Show program's version number and exit.

This program requires, or optionally 'requires' other software.

Such software is listed in the README.md file that accompanies this program;
additionally, a copy of the said file can be found at:
<https://git.sr.ht/~jason-scheffel/metatree>.

SPDX-FileCopyrightText: 2023 Jason Scheffel <contact@jasonscheffel.com>
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (C) 2023 Jason Scheffel

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""


if __name__ == "__main__":
    __version__ = "0.1.0"
    parser = argopt(docstring(), version=__version__)
    arguments = parser.parse_args()
    main(arguments)

#
