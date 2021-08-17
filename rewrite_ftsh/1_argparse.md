---
title: Creating a command-line script with arguments
parent: Rewriting ft.sh
nav_order: 1
---

## Goals

* Explain the purpose of the script
* Accept user input for the file path of the digital carrier
* Accept user input for the Media ID number (M######-####)

## Anatomy of a script

Many Python tutorials start in a Python interpreter, an environment where every block of code is executed once you press enter.
This is much like how bash commands work when using a terminal or shell.
Our goal is to create scripts, so we'll start with scripts instead.

For scripts that implement a strict, sequential procedure, the code can be organized with the same procedural order.
When writing bash scripts, that means that the final script can look like a series of commands that could have been run in a terminal one-by-one.
Grouping them into a script automates the process of entering those lines.

However, a good script is more than a recording of a command-line session.
Good practice means making sure that the script will be executed the same way everytime, and that you record any of your goals and logic for structuring the script as you did.

The first lines of `ft.sh` demonstrate some of these practices:

```bash
#!/bin/bash

#This is a program to create Siegfried metadata, bags and validation for file transfers.
#Check that sf conf file is set properly

BLUE='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}This script will create a file transfer.${NC}"
echo -e "${BLUE}Please drag the SIP folder over this window. See the folder path displayed? Hit return!:${NC}"

read FT
```

`#!/bin/bash` is known as a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)).
The line tells the computer which interpreter to use to interpret the rest of the code in the script.
This line isn't strictly necessary, but it is good practice.
For Python, we'll be using the following shebang.
`#!/usr/bin/env python3`

The `# ....` lines describe what this script does.
Every script should have a description of its purpose.
Python uses the same `# ...` syntax for comments, so we could mimic this method.
However, how would a user not familiar with this script know what it does?

If they were familiar with bash scripting, they could print out the script with a `cat` command or open it in a text editor to see this comment.
If they were adventurous, they could run the script and hope it explains its purpose before doing any major changes.
This script anticipates that method with its first `echo` line.
To make something more user friendly, we could have help information.
For example:

```bash
> ft.sh -h
# This is a program to create Siegfried metadata, bags and validation for file transfers.
#Check that sf conf file is set properly
```

We'll cover how to do that in Python.

The `read FT` is where the procedural portion of this code starts.
After executing that line, the terminal waits for a user to input a filepath and press enter, before running the next line in the script.

From a user perspective, it would be nice to use command line arguments instead of prompts.
When running this code, we'd only have to write a single line before the computer takes over.
That also means that we could quickly alter that line to transfer from a different carrier or to correct a typo.
For example:

```bash
> ft.sh --source /path/to/carrier_1 --id M12345_0001
> ft.sh --source /path/to/carrier_2 --id M12345_0002
```

## A Python ft.sh

After examining `ft.sh` our goal is to create a Python script that:

* uses a shebang
* includes a description and help function that a user can access with `-h`
* accepts arguments using the flags `--source` and `--id`

### Creating and running a python script

A python script is a text file with python code.
Typically, it has a `.py` file extension, although this isn't required.
So to create a script,

1. Open a text editor
2. Add Python code: `print('Hello world')
3. Save the file to your Desktop as `ft.py`

To run this script,

1. Open a terminal
2. Use the python interpreter to run the file `python ~/Desktop/ft.py`

### Making an executable python script

Ideally we wouldn't have to type `python` every time we want to use this script.
That's the role of the shebang.
But by default for security reasons, a computer does not allow any file to be executed.
We have to change the mode of a script file to allow it to be executed.

1. In the text editor, add `#!/usr/bin/env python3` as the first line of `ft.py`
2. Save `ft.py`
3. In the terminal, CHange the MODe of the script to executable `chmod +x ~/Desktop/ft.py`
4. Run the file `~/Desktop/ft.py`

#### Current executable script file

```py
#!/usr/bin/env python3

print('Hello world')
```

### Making more functions available

By default, Python has about 75 built-in functions like `print()`, `input()`, and `compile()`.
Most of these are too unspecific to perform the tasks that we want.

Python also has over 200 built-in modules in its standard library that each contain tens or hundreds of additional functions for more specific purposes like manipulating accessing file systems (`os`), working with time data (`datetime`), and parsing arguments from command-line interfaces (`argparse`).

Each of these modules is composed of multiple script files.
To use a function defined in a module, the Python interpreter has to load that module.
To minimize the amount of time spent loading modules that may not be used, Python does not load any modules by default.

Importing `argparse` makes its functions available.
To learn how to use it, or any Python module, it's helpful to head to the module's documentation.
The [documentation for argparse](https://docs.python.org/3/library/argparse.html) follows the standard documentation structure for all standard library modules.

First, there is a minimal working example using good stylistic practice.
You can copy paste this code yourself to test it out.

Next, major concepts of the module are explained and illustrated with examples.
These concepts are typically arranged in order of common usage.
For `argparse`, the concepts are:

* the `ArgumentParser` object
* the `add_argument()` method
* the `parse_args()` method
* other tools in the module

This type of documentation is often not read from start to finish, but skimmed and referenced as needed.
Using `cmd+f` to jump to other portions of the page is frequently helpful.

### Adding a help function

#### Import the module

As shown in the initial example from the documentation, we need to first load `argparse` using an `import` statement. In general, all `import` statements should be at the beginning of a script, after a shebang.

* Add `import argparse` after the shebang.

#### Create an ArgumentParser

After loading, `argparse` we can use the tools in the module.
Whenever using code from a module, reference that code with the name of the module.
This tells the Python interpreter which specific piece of code to use.
For example, there is a built-in `open()` function and an `open()` function in the `gzip` module.
To tell Python to open a file using the gzip compression algorithm, we have to use the specifically call the `gzip.open()`.

Similarly, *to create an `ArgumentParser` object, we have to call `argparse.ArgumentParser()`

The `ArgumentParser` object takes a description.
According to the [documentation](https://docs.python.org/3/library/argparse.html#description), this is used to describe the purpose of the program.

Because we are creating an object and would like to change it and reference it, we store it to a variable.

* Add `parser = argparse.ArgumentParser(description='Create Siegfried metadata, bag files from a carrier, and validate bagging for file transfers')` after the import statement.

#### Parse the arguments

Finally, the data stored in the `ArgumentParser` needs to be processed.
For this, `ArgumentParser` objects have a method called `parse_args()`.
The results of this method also have to be stored.

* Add `args = parser.parse_args()` after the `parser = ...` line.
* Save the script
* In the terminal, test the script `~/Desktop/ft.py -h`

#### Current script file with help

```py
#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Create Siegfried metadata, bag files from a carrier, and validate bagging for file transfers')

args = parser.parse_args()

print('Hello world')
```

### Parsing command line arguments

One of the reasons we had to store the `ArgumentParser` to a variable is because we want to store more arguments.
The documentation example shows two arguments added with the `add_argument()` method.

#### Adding an argument to the parser

All of the arguments are being stored in the `ArgumentParser` object stored as `parser`.
The `add_argument()` method updates that object with new data.
Unlike in previous lines, we don't need to create a variable to store this data because the method adds it to the object that it is called from.

The powerful thing about `add_argument()` is the number of modifications we can make using the arguments in the method.
We'll review a few of the more usability focused modifications.

#### Argument names

The first argument(s) in the method are the names of the argument.
These can take 3 forms.

1. a positional argument (e.g. `ft.py path/to/file`)
2. a one-character flagged argument (e.g. `ft.py -s path/to/file`)
3. a multi-character flagged argument (e.g. `ft.py --source path/to/file`)

It's possible to give an argument multiple allowable flags, (e.g. `parser.add_argument('-s', '--source')`)

#### Optional arguments

By default, flagged arguments are assumed to be options.
If you want to require that flag, add `required=True` (e.g.`parser.add_argument('--source', required=True)`)

#### Arguments help

It is often useful to explain the expected input for an argument.
To do this, add `help='...'` (e.g.`parser.add_argument('--source', help='path to the carrier media')`)

#### Usage help

The dummy inputs in the usage instructions can also be updated.
To do this, add `metavar='...'` (e.g.`parser.add_argument('--source', metavar='path/to/carrier')`)

#### Adding everything together

`ft.sh` required 2 inputs

* the path to the source media
* the Media ID number

In addition to defining these two inputs as argument, we can increase our usability by updating the help text for each.

* After `parser = ...` add the following.

```py
parser.add_argument('--source', required = True,
help='path to the root of the digital carrier', metavar='path/to/carrier')
parser.add_argument('--id', required = True,
help='media id assigned to the digital carrier', metavar='M######_####')
```

* In the terminal, test the script through each scenario.
  * Run the script with the help flag.
  * Run the script without any argument.
  * Run the script with all required arguments

## A Skeleton Script

At this point, it may feel like `ft.py` doesn't really accomplish anything.
However, parsing arguments sets up the rest of any script.
By first defining all of the user input that we need, we make it easy to understand what data we'll have available later in the script.

We can make improvement to this skeleton.
For example, we could validate that the file path exists or that the media id is formatted correctly.
The [`type` argument](https://docs.python.org/3/library/argparse.html#type) is one method to do this.
We'll return to these ideas as we explore more of Python.
For the next lesson, we'll focus on using the input within the script.

### Current script with arguments

```py
#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--source', required = True,
help='path to the root of the digital carrier', metavar='path/to/carrier')
parser.add_argument('--id', required = True,
help='media id assigned to the digital carrier', metavar='M######_####')

args = parser.parse_args()

print('Hello world')
```
