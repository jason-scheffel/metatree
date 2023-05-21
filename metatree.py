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
import json
import os
import subprocess
import sys
import time
from argparse import Namespace

from argopt import argopt
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table


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
    args: Namespace,
    save_path: str,
    dir_count: int,
    file_count: int,
    other_stuff: dict,
):
    """
    Create the log file for the program.

    Contains information regarding stats about the directory to be scraped like
    how many folders are in it.

    Also contains information about the arguments used to run the program.
    """
    log_file_name = f"metatree_log_{other_stuff.get('Start Scrap Time')}.yml"
    log_file_path = os.path.join(save_path, log_file_name)

    with open(log_file_path, "w") as log_file:
        log_file.write(f"Date: {other_stuff.get('Start Scrap Time')}\n")

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

        log_file.write("\n")

        log_file.write("Other stuff:\n")
        log_file.write("\n")
        log_file.write(json.dumps(other_stuff, indent=2))

        log_file.write("\n")
        log_file.write("\n")
        log_file.write("\n")

        with open(__file__, "r") as this_file:
            log_file.write(this_file.read())


def get_file_info(file_name: str, exiftool: bool) -> dict:
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
        SEP = "{/~/}"
        format_options_file = {
            "%a": "permission bits in octal (note '#' and '0' printf flags)",
            "%A": "permission bits and file type in human readable form",
            "%b": "number of blocks allocated (see %B)",
            "%B": "the size in bytes of each block reported by %b",
            "%C": "SELinux security context string",
            "%d": "device number in decimal (st_dev)",
            "%D": "device number in hex (st_dev)",
            "%Hd": "major device number in decimal",
            "%Ld": "minor device number in decimal",
            "%f": "raw mode in hex",
            "%F": "file type",
            "%g": "group ID of owner",
            "%G": "group name of owner",
            "%h": "number of hard links",
            "%i": "inode number",
            "%m": "mount point",
            "%n": "file name",
            "%N": "quoted file name with dereference if symbolic link",
            "%o": "optimal I/O transfer size hint",
            "%s": "total size, in bytes",
            "%r": "device type in decimal (st_rdev)",
            "%R": "device type in hex (st_rdev)",
            "%Hr": "major device type in decimal, for character/block device special files",  # noqa
            "%Lr": "minor device type in decimal, for character/block device special files",  # noqa
            "%t": "major device type in hex, for character/block device special files",  # noqa
            "%T": "minor device type in hex, for character/block device special files",  # noqa
            "%u": "user ID of owner",
            "%U": "user name of owner",
            "%w": "time of file birth, human-readable; - if unknown",
            "%W": "time of file birth, seconds since Epoch; 0 if unknown",
            "%x": "time of last access, human-readable",
            "%X": "time of last access, seconds since Epoch",
            "%y": "time of last data modification, human-readable",
            "%Y": "time of last data modification, seconds since Epoch",
            "%z": "time of last status change, human-readable",
            "%Z": "time of last status change, seconds since Epoch",
        }
        format_options_fs = {
            "%a": "free_blocks_available_to_non_superuser",
            "%b": "total_data_blocks_in_file_system",
            "%c": "total_file_nodes_in_file_system",
            "%d": "free_file_nodes_in_file_system",
            "%f": "free_blocks_in_file_system",
            "%i": "file_system_ID_in_hex",
            "%l": "maximum_length_of_filenames",
            "%n": "file_name",
            "%s": "block_size_for_faster_transfers",
            "%S": "fundamental_block_size_for_block_counts",
            "%t": "file_system_type_in_hex",
            "%T": "file_system_type_in_human_readable_form",
        }

        cmd_file = [
            "stat",
            file_name,
            "--format",
            SEP.join(format_options_file.keys()),
        ]

        cmd_fs = [
            "stat",
            file_name,
            "--file-system",
            "--format",
            SEP.join(format_options_fs.keys()),
        ]

        # creates two dicts, new_stat_file and new_stat_fs.
        # The keys should be the description of the information
        # and the value should be the actual information

        # get the output of the stat command
        output_file = run_command(cmd_file).get("stdout")
        output_fs = run_command(cmd_fs).get("stdout")

        # split the output of the stat command
        output_file = output_file.split(SEP)  # type: ignore
        output_fs = output_fs.split(SEP)  # type: ignore

        # create a dict with the keys being the description of the information
        # and the value being the actual information
        new_stat_file = {}
        for key, value in zip(format_options_file.values(), output_file):
            new_stat_file[key] = value

        new_stat_fs = {}
        for key, value in zip(format_options_fs.values(), output_fs):
            new_stat_fs[key] = value

        return {"file": new_stat_file, "fs": new_stat_fs}

    def _get_exiftool():
        cmd = ["exiftool", file_name]
        output = run_command(cmd).get("stdout")

        """
        exiftool output looks like this:
        ExifTool Version Number         : 12.16
        File Name                       : IMG_20210101_000000.jpg
        ...

        We want to create a dict with the keys being the first part of the line
        """

        # split the output of the exiftool command
        output = output.split("\n")  # type: ignore

        # create a dict with the keys being the first part of the line
        # and the value being the rest of the line
        exiftool = {}
        for line in output:
            if line:
                key, value = line.split(":", 1)
                exiftool[key.strip()] = value.strip()

        return {"exiftool_hi": exiftool}

    def _get_other():
        other_stuff = {
            "Scrap Time": get_time(),
        }
        return {"other": other_stuff}

    return {
        "stat": _get_stat(),
        "exiftool": _get_exiftool() if exiftool else {},
        "other": _get_other(),
    }


def recreate_dir(args: Namespace) -> None:
    """
    Recreate the directory structure of the input directory in the output dir.
    """

    start_time = get_time()
    start_time_unix = time.time()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def _count_dirs() -> int:
        """
        Count the number of directories in the input directory.
        """
        num_dirs = 0
        for _, dirs, _ in os.walk(input_path):
            num_dirs += len(dirs)

        return num_dirs + 1

    def _count_files() -> int:
        """
        Count the number of files in the input directory.
        """
        num_files = 0
        for _, _, files in os.walk(input_path):
            num_files += len(files)

        return num_files

    num_folders = _count_dirs()
    num_files = _count_files()

    # bar stuff
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>4.0f}%"),
        TimeRemainingColumn(),
    )
    job_folder = job_progress.add_task("Folders", total=num_folders)
    job_file = job_progress.add_task("Files", total=num_files)

    job_total = sum(task.total for task in job_progress.tasks)  # type: ignore
    overall_progress = Progress()
    overall_task = overall_progress.add_task("All Jobs", total=int(job_total))

    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(
            overall_progress,
            title="Overall Progress",
            border_style="green",
            padding=(2, 2),
        ),
        Panel.fit(
            job_progress,
            title="[b]Folders/Dirs",
            border_style="red",
            padding=(1, 2),
        ),
    )

    with Live(progress_table, refresh_per_second=7):
        # Iterate through the input directory
        for root, dirs, files in os.walk(input_path):
            # Recreate the directory structure in the output directory
            relative_path = os.path.relpath(root, input_path)
            output_dir = os.path.join(output_path, relative_path)

            # Not sure if this is necessary
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Create a .json file with the parent directory's name
            parent_dir_name = os.path.basename(root)
            parent_json_file = f"PARENT_{parent_dir_name}.json"
            parent_json_path = os.path.join(output_dir, parent_json_file)

            # Put data in the .json file
            with open(parent_json_path, "w") as f:
                folder_data = get_file_info(root, False)
                json.dump(folder_data, f, indent=2)

            # Update the folder bar
            job_progress.update(job_folder, advance=1)
            completed = sum(task.completed for task in job_progress.tasks)
            overall_progress.update(overall_task, completed=completed)

            # Iterate through the files in the input directory
            for file_name in files:
                # Create a .json file with the file's name
                file_json_file = f"{file_name}.json"
                file_json_path = os.path.join(output_dir, file_json_file)

                file_path = os.path.join(root, file_name)

                # Put data in the .json file
                with open(file_json_path, "w") as f:
                    file_data = get_file_info(file_path, True)
                    json.dump(file_data, f, indent=2)

                # Update the file bar
                job_progress.update(job_file, advance=1)
                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)

    # put the log file in the output Directory

    end_time = get_time()
    end_time_unix = time.time()

    other_info = {
        "Start Scrap Time": start_time,
        "Start Scrap Time Unix": start_time_unix,
        "End Scrap Time": end_time,
        "End Scrap Time Unix": end_time_unix,
        "Elapsed Time (h)": (end_time_unix - start_time_unix) / 3600.0,
    }

    create_log_file(args, output_path, num_folders, num_files, other_info)


def main(args: Namespace) -> None:
    recreate_dir(args)


def check_args(args: Namespace) -> None:
    # Check that the input directory exists
    if not os.path.exists(args.input):
        print(f"The input directory '{args.input}' does not exist.")
        sys.exit(1)


def tar_dir(args: Namespace) -> None:
    pass


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
