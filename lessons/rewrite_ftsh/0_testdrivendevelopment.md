---
title: Test-driven Development
parent: Rewriting ft.sh
nav_order: 0
---

## Goals

Scripts perform the same action repeatedly.
This means they also perform the same mistake repeatedly.
We call those mistakes bugs.

The goal of this module is to introduce test-driven development, a way of writing code that proactively checks for those bugs.

## Why Test-Driven Development

When first learning to write code, a common method is to use an exploratory approach.
You have some information/data, and you want to a specific result.

1. Write some code that gets you closer to the result
2. Run the script and test if it does the thing you want
   * If it fails your test, adjust the code and go back to 2
   * If it passes your test, go to 1 and write more code

This eventually creates a script that does what you want, but it is probably more complicated, less efficient, or non-optimal in other ways.
If you want to go back to improve it, how do you know that a change won't cause a bug somewhere down the line?

Test-driven development addresses this by changing the order of the process above.

1. Write some code that tests the behavior of your script
2. Add code to your script that performs that behavior
3. Run your tests
   * If the tests fail, adjust the script and go back to 3
   * If the tests pass, go to 1 and write more tests

In effect, we are writing two scripts in parallel.
The first script encodes what we would want a script to do.
The second script encodes one way of accomplishing that.

If we improve, update, or alter the second script, we can use the first to test that it still does what we expect it to do.

## Two Types of Test

When testing, you can look at two different levels of test, unit test and functional test.

* functional test - a test to see if the larger purpose is met by the code
* unit test - a test to see if a specific portion of code performs as expected

For example, a functional test of `ft.sh` would check if the script successfully transfers the files when given the correct inputs.
A unit test of `ft.sh` would check that the portion of the script that parses the inputs raises an error if it receives bad inputs.

We'll start by writing a functional test and then build unit tests as we develop the body of the script.
That also means that our first test will always fail until we have completed the script.

## Using PyTest

There are a few Python testing framework.
We're going to use PyTest, primarily because it's recommended by Joanna White, Knowledge & Collections Developer at the BFI.

To start our project, we'll create two files `filetransfer_test.py` and `filetransfer.py`

```sh
project_folder
├── filetransfer.py
└── filetransfer_test.py
```

`filetransfer_test.py` has to test the code within `filetransfer.py`.
To do this, we import the script into the test script.

```py
import filetransfer
```

This looks exactly like importing a module into your script, because this is how module imports work.
Python first looks for a file with the correct name in the working directory.
If it can't find a file with that name, it looks in common locations for module installation.

Next we define our first functional test.
For now, we have to make a few assumptions about our script.

* `filetransfer.py` will have a `main()` function that performs the actions we want.
* A successful run of `filetransfer.py` will create the appropriate folder at a destination.
* We'll learn a better way to refer to that folder in our test in the future.

To test that the script performs the actions we want, we will need

1. to give a docstring to the function that explains the test
2. to define the setup data for the test
3. to call the functions that we want to test, ie. `filetransfer.main()`
4. to assert that the expected result occurred

Every test that we write will have one or more `assert` statements.
These evaluate whether a statement is true.
Their syntax is very similar to an `if` statement, except there is no colon at the end that sets off another code-block.

```py
import pathlib
import filetransfer

# functional test
def test_completedtransfer():
    """script should create a folder with the contents from the source"""
    expected_folder = pathlib.Path('/path/to/destination')

    filetransfer.main()

    assert expected_folder.exists()
```

To check our test, use the auto-discovery feature of pytest.
In the project directory, run `pytest` and you'll see the following.

```sh
collected 1 item

test_python.py F                             [100%]

=============== FAILURES ==========================
_______________ test_completedtransfer ____________

    def test_completedtransfer():
        expected_folder = pathlib.Path('/path/to/destination')

>       filetransfer.main()
E       AttributeError: module 'filetransfer' has no attribute 'main'

filetransfer_test.py:5: AttributeError
=============== short test summary info ===========
FAILED filetransfer_test.py::test_completedtransfer - AttributeError: module 'filetransfer' has no attribute 'main'
```

Failure is a sign of good coding practice.
If you're writing tests and running tests first, every test will fail at least in its life.
This particular test will fail until we finish rewriting `ft.sh`.

The important thing is that we read why the test failed, and address those errors that we can.
In this case, `'filetransfer' has no attribute 'main'` makes sense because `filetransfer.py` doesn't have a single line of code, much less a definition for `main()`.
We can address that immediately.

```py
def main():
    return
```

This function does nothing except exist.
When we rerun `pytest`, the output changes.

```sh
test_python.py F                                   [100%]

======================== FAILURES ========================
_________________ test_completedtransfer _________________

    def test_completedtransfer():
        expected_folder = pathlib.Path('/path/to/destination')

        filetransfer.main()

>       assert expected_path.exists()
E       AssertionError: assert False
...
filetransfer_test.py.py:6: AssertionError
================ short test summary info =================
FAILED filetransfer_test.py::test_completedtransfer - AssertionError: assert False
=================== 1 failed in 0.04s ====================
```

The failure is now where we want it.
`AssertionError: assert False` means that the thing we want to be true is not true, because the code does not accomplish what we want.

We will return to this particular test over the next few lessons to incorporate additional code.
For now, we established the pattern for test-driven development.

## Summary

In test-driven development:

1. Figure out what your code should do (and what it should not do)
2. Write a test function or functions to see if your code passes your test
3. Run the tests to check that your new tests fail as expected
4. Write code that will make your tests pass
