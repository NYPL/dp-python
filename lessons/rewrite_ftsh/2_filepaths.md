---
title: Manipulating file paths
parent: Rewriting ft.sh
nav_order: 2
---

## Goals

* Learn how to mock files and directories for testing purposes
* Use the features of `pathlib` to create and manipulate paths

## Path requirements

`filetransfer.py` will need to

* Read the source digital carrier
* Create a destination based on the Media ID

Let's think about these as tests.

* Confirm that that source digital carrier exists
* Confirm that the destination parent directory exists
* Confirm that the destination based on the Media ID doesn't already exist
* Confirm that we can create the destination

All of these require working with paths.

## Paths in Digital Preservation

Our work always come back to files.
Finding files.
Moving files.
Reading files.
Creating files.
Deleting files.

Our scripts need to be able to work with files scattered across local storage, network storage, external storage, and other systems.
Our desktop computers hide this physical complexity by organizing files according to a hierarchal system of folders.
A file is contained in a folder, which is contained in a folder, and so on until you reach the root folder (Mac/Linux) or drive (Windows).
The series of folders is called the path.

When you use a graphical file manager or a file open dialog, the program constructs the path as you open folders.
That metaphor hides more complexity.
When you open a folder, the contents are listed and you learn what the folder contains.
When you open a further folder, the program updates its current working path by adding that folder to the path.
In Python, we often have to perform these steps explicitly.

And because Python scripts can work on Windows, Linux, and Mac, we also have to be aware of how paths differ between those systems.

## Filepath strategies in Python

If you've worked with files in Python before, you might have written lines like `'C:\path\to\directory' + '\' + 'filename'` + `open('/path/to/network/drive/report.csv')`.
These strings look like paths, and Python functions that work with files can interpret them as path.
Working with paths as just strings does create some problems.
The most visible is that the direction of the slashes (`\` or `/`) depends on the platform.
That is annoying, although if you work in a single-platform office, it might not come up.

Less obvious is that this encourages hard-coding paths.
The network drive might be mounted as `'/Volumes/network_folder'` on one machine but `'/Users/username/Desktop/network_folder'` on another.
It would be nice if our script could work on both machines without us having to maintain two different versions of the script.

We'll use a few strategies to manage these situations.
These will include using one of the standard modules for path manipulation and defining our paths as user input.

### `os.path` and `pathlib`

There are two standard modules that you can use to manipulate filepaths, `os` and `pathlib`.
`os` is for operating system interactions, including but not limited to filepaths.
Most of the filename functionality is actually in its `path` submodule
`pathlib` is a newer module that is only for working with paths.

Both detect the platform they are on, and create a path to that follows the rules of that platform.
The following demonstrates how to join together folder and filenames with each module.

```py
import os

path = os.path.join('path', 'to', 'directory')
```

```py
import pathlib

path = pathlib.Path('path', 'to', 'directory')
```

The code looks very similar, but result is different.
`os.path` returns a string, `'path/to/directory'`.
`pathlib.Path` returns a `Path()` object, `Path('path/to/directory')`.
The following illustrates the difference.

```py
path = os.path.join('path', 'to', 'directory')
filepath = os.path.join(path, 'filename'))
os.path.is_file(filepath)
```

```py
import pathlib

path = pathlib.Path('path', 'to', 'directory')
filepath = path.joinpath('filename')
filepath.is_fileF()
```

Because the result of `os.path` manipulations is a string, everytime we use it, we have to call first call a function, and then give it data.
Because the result of `pathlib` manipulations is a `Path()` object, every object has built-in functions that relate to it being a path.

We will be using `pathlib`.
Since it is newer, you may not find as many posts and articles for it on the Internet.
In those cases, you can always use ideas from `os.path` but you'll need to translate to the `pathlib` syntax.

### Mocking file paths

If we're trying to test code that works with files, how do we test it?
Especially if the script moves or deletes files, how do we makes sure it is not going to run amok?
Mocking.

The mock features of a `pytest` can also create temporary files and folders so we can understand if our script's logic works without risking the files we care about.
To mock a file with `pytest`, use the `tmp_path` argument.
`tmp_path` actually builds off of the `pathlib` library.
All of the methods we'll use to manipulate these temporary paths can also be used with `pathlib` paths.

The following tests both the existence of the temporary directory and that it is empty.

```py
def test_empty_dir(tmp_path):
    contents = list(tmp_path.iterdir())
    assert tmp_path.exists()
    assert len(contents) == 0
```

We can also create folders with specific names.

```py
def test_mddir_created(tmp_path):
    md_dir = tmp_path.joinpath('metadata')
    md_dir.mkdir()
    assert md_dir.name == 'metadata'
```

However, it would be annoying if we had to start every single test with by mocking files and folders.
To simplify this, we can mock the file structure once and tell `pytest` to continually reuse that file structure.

The key portions to note here are:

1. `@pytest.fixture()` is a decorator that tells Python to use the following function as a `pytest.fixture`
2. `destination_md()` returns a value we can use in future functions
3. The name of the function `destination_md` is passed as an argument to tests that need to used it

```py
@pytest.fixture()
def destination_md(tmp_path):
    md_dir = tmp_path.joinpath('metadata')
    md_dir.mkdir()
    return md_dir

def test_empty_dir(destination_md):
    assert destination_md.name == 'metadata'

def test_mddir_created(destination_md):
    contents = list(destination_md.iterdir())
    assert len(contents) == 0
```

## Making sure paths exist

This script works with two storage locations: the source digital carrier and the destination for the bag.
In order for the script to work, both have to exist.
As an extra feature, it would be nice to have a default destination that we can change if needed.

In the previous lesson, we added features to `parse_args` to accomplish this.
We will do the same for these arguments, but use file mocking to test if they work.

### Testing for a bad carrier path

This test can follow the same template as the Media ID validation.
Because we are testing for a non-existant path, we don't have to mock one up, yet.

```py
def test_bad_id(monkeypatch):
    ...

def test_bad_carrier_path(monkeypatch):
  bad_path ='path/to/carrier'
  monkeypatch.setattr('sys.argv', ['filetransfer.py', '--source', bad_path, '--id', 'M12345-0001'])

  with pytest.raises(SystemExit):
    filetransfer.parse_args()

  stderr = capsys.readouterr().err

  assert f'{bad_path} does not exist' in stderr
```

Run `pytest` and there should be a new fail.

### Validating the carrier path

The `valid_id` code from the previous lesson can also act as a template for validating the carrier path.
In `valid_id`, we used the `re` module to test if the input matches our requirement and then return the input if it does.
That function is then referenced in the appropriate `.add_argument()` by `type=valid_id`.

We will write a function that similarly tests the input.
In this case, we'll use the `Path` class from the `pathlib` module.
Every `Path` object has an `.exists()` method that will tell you if the path exists or not.
More specifically, it has methods like `.is_dir()`, `.is_file()`, and others that will tell you if the path is a specific kind of object.

It may feel strange that there can be paths that don't exist.
But, paths are strings of characters that follow particular rules.
They don't need to refer to files or folders that exist.
For example, `/path/i/just/made/up` is a valid path.
It probably does not exist on your computer, but `pathlib` will parse that it is an absolute path, on a Mac/Linux system, with four folders (`path`, `i`, `just`, `made`), and a final object that is probably a file or a folder (`up`).
If we want this path to exist, we will need to create each component of this path.
We'll do that later in this lesson.

`pathlib.Path` objects have lots of useful methods.
While `valid_id` tested the input string and returned a string, it would be nice if our function for paths could do 3 things.

1. parse the input as a `Path`
2. check if the path exists
3. return the `Path` object so we don't have to parse it again

```py
import argparse
import re
from pathlib import Path

def parse_args():
    def valid_id(id):
        ...

    def extant_dir(path):
        parsed_path = Path(path).is_dir()
        if not parsed_path:
            raise argparse.ArgumentTypeError(
                f'{parsed_path} does not exist'
            )
        return parsed_path


    parser = argparse.ArgumentParser(
        description='transfer files from a carrier into a bag'
    )
    parser.add_argument(
        '--source',
        help='path to the digital carrier'
        required=True
        type=extant_dir
    )
```

Run `pytest` and... there are 2 failures?

This demonstrates how small assumptions can start creeping into code.
Let's look at the failures.

```sh
E   argparse.ArgumentError: argument --source: path/to/source does not exist
```

```sh
E   AssertionError: assert 'N12345-0001 does not match the required Media ID format of M#####-####' in 'usage: filetransfer.py [-h] --source SOURCE --id ID\nfiletransfer.py: error: argument --source: path/to/source does not exist\n'
```

Now that code is checking to make sure a source exists, any test that we wrote with a non-existent path fails.
These are good fails.
What we need to do is update our tests to use paths that exist.

At the top of the testing script we can create a file fixture.

```py
import filetransfer
import pytest

# Fixtures
@pytest.fixture()
def source_dir(tmp_path):
    return tmp_path
```

And in each of our failing tests, we add `source_dir` as input and replace the hard-coded non-existent file path with the new fixture.
Note that sometimes we have to explicitly ask for the string representation of the path, like in the `sys.argv` mock.

```py
def test_required_args(monkeypatch, source_dir):
    monkeypatch.setattr('sys.argv', ['filetransfer.py', '--source', str(source_dir), '--id', 'M12345-0001'])
    args = filetransfer.parse_args()
    assert args.source == source_dir
    assert args.id == 'M12345-0001'
```

```py
def test_bad_id(capsys, monkeypatch, source_dir):
    bad_id ='N12345-0001'
    monkeypatch.setattr('sys.argv', ['filetransfer.py', '--source', str(source_dir), '--id', bad_id])

    with pytest.raises(SystemExit):
        filetransfer.parse_args()

    stderr = capsys.readouterr().err

    assert f'{bad_id} does not match the required Media ID format of M#####-####' in stderr
```

Run `pytest` and there should be 6 passes.

### Testing for an available and writeable destination

This requirement feels very similar to the previous, and we'll follow a lot of the same template.

First for the mock file structure, add a fixture to create a destination fixture.
We are using tmp_path, but this will create a new directory separate from source_dir.

```py
def source_dir(tmp_path):
    ...

@pytest.fixture()
def dest_dir(tmp_path):
    return tmp_path
```

Back at the bottom of the script, create a test for a non-existent destination directory.

```py
def test_bad_carrier_path(monkeypatch):
    ...

def test_non_existant_destination_path(capsys, monkeypatch, source_dir):
    bad_path = 'path/to/dest'
    monkeypatch.setattr('sys.argv',
        [
            'filetransfer.py',
            '--source', str(source_dir),
            '--id', 'M12345-0001',
            '--dest', bad_path
        ])

    with pytest.raises(SystemExit):
        filetransfer.parse_args()

    stderr = capsys.readouterr().err

    assert f'{bad_path} does not exist' in stderr
```

Run `pytest` and there should be 1 failed test.
The expected error didn't happen.

Next create a similar test for if the destination is writable.
We will use the same fixture and alter the readability of it for just this test by using the `.chmod()` method.

`.chmod()` replicates the `chmod` shell tool, which is used to set the read, write, and execute permissions for 3 kinds of users.
Those characteristics are set by a set of 3 numbers, each between 0 and 7.
We supply those numbers to `chmod()` in Python by first indicating that these are octal (`0o`).
To make a folder readable and executeable but non-writeable for all users, use `0o555`
Read up on [chmod](https://en.wikipedia.org/wiki/Chmod) for more information.

```py
def test_non_existant_destination_path(capsys, monkeypatch, source_dir):
    ...

def test_non_writable_destination_path(capsys, monkeypatch, source_dir, dest_dir):
    dest_dir.chmod(0o555)
    monkeypatch.setattr('sys.argv',
        [
            'filetransfer.py',
            '--source', str(source_dir),
            '--id', 'M12345-0001',
            '--dest', str(dest_dir)
        ])

    with pytest.raises(SystemExit):
        filetransfer.parse_args()

    stderr = capsys.readouterr().err

    assert f'{bad_path} is not writable. Check your permissions' in stderr
```

Run `pytest` and there should be 2 fails.

### Accepting and validating a destination

In order to raise the expected errors, the parser needs to work with the `--dest` argument in the tests.
You could argue that we should have written an additional test or updated an existing test for successfully accepting this argument.
You're probably right, as we'll soon see.

For now, let's add the new argument.
Instead of making it required, we will use a new feature, `default`.
It will also use the same validation function as the `source` argument.

```py
def parse_args():
    ...
    parser.add_argument(
        '--id',
        help='media id in the form of M#####-####',
        required=True,
        type=valid_id
    )
    parser.add_argument(
        '--dest',
        help='path to destination',
        default='/Volumes/DigArchDiskStation/',
        type=extant_dir
    )
```

Run `pytest` and there should be 3 failed test.
`test_non_existent_destination_path` should be passing as expected.
`test_non_writable_destination_path` should still be failing as expected.
`test_require_args` and `test_missing_args` are failing.

That's not because there are new requirements, but because the default `dest` argument is failing its validation.
`error: argument --dest: /Volumes/DigArchDiskStation does not exist`
That's a good fail, again.
It's an annoying failure, because it's less clear how to handle this issue.

1. Update the failing test to use the `dest_dir` fixture. (easiest)
2. Update the failing tests to ignore the `dest` validation. (more complicated, may cause its own bugs)
3. Use a fixture to create a directory at the default path. (dangerous if that's our production path)
4. Another strategy that a more experienced programmer know about.

This is one of the frustrations of unit testing as a non-professional programmer.
The more training you have, the better you are able to create tests systematically.
But we don't have that intuition or knowledge, so it's hard to know if we're over-testing, under-testing, or testing the wrong things.
This inexpert-programming author isn't sure where the balance exists either. `¯\_(ツ)_/¯`

For now, let's use the first strategy.
It does dilute the purpose of those tests.
However, it most directly addresses our issue.

```py
def test_required_args(monkeypatch, source_dir, dest_dir):
    monkeypatch.setattr('sys.argv',
        [
            'filetransfer.py',
            '--source', str(source_dir),
            '--id', 'M12345-0001',
            '--dest', str(dest_dir)
        ])
    ...


def test_missing_args(capsys, monkeypatch, dest_dir):
    monkeypatch.setattr('sys.argv', ['filetransfer.py', '--dest', str(dest_dir)])
    ...
```

Run `pytest` and there should only be 1 failed test.
Let's address that.

Unfortunately, `pathlib` does not have a method for checking writability.
We will need to use the [`os.access` function](https://docs.python.org/3/library/os.html#os.access) for this.
The testing template is the same.
In this case, the test will be `os.access(path/to/dir, os.W_OK)`

We used the type argument to test the existence of the file.
We can only use that argument once.
If we add a writability test to the `extant_dir`, that would also affect `source` arguments.
Instead, we can wrap `extant_dir` inside of another function.

Then

```py
import os
...

    def extant_dir(path):
        ...

    def writable_path(path):
        parsed_path = extant_dir(path)
        if not os.access(parsed_path, os.W_OK):
            raise argparse.ArgumentTypeError(
                f'{parsed_path} is not writeable. Check your permissions.'
            )
        return parsed_path
```

Run `pytest`. There should be 8 passes.

## Creating the destination directory

All of this work, and we've only defined inputs.
We haven't done anything with any data so far.
Then again, that is a lot of digital curation work.
We rely on specialized tools that do very complicated things.
Our expertise is in supplying the right inputs to those tools to make sure they perform the work we expect.

Now that we're confident in our inputs, we can use that data to perform some work.
For example, if we know the destination directory and Media ID, we can create the correct folders in preparation for the file transfer.

In our case, those folders are

1. a parent folder for the collection
2. a parent folder named by the Media ID
3. a child folder named `objects` that will receive the transferred files
4. a child folder name `metadata` with a second child folder named `submissionDocumentation` that receives reports and logs about the transferred files

We also don't want to overwrite these folders if they already exist.

### Testing for creating folders

We need a function to create the directories.
We'll call this `create_dirs`.
It will take two arguments, the destination directory and the Media ID.
It will create our required folders and return the path to the `objects` folder.

Our test will need to

* define the paths that should be created
* run the `create_dirs`
* test that the paths exist
* test that the function returns the expected value

```py

def test_create_directories(dest_dir):
    media_id = 'M12345-0001'
    collection = media_id.split('-')[0]
    coll_dir = dest_dir.joinpath(collection)
    id_dir = coll_dir.joinpath(media_id)
    object_dir = id_dir.joinpath('objects')
    subDoc_dir = id_dir.joinpath('metadata').joinpath('submissionDocumentation')

    returned_object_dir = filetransfer.create_dirs(dest_dir, media_id)

    assert object_dir.exists()
    assert subDoc_dir.exists()
    assert object_dir == returned_object_dir
```

We only test for the existence of two directories because if they exist, so do their parent directories.

### Writing `create_dirs`

The logic for creating the test can be transferred over to the function.
It will need to:

* receive two arguments as input
* define the paths to be created
* return the one of the paths as output

```py
def create_dirs(parent_dir, media_id):
    collection = media_id.split('-')[0]
    coll_dir = parent_dir.joinpath(collection)
    id_dir = coll_dir.joinpath(media_id)
    object_dir = id_dir.joinpath('objects')
    subDoc_dir = id_dir.joinpath('metadata').joinpath('submissionDocumentation')

    object_dir.mkdir(parents=True)
    subDoc_dir.mkdir(parents=True)

    return object_dir
```

This code looks very similar to the test.
As we write further tests, it will start looking different.

Much like `.exists()` also checks the existence of parent folders, `.mkdir()` can create parent folders by using the argument `parents=True`.

Run `pytest` and the test should be passing.

### Testing against overwrites

The test to make sure `create_dirs` raises an exception follows the logic of the test for the unwritable destination.
First create the situation in the mock file system, then see if the correct error is raised.

Because the function is supposed to raise an exception, it is wrapped in a `with` block much like the system exits for argument parsing.

```py
def test_do_not_overwrite_transfer(dest_dir):
    media_id = 'M12345-0001'
    collection = media_id.split('-')[0]
    coll_dir = dest_dir.joinpath(collection)
    id_dir = coll_dir.joinpath(media_id)
    id_dir.mkdir(parents=True)

    with pytest.raises(Exception) as err:
        returned_object_dir = filetransfer.create_dirs(dest_dir, media_id)

    assert f'{id_dir} already exists, check to make sure you are not overwriting' in err.value.args[0]
```

Run `pytest` and the failed test will report that no exception is raised.
That means our script would happily overwrite existing work.

### Improving `create_dirs`

In order to address this issue, `create_dirs` should check if the directory exists before creating new directories.
If it does exist, it should raise an exception.

```py
def create_dirs(parent_dir, media_id):
    media_id = 'M12345-0001'
    collection = media_id.split('-')[0]
    coll_dir = parent_dir.joinpath(collection)
    id_dir = coll_dir.joinpath(media_id)
    object_dir = id_dir.joinpath('objects')
    subDoc_dir = id_dir.joinpath('metadata').joinpath('submissionDocumentation')

    if not id_dir.exists():
        object_dir.mkdir(parents=True)
        subDoc_dir.mkdir(parents=True)
    else:
        raise Exception(
            f'{id_dir} already exists, check to make sure you are not overwriting'
        )

    return object_dir
```

## Filepath Conclusion

This lesson introduced `pathlib` and several of its methods, including `.joinpath()`, `.exists()`, `.is_dir()`, `.chmod()`, and `.mkdir()`.
It also introduced the file mocking and fixture features of `pytest`, which conveniently also used `pathlib`.

We were able to use these tools to write code that creates new folders while making sure we don't overwrite existing folders.
