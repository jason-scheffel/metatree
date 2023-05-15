<!---
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
-->

<a name="TOP"></a>

<!-- BADGESDDSFKJ -->

<div align="center">

<!-- put sheilds here -->

</div>

<!-- PROJECT LOGO -->

<h3 align="center">
metatree
</h3>

metatree is a Python program that allows the user to recursively scrap metadata
from files and directories within a specified directory. The user is allowed to
specific patterns in which should be used to ignore certain files or
directories. It is not intended to follow the "suckless" philosophy of minimal
software. It is not intended to be an actually "good" program.

<!-- TABLE OF CONTENTS -->

<summary>Table of Contents</summary>
  <ol>
    <li><a href="#license">License</a></li>
    <li><a href="#Dependencies">Dependencies</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>

<!-- LICENSE -->

## License

This program is licensed under the following license(s):

- [AGPL-3.0-or-later](https://spdx.org/licenses/AGPL-3.0-or-later.html)
- [CC0-1.0](https://spdx.org/licenses/CC0-1.0.html)

The following file is an spdx document, which includes the specific license(s)
per file in this program:

- `~/spdx.spdx`

Furthermore, this program contains and uses dependencies. The specific
dependencies and their corresponding licenses can be viewed in the following
directory:

- `~/ort/output_docs`

Finally, the `~/LICENSES` directory includes the texts for the licenses used
for this program; additionally, the `~/ort/output_docs/NOTICE_DEFAULT` file
includes the texts for the licenses, along with other things, for the
dependencies of this program.

<p align="right"><<a href="#TOP">back to top</a>></p>

<!--Dependencies-->

## Dependencies

This section lists the dependencies for this program and a brief comment on why
the dependency exists. Note, this section only lists the top-level dependencies
for this program. Transitive dependencies or others are not listed. The
`~/ort/output_docs` folder may have more information regarding additional
dependencies.

| Dependency     | Reason                                            |
| -------------- | ------------------------------------------------- |
| stat           | Get data about files                              |
| exiftool       | Get data about files                              |
| tar            | To archive all the scrapped metadata              |
| alive-progress | Progress bar---scraping can take awhile sometimes |

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

The following are listed in alphabetical order with respect to the entities'
name:

The `~/ort/` directory and its contents were generated using
[ORT](https://github.com/oss-review-toolkit/ort).

The `~/LICENSES` directory and the `~/spdx.spdx` file were generated using
[reuse-tool](https://github.com/fsfe/reuse-tool).

<p align="right"><<a href="#TOP">back to top</a>></p>

<!-- blank -->
