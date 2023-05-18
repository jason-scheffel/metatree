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

The main license for this program is:

- [AGPL-3.0-or-later](https://spdx.org/licenses/AGPL-3.0-or-later.html)

Some files, however, may be licensed under the following license(s):

- [CC0-1.0](https://spdx.org/licenses/CC0-1.0.html)

The following file is an spdx document, which includes the specific license(s)
per file in this program:

- `~/reuse.spdx`

Finally, the `~/LICENSES` directory includes the licenses used for this
program.

<p align="right"><<a href="#TOP">back to top</a>></p>

<!--Dependencies-->

## Dependencies

This program requires, or optionally 'requires' the following software:

<center>

| Software           | License                               | Type                      |
| :----------------- | :------------------------------------ | ------------------------- |
| stat\*             | GPL-3.0-or-later                      | Program                   |
| exiftool\*         | GPL-1.0-or-later OR Artistic-1.0-Perl | Program                   |
| tar\*              | GPL-3.0-or-later                      | Program                   |
| Python\*           | 0BSD AND PSF-2.0                      | Program                   |
| alive-progress\*\* | MIT                                   | Python Package            |
| argopt\*\*         | MPL-2.0                               | Python Package            |
| about-time\*\*\*   | MIT                                   | Python Transitive Package |
| grapheme\*\*\*     | MIT                                   | Python Transitive Package |

</center>

```
* denotes a system program

** denotes a Python package

*** denotes a Python transitive package
```

If you would like a list that includes where to view the source code of each
program and where to view a copy of the relevant license(s), then:

- A link to the source code pertaining to each software can be viewed in the
  `~/depend-info.txt` file.
- The license text files can be viewed in the `~/LICENSES` directory.
- You may also view the aforementioned files and directories at
  <https://sr.ht/~jason-scheffel/metatree/>.

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

The following are listed in alphabetical order with respect to the entities'
name:

The `~/LICENSES` directory and the `~/reuse.spdx` file were generated using
[reuse-tool](https://github.com/fsfe/reuse-tool).

<p align="right"><<a href="#TOP">back to top</a>></p>

<!-- blank -->
