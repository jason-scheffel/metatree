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

from alive_progress import alive_bar
from argopt import argopt


def run_command(command: list[str]) -> str:
    return subprocess.check_output(command).decode("utf-8")


def get_time() -> str:
    return time.strftime("%Y-%m-%d-%Z %H:%M:%S", time.localtime())


def recreate_dir(input_path: str, output_path: str) -> None:
    if not os.path.exists(output_path):
        os.makedirs(output_path)

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

        # Iterate through the files in the input directory
        for file in files:
            # Add .yml to the end of the file names
            # and create empty files in the output directory
            new_file_name = f"{file}.yml"
            new_file_path = os.path.join(output_dir, new_file_name)
            open(new_file_path, "w").close()


def main(args: Namespace) -> None:
    recreate_dir(args.input, args.output)


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
    args = parser.parse_args()
    main(args)

#
