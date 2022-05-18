---
title: Creating a command-line script with arguments
parent: Rewriting ft.sh
nav_order: 1
---

## Goals

* Document what user input we need to support
* Write tests to check if our script accepts that input
* Build a command-line interface for our script

## User Input Requirements

`ft.sh` has two points where it asks for user input.

```sh
echo -e "${BLUE}Please drag the SIP folder over this window. See the folder path displayed? Hit return!:${NC}"
echo -e "${BLUE}Please enter the MediaID for this file transfer and hit return:${NC}"
```

The folder path is an absolute path to the digitial carrier being transferred, such as `/Volumes/mounted-hard-drive`
The MediaID is an ID created by NYPL to uniquely identify the carrier.
It consists of the collection number, a dash, and a sequential number for the media in the collection, such as `M123456-0001`.
Both of these inputs are required.

Currently, `ft.sh` accepts inputs interactively.
First, you run the script.
Then, a prompt appears asking you for a file path.
Then, another prompt appears asking you for a MediaID.
Each of these steps contain a lot of help text.

We're going to change this behavior and have all user input happen as arguments to the first command, e.g. `filetransfer.py -arg1 /Volumes/mounted-hard-drive -arg2 M123456-0001`
This will make it easier to further automate the command in the future since you don't need to sit at the computer and wait for the prompt.
We're also going to require both pieces of input, and we'll have a help interface to explain these features.

So our requirements for the command-line interface are:

1. Accept a Media ID and a carrier path
2. Require both a Media ID and a carrier path to run
3. Provide help text

Before we build the code to accomplish this, we'll build the tests to see if we were successful.

## Writing Tests for Command Line Input

We need two things to test the command line interface for the script.

1. A way to refer to the command-line portion of the script from our test script
2. A way to for the test script to send command-line arguments

### Functions and Testing

In order to refer to the command-line portion of the script, we need a name to refer to it.
That's one of the benefits of creating a function.

The following examples of pseudo-code are roughly equal.
A piece of data is processed by one function, `str`, and the result is processed by a second function, `parse`.
The final result is stored to a variable called `result`.

```py
variable = str(argument[0])
result = parse(variable)

```

```py
def parse_args(argument):
  variable = str(argument[0])
  result = parse(variable)
  return result

```

The difference is that if we ever need to use that sequence of functions again, the second example let's us call `function_name(argument)` instead of repeating the previous two lines.

When it comes to testing, functions are critical, because they're the only way that we can test that logic.
The first example above is untestable.
There is no easy way to tell our testing script to run two random lines of code.
And even if we figured one out, we'd have to update that test every time the lines shifted around.
Being able to call `script_name.function_name()` makes the code testable.

Once our code has a name, we can write one or more tests to check the behavior of that code.
As we improve the logic inside the function, we should have unit tests that check to make sure it performs the right actions.

```py
def test_parse_args():
  argument = 'a known input'
  result = script_name.function_name(argument)
  assert result == 'a known result'

```

If we learn about a new function that runs faster, looks cleaner, or is somehow better than our current implementation, we can update our script and see if it still passes the test.

```py
def parse_args(argument):
  result = a_better_way_we_just_found_out_about(argument)
  return result

```

A more immediate benefit of functions is that they can help break down the logic of a program into discrete chunks.
That gives a nice grouping for the data and functions used to accomplish a particular step.
In this lesson, we'll create a function for parsing command-line arguments.

### Mocking

The second thing we need is a way for our test script to act like it's receiving command-line arguments.
It would be painful if we have to actual input our arguments during a test run.

Having a test perform fake actions for the sake of testing some other functionality is called mocking.
`pytest` has a specific version of mocking called `monkeypatch`.

To use it, our test function needs to accept `monkeypatch` as input.
Then we can use the attributes of `pytest`'s `monkeypatch` to fake command-line arguments, receiving data from a server, creating files, and other testing conditions.
In Python, command-line arguments are represented by a list called `sys.argv`.
Then for our command-line argument tests, we mock `sys.argv` with a potential command broken down into a list of strings.

```py
def test_parse_args(monkeypatch):
  monkeypatch.setattr('sys.argv', ['filetransfer.py', 'arg1', 'arg2'])
  args = filetransfer.parse_args()
  assert arg1 in args
  assert arg2 in args

```

There is some magic happening here that is easier to accept on faith.
`sys.argv` is how Python parses terminal inputs.
Those inputs are separated into a list by space characters, e.g. `filetransfer.py arg1 arg2` becomes `['filetransfer.py', 'arg1', 'arg2']`
The `parse_args` method should by default parse terminal defaults.
It's worth investigating this magic as you get deeper into CLIs, but we'll get back to our task for now.

## Writing CLI Tests for `filetransfer.py`

Back to the `test_filetransfer.py` script, which looked like this.

```py
import filetransfer
import pathlib

def test_completedtransfer():
    filetransfer.main()
    assert pathlib.Path('/path/to/destination').exists()
```

First we'll add some comments to keep things organized.
Over time, we'll add additional tests.
It will be easier to read all the tests if they are grouped by purpose

```py
import filetransfer
import pathlib
import pytest

# functional tests
def test_completedtransfer():
    filetransfer.main()
    assert pathlib.Path('/path/to/destination').exists()

# unit tests
# command line tests
```

Our CLI should do 3 things.

1. Accept a Media ID and a carrier path
2. Require both a Media ID and a carrier path to run
3. Provide help text

The loop for writing these tests will be.

1. Write the test
2. Run the test script to make sure it generates a fail and not an error.
3. Correct any bugs in the test, in case of an error
4. Add and commit the test in version control

### Test for accepting arguments

This test brings up one of the hardest tasks in programming, naming things.
We want argument names that are both descriptive but not annoyingly long to type out.
For now, let's say that the argument name for the media id should be `--id` and for the path should be `--source`.
A run of this script would be `python filetransfer.py python filetransfer.py --source path/to/source --id M12345-0001`.

```py
# unit tests
# command line tests

def test_required_args(monkeypatch):
  monkeypatch.setattr('sys.argv', ['filetransfer.py', '--source', 'path/to/source', '--id', 'M12345-0001'])
  args = filetransfer.parse_args()
  assert args.source == 'path/to/source'
  assert args.id == 'M12345-0001'
```

`args` is a fairly common abbreviation for arguments.
The `args.argument_name` syntax is also a common method to handle command-line arguments, based partially on the module we'll use to do the parsing.

### Require both arguments

Our CLI should also give feedback if a user forgets to include an argument or has a typo in their argument.
To mock this, we'll act like the user only ran `python filetransfer.py`.
In this situation, we want the script to immediately exit and report that both the `source` argument and the `id` argument are missing.

When a tested Python function exits, the function doing the testing also exits.
In order to examine and test the behavior during the exit, we have to run the tested function in a special context that does not cause the testing function to exit.
In `pytest`, this is done using a `with pytest.raises(SystemExit):` block.
We also need something that captures the error reporting.
In `pytest`, this is done by adding `capsys` to the input of the testing function and then parsing what it captures.

After `test_parse_args()`:

```py
def test_missing_args(capsys, monkeypatch):
  monkeypatch.setattr('sys.argv', ['filetransfer.py'])

  with pytest.raises(SystemExit):
    filetransfer.parse_args()

  stderr = capsys.readouterr().err

  assert 'error: the following arguments are required' in stderr
  assert 'id' in stderr
  assert 'source' in stderr
```

### Provide help text

Finally, it would be good for the script to have a help argument that explains what the script does.
This case will transfer files from a carrier into a bag, so let's have the script say that it does that.

The script will exit immediately after printing the help information, so a `with` block is needed.
Because the help text is sent to standard oupout instead of standard error, we parse `capsys.readouterr().out`

```py
def test_cli_help(capsys, monkeypatch):
  monkeypatch.setattr('sys.argv', ['filetransfer.py', '-h'])

  with pytest.raises(SystemExit):
    filetransfer.parse_args()

  stdout = capsys.readouterr().out

  assert 'transfer files from a carrier into a bag' in stdout
```

### CLI Testing Summary

The test script should now have 3 new testing functions.
These aren't perfect test.
You might want to add additional assertions for what the help should look like.
Or you could test what happens when you provide just one of the required arguments.
However, they are a good start for any CLI testing you want to do.

If you don't fully understand `monkeypatch`, `capsys`, `SystemExit`, or other `pytest` features that were introduced, treat these three testing functions as a template to build from until you're more comfortable with `pytest`

For now, we can return to writing the script itself.

## Writing the CLI for `filetransfer.py`

First, let's run the tests.
In a terminal in the the working directory of your script files, run the following.

```sh
pytest
```

You should see a report of `3 failed, 1 passed`.
The summaries for the failed tests, should look similar to the last lesson.
`module 'filetransfer' has no attribute 'parse_args'`

We can fix that issue pretty quickly by adding a new function to `filetransfer.py`

```py
def parse_args():
    return

def main():
    return
```

Running `pytest` in the terminal again no yields more specific errors.

```sh
FAILED test_python.py::test_required_args - AttributeError: 'NoneType' object has no attribute 'source'
FAILED test_python.py::test_missing_args - Failed: DID NOT RAISE <class 'SystemExit'>
FAILED test_python.py::test_cli_help - Failed: DID NOT RAISE <class 'SystemExit'>
```

This says that our script does not:

1. successfully parse command line arguments
2. successfully exit when it does not receive required arguments
3. successfully exit when it receives an argument to print help

We'll fix these one-by-one using the `argparse` module, Python's built-in module for building command-line interfaces.

### Adding `argparse` and parsing arguments

To access the functions of `argparse`, we need to import it into the script.

```py
import argparse

def parse_args():
    return
...
```

To learn how to use it, or any Python module, it's helpful to head to the module's documentation.
The [documentation for argparse](https://docs.python.org/3/library/argparse.html) follows a standard documentation structure used for most other standard library modules.

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

For our script, we will need to:

1. create an instance of the `ArgumentParser` object
2. define arguments for `source` and `id`
3. parse the arguments before returning it

```py
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source')
    parser.add_argument('--id')
    return parser.parse_args()

```

Because `parser` is an instance of the `ArgumentParser` class, it has all of the methods of the class, including `add_argument()`.
That method allows us to define how the `parser` should interpret command-line arguments.
For example, `parser.add_argument('--source')` makes it possible to run a command like `python filetransfer.py --source path/to/source` and argparse will associate the flag `--source` with the input `path/to/source`.
We can add further inputs to an `add_argument` in order to add optional names, required data types, help text, or other features.

Finally, `parser.parse_args` actually performs the work of interpreting arguments received by the script into data that the rest of the script can use.
In general, each argument created in the parser is produced as an attribute of the object returned by `parse_args`, e.g. `--source` is referenced as `.source`.
We're coopting the name of `parse_args` in order to communicate that the results of our function are the results of a `argparse.ArgumentParser.parse_args()` method.

Back to the terminal to run `pytest` and out test results should now be `2 failed, 2 passed`.

### Requiring arguments

The missing argument test is still failing.
Just because our script can parse something like `python filetransfer.py --source path/to/source`, doesn't mean that it will exit if we forget that argument, mistype, or have another issue.
To make these non-optional, we need to put further conditions on `add_argument`

Because making arguments required is very common, `add_argument` has its own argument for it, `required`.
According to the docs, `required` is set to `False` by default.
If we want an argument to be required, we need to set it to `True` when we define the argument.

```py
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--id', required=True)
    return parser.parse_args()

```

Back to the terminal to run `pytest` and out test results should now be `1 failed, 3 passed`.

### Adding a help function

Finally, argparse comes with a built-in help argument.
Running the script with a `-h` will print out all of the configuration options chosen for the parser.
To add a description of the entire script to the help output requires a change to the initial `ArgumentParser` call.

```py
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='transfer files from a carrier into a bag')
    parser.add_argument('--source', required=True)
    parser.add_argument('--id', required=True)
    return parser.parse_args()

```

Back to the terminal to run `pytest` and out test results should now be `4 passed`.

## Going further

This is a basic setup for using `argparse`.
There a plenty of additional features we could use.
For example, every argument can have its own help text.

Note: as you increase the number of arguments, it becomes harder to read a function call.
You can break the arguments over several lines to improve legibility.
To do so, create a new line after either a parenthesis or a comma and start the new line one tab in from the function.

```py
parser.add_argument(
    '--id',
    help='Media ID in the form of M#####-####'
    required=True
)
```

We could have a requirement that every argument has specific help text, then write test for that help text, and finally implement that help text.
However, we could also choose to just implement the help text.
Everyone has their own opinions about what features require testing.

### Better argument validation

We could get more exact about our requirement though.
What if someone entered an incorrect Media ID, like N12345-0001, M12345_0002, or M12345-000q?
It would be good for the script to report and error and exit.

Let's write a test for that.

```py
def test_bad_id(monkeypatch):
  bad_id ='N12345-0001'
  monkeypatch.setattr('sys.argv', ['filetransfer.py', '--source', 'path/to/source', '--id', bad_id])

  with pytest.raises(SystemExit):
    filetransfer.parse_args()

  stderr = capsys.readouterr().err

  assert f'{bad_id} does not match the required Media ID format of M#####-####' in stderr
```

Running `pytest` should result in 1 failed test.

To validate input, we can use the `add_argument` `type` argument.
At its most direct level you can require input to be a specific data type like `str` or `int`.
But, you can also create function to validate custom types.
The pattern for the validation function will be

```py
def valid_...(input):
    # if the input isn't valid
        # raise an exception
    # return the input
```

For the Media ID, the NYPL pattern is start with M, then 4 to 6 numbers, then a dash, and then end with 4 numbers.
We can express this more succinctly as a regular expression, `M\d{4,6}-\d{4}`.
So we'll import the `re` module into our script, in order to use `re.match(r'M\d{4,6}-\d{4}', id)`.

Because this function will only be used within the argument parser, we define it inside of `parse_args`.
(It may seem strange, but yes, you can define functions in functions.)

Finally, we reference the validator from `add_argument` with `type=valid_id` (note that it doesn't have parentheses).

```py
import argparse
import re

def parse_args():
    def valid_id(id):
        if not re.match(r'^M\d{4,6}-\d{4}$', id):
            raise argparse.ArgumentTypeError(
                f'{id} does not match the required Media ID format of M#####-####'
            )
        return id

    parser = argparse.ArgumentParser(
        description='transfer files from a carrier into a bag'
    )
    parser.add_argument(
        '--source',
        help='path to the digital carrier'
        required=True
    )
    parser.add_argument(
        '--id',
        help='media id in the form of M#####-####',
        required=True,
        type=valid_id
    )

    return parser.parse_args()
```

Back to the terminal to run `pytest` and out test results should now be `5 passed`.
Note, this was a slightly different rhythm of testing, just one test at a time.
That is yet another choice depending on what you find most useful.

Next lesson, we'll cover file paths from creating paths to testing for their existence.
We can use that to validate the `--source` argument, but for now, we have a good start to the script.

## Argument Parsing Conclusion

Python has a built-in module for creating command-line interfaces called `argparse`.
A common way to use this module is to create a self-contained function that invokes the `ArgumentParser`, defines each desired argument, and the parses the results.
In practice, this can become so idiomatic that you may skip writing tests for your CLI.

However, writing test can help you keep track of requirements, implement new kinds of features, or for other reasons.
Testing this part of a script can be complicated with all the mocking and exit codes, so the test functions built here are a good starting point if you want to build your own tests.
