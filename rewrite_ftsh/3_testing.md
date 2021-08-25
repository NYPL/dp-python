---
title: Test-driven Development
parent: Rewriting ft.sh
nav_order: 2
---

Scripts perform the same action repeatedly.
This means they also perform the same mistake repeatedly.
Test-driven development is a method to pre-emptively address these potential mistakes before they become bugs.

Test-driven development requires a few additions to our scripting process.

1. transforming our script requirements into Python code that we can test the script against
2. creating additional to cover gaps in our requirements
3. writing our script in a way that it can be tested

This may seem like a lot of overhead.
However, this overhead encourages good coding practices like defining functions and handling errors.

We can start with the basic question of how to write a test.
That starts from our functional requirements.
Each of our functional requirements should have some expected behaviors.

The last module ended asking what to do if we type in the media ID for an item that has already been transferred.
Ideally, the script would quit and tell the user why it was stopping.
That makes for two tests, one where a folder is created as expected, and a second where the script errors out.
In Python pseudo-code that might look like this.

```py test_ft.py
def test_no_errors():
    # run ft.py --id M1234-0001
    # expect to find xfer_path/M1234/M1234-0001

def test_error_if_dest_path_exists():
    # create xfer_path/M1234/M1234-0001
    # run ft.py --id M1234-0001
    # expect ft.py to quit
    # expect ft.py to report "Media may have been transferred, make sure that the entered ID is correct"
```

First, we haven't worked with this `def ....():` syntax before.
Each `def` block defines a function.
The name of the function is the string that starts after the space.
That string is followed by a pair of parenthese where arguments can be defined for the function.
The function definition is finished by a `:`.
Every indented line that follows the first line is part of the function.
The function definition is ended by a blank line followed by unindented code.

Functions are useful because they break up a long script into modular, reuseable chunks.
Right now we're defining functions for our tests, but you can also imagine how functions might impact our script.
For each of these tests, there is a line `run ft.py --id M1234-0001` that will perform every action the script performs.
These tests are only interested in those few lines of the script that create the transfer folders.
It would be more efficient if the test could be more specific.

```py test_ft.py
def test_no_errors():
    # ft.create_transfer_folders(media_id='M1234-0001')
    # expect to find xfer_path/M1234/M1234-0001
```

This test assumes that there is a function in ft.py with the sole purpose of creating folders according to our rules.
Now instead of having to test run the entire script, we can examine just this one component.

Testing is one benefit to writing functions.
Some of the other benefits include:

* abstracting a script into components instead of a long line of code
* creating reuseable components that you can call multiple times in a script
* making discrete components that you can extend or improve
* allowing you to hide complicated or wordy bits in a different part of your script

### Functional-izing `ft.py`

So far `ft.py` has been a sequential list of Python lines.
When the Python interpreter starts, it reads and executes each consecutive line of code.
We'll reorganize this so that the Python interpreter first loads a set of functions, and then executes those functions in the order we define.

The first step to this process is defining a `main()` function.
In practice, most programmers would assume that whatever code is defined within `main()` is the central purpose of the script.
To add our existing code to a `main()` function, insert `def main():` before the first line of code after the import statements.
Then indent all lines of the following lines of code.
(In VS Code you can highlight everything and press `<tab>`)

If you try to run this new version of `ft.py`, nothing will happen.
The Python interpreter loaded the script including `main()`, but no part of the script told the interpreter to run `main()`

The other common practice that you'll see for scripts is a couple lines at the very end.

```py
if __name__ == '__main__':
    main()
```

These lines instruct the interpreter that if the script is executed via the command line, it should run the `main()`.
Running the script again should show the script working as it did before.
For our purposes, this is boilerplate code.
How exactly it works is useful to know, but not critical.

The next portion of functional-izing `ft.py` is moving the contents of `main.py` into smaller functions.
Each of these functions should accomplish a specific purpose.
For example, we can have a function that parses command-line arguments and a function that creates transfer directories.
These purposes point towards a good naming practices for functions, `do_this_thing()`.

For the `parse_args()` function, we can do the following.

```py
def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--source', required = True,
    help='path to the root of the digital carrier', metavar='path/to/carrier')
    parser.add_argument('--id', required = True,
    help='media id assigned to the digital carrier', metavar='M######_####')

    return parser.parse_args()

def main():

    args = parse_args()
    ...
```

The new component here is the `return` statement.
When you call a function, Python executes every line of that function.
If you want that function to give you output, you define the output with the `return` operator followed by whatever Python code will provide that output.
The Python interpreter ends the function as soon as it executes a `return` statement, so typically you see these as the last line in a function.

For the `create_transfer_folders()` function, we can do the following.

```py
def create_transfer_folders(media_id):
    ft_path = '/Volumes/DigArchDiskStation/Staging/ingest/fileTransfers'

    coll_id = media_id.split('-')[0]
    dest_path = Path(ft_path).joinpath(coll_id).joinpath(args.id)
    md_path = dest_path.joinpath('metadata')
    subdoc_path = md_path.joinpath('submissionDocumentation')
    object_path = dest_path.joinpath('object')

def main():

    args = parse_args()

    create_transfer_folders(args.id)
```

This function includes an argument definition.
A single argument must be included between the parentheses when `create_transfer_folders()` is executed.
That argument will be used as the `media_id` variable within the function itself.
In our case, we need to edit the lines that referenced `args.id` to use the new `media_id` variable.

One last note about how function make code modular.
Anything defined within the context of a function cannot be accessed outside of that function unless it is specifically outputted to another function.

For example, in this reorganization, the `args` variable exists only in the context of the `main()` function.
If you want to use data from `args` in another function, you need to send it to that function as an argument.
And the name of the data in the context of that function will not be `args` but instead the name of that argument.

### Testing the New Functions

As a quick check, run the script to make sure that it still works.
If it does, we're ready to start writing unit tests.

Start a new file in the same folder called `test_ft.py`.
We'll need two module for our testing work:

* `unittest` - tools to help us write and execute tests
* `tempfile` - tools to create temporary files and folders, especially during tests

When using `unittest` we create a class to group testing functions.
We'll create two classes.
One for the command-line interface and one for the code that transfers files.
For now, we'll create a passing test in each class.

```py
import unittest
import tempfile
import ft
from pathlib import Path


class CommandLineTest(unittest.TestCase):

    def test_required_parser(self):
        self.assertTrue(True)


class Xfer_Test(SelfCleaningTestCase):
    def test_create_xfer_dirs(self):
        self.assertTrue(True)
```

And run the test to see what a passing test looks like.

```sh
python -m unittest -v test_ft
```

The syntax for testing functions is that each test must include one or more assertions about the result of the test.
In `unittest` syntax, these assertions look like this `self.assert_(some_data)`.
`unittest` includes assert methods for a variety of conditions like `assertTrue`, `assertEquals`, and `assertRaises`.

For our default `create_transfer_folders()` test we want to assert that it does create the folder as expected.

From pseudocode

```py test_ft.py
def test_create_folders():
    # ft.create_transfer_folders(media_id='M1234-0001')
    # expect to find xfer_path/M1234/M1234-0001
```

To Python code

```py test_ft.py
def test_no_errors(self):
    ft.create_transfer_folders(media_id='M1234-0001')
    expected_folder = Path(transfer_path, 'M1234', 'M1234-0001')
    self.assertTrue(expected_folder.exists())
```

When we run the unittest, we get a fail report.
This is actually the way that test-driven development is supposed to work.
Write a test for what the code should do, and then write code that can pass the test.

At this point, `create_transfer_folders()` doesn't actually create any folders.
It only creates paths to potential folders.

Since this is a test that we'll run over and over again, we want a clean test environment that doesn't affect our production workspace.
So we'll use with temporary folders that can be deleted after the test.
And, we'll have to make it possible to change the `ft_path` that's currently hard-coded.

First for the hard-coded `ft_path`, we'll define the variable outside of the scope of any function.
And then, we'll add an argument to `create_transfer_folders()` with a default of `ft_path`.

```py ft.py
ft_path = '/Volumes/DigArchDiskStation/Staging/ingest/fileTransfers'

def create_transfer_folders(media_id, ft_path=ft_path):
    
    coll_id = media_id.split('-')[0]
    dest_path = Path(ft_path).joinpath(coll_id).joinpath(args.id)
    md_path = dest_path.joinpath('metadata')
    subdoc_path = md_path.joinpath('submissionDocumentation')
    object_path = dest_path.joinpath('object')
```

Now in the test, we can override this path with a temporary directory.
To see where the temporary directory is, we print it out.

```py test_ft.py
def test_no_errors(self):
    transfer_path = tempfile.tmpdir()
    ft.create_transfer_folders(media_id='M1234-0001', ft_path=transfer_path)
    expected_folder = Path(transfer_path, 'M1234', 'M1234-0001')
    print(expected_folder)
    self.assertTrue(expected_folder.exists())
```

The test still fails.
`create_transfer_folders()` still needs to create a directory.
Every `Path()` object has a `mkdir()` method to do this.
By default, `mkdir()` only creates a single directory, but it can make a chain of directories with an optional argument.

```py ft.py
def create_transfer_folders(media_id, ft_path=ft_path):
    
    coll_id = media_id.split('-')[0]
    dest_path = Path(ft_path).joinpath(coll_id).joinpath(args.id)
    md_path = dest_path.joinpath('metadata')
    subdoc_path = md_path.joinpath('submissionDocumentation')
    object_path = dest_path.joinpath('object')

    dest_path.mkdir(parents=True)
```

Running the test again should result in two passes.

That's just tests part of our requirements.
We probably want to add `self.assertTrue()` statements for the other directories.
We also need to think about what should happen when a directory already exists.
