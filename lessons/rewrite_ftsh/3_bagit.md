---
title: Using bagit-python in Python
parent: Rewriting ft.sh
nav_order: 3
---

## Goals

* Creating file fixtures to test file manipulations
* Using bagit-python within a python script

## Bagging Requirements

`bagit-python` is most commonly used as a command-line tool, `bagit.py --validate path/to/bag`.
However, that shell tool is itself a Python script, with classes and functions you can import into other Python scripts.

This was the same case as `bagit-java` which was used in `ft.sh`.
Part of the reason for rewriting `ft.sh` was that `bagit-java` removed its command-line interface.
That meant that we would either have to maintain an out-of-date version of `bagit-java`, rewrite `ft.sh` as a Java applet, or switch to another `bagit` tool.
As long as we were switching to `bagit-python` we might as improve `ft.sh` as well.

Our goal in using `bagit-python` is to have a structure that holds fixity information that we can reuse when we return to a project, weeks or months later.
We'd like for the fixity information to be generated from the original file from the media.
And we'd like to know if anything went wrong during the transfer.

So for bagging, we have a few requirements.

1. transfer the files from the carrier to the destination
2. package files into a bag
3. report if there were any files left behind
4. report the number and total size of the files

