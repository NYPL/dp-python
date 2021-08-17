---
title: Manipulating file paths
parent: Rewriting ft.sh
nav_order: 2
---

The purpose of `ft.sh` is to transfer data from a source to a destination, that we define.
That destination consists of a few parts, `RAID location/Collection folder/Media ID folder`.
These are all string manipulations.

`ft.sh` uses some neat bash syntax tricks to do a lot of work at the same.

```sh
mkdir -p "$FTpath/$Collection/$MediaID/"{metadata/submissionDocumentation,objects}
```

In one line, this defines 4 different folders and creates them.

* `$FTpath/$Collection/$MediaID/`
* `$FTpath/$Collection/$MediaID/metadata`
* `$FTpath/$Collection/$MediaID/metadata/submissionDocumentation`
* `$FTpath/$Collection/$MediaID/objects`

In Python, we'll be approaching this step by step.
First defining the paths, then seeing if the paths already exist, and finally creating them.
This is more verbose but also useful in the future when troubleshooting.

## Goals

* extract collection id from the Media ID argument
* create a filepath based on Media ID argument
* verify the existence of the carrier's filepath

## Filepaths and Strings

Data stored in Python has a data type that changes how that data can be worked with. The core types are:

* Boolean - a value that can be evaluated as True/False, 1/0, or other binary classifications. The only Boolean values are `True` and `False`.
* Number - a value that can be used for math. Numbers are written as sequences of number characters like `1` and `3.14159`
* String - a value that can store a sequence of characters. Strings are wrapped in quote marks like `'True'` and `'1'`

To demonstrate the difference, we can use the `type()` function and the `+` operator.

```py
> type(True)
<type 'bool'>
> True + True
2
> type(True + True)
<type 'int'> # integer, a type of number value

> type(1)
<type 'int'>
> 1 + 1
2

> type('1')
<type 'str'>
> '1' + '1'
'11'
```

A filepath is a long sequence of characters, so in Python it is stored as a string.
Strings are always surrounded by single quotes, `'`.
Double quotes also work, but single quotes are recommended.

Recognizing that a filepath is a string, means that we also have access to the methods available to all strings. For example,

```py
> 'PATH/TO/file.ext'.lower()
'path/to/file.ext

> 'path/to/file.ext'.endswith('ext')
True

> 'path/to/file'.split('/')
['path', 'to', 'file']
```

None of these methods are directly related to the filepath-ness of the string, but they can be useful when working with filepaths.

The last example demonstrates one of the higher-level data structures of Python.
Booleans, numbers, and strings can store a single chunk of information.
To store and use more complex arrangements of information, we have:

* lists - ordered and editable series of data
* dictionaries - labeled arrangements of data
* tuples - ordered and uneditable series of data

```py
type([1, 2, 3])
<type 'list'>
type({'first': 1, 'second': 2})
<type 'dict'>
type((1, 2, 3))
<type 'tuple'>
```

Lists are useful for creating queues of data to work through.
Dictionaries are useful for storing complex structures of data with labels to access specific items. Tuples are less useful for our purposes.
We'll focus on lists here.

## Script work

To create the destination for the data transfer, we'll need to:

* store a constant path
* reference a value from argparse
* extract a portion of string
* combine the three components with the appropriate directory separators

### Store the RAID path

Much like `ft.sh` storing the RAID path requires creating a variable and assigning the path to that variable.

One of the most challenging parts of programming is picking names for variables.
In general a variable name should be:

* short
* descriptive of the data it stores
* use a consistent style like `under_scores` or `camelCase`
In this case, we'll use `raid_path`.

```py
ft_path = '/Volumes/DigArchDiskStation/Staging/ingest/fileTransfers'
print(ft_path)
```

### Reference the Media ID from argparse

The next portions of the destination path depend on data from argparse.

When `parse_args()` is called, it creates an object where each piece of data is available via it's argument name.
In our case, the Media ID is stored as `args.id`

```py
print(args.id)
```

We can use `args.source` whenever we want to pull the source path entered by a user.
However, if we want to manipulate this path for any reason, it's better to store the results to a new variable.
That will keep the job of the data in the `args` object and the new variable more defined.

### Extract the Collection ID from Media ID

NYPL Media ID's are a standard format of `CollectionID-####`.
The length of both the Collection ID and the media number is not perfectly constant.
But the `-` character is always present.
We use the string's `split()` method to get the characters before and after the `-` character in `args.id`.

```py
print(args.id.split('-'))
```

The data we get back is in a list.
The square brackets `[ ]` are a good indicator of this.
We don't want both items in the list.
We want only the first one.
To do that we use list indexing.

To call a specific item from a list, put the number of the item's position in square brackets after the list.
In Python (and many other programming languages), the first position is always `0`.

```py
print(args.id.split('-')[0])
```

List indexing is a deeper topic with other features.
For example, you can negative index to call items from the end of the list `[-1]`.
And you can index a range to get a sublist from the original, `[0:1]`.
Explore these features as you work with lists more.

For now, we can extract and store the collection ID.

```py
coll_id = args.id.split('-')[0])
```

### Create filepath

The final step in our file path manipulation is creating a destination path according with the components that we have.
The pattern for the destination path is `ft_path/coll_id/args.id`.

We have the three strings that make up this path.
To get the final path, we need to put them together.
Strings can be put together with a `+` operator.
For example,

```py
print(ft_path + coll_id + args.id)
```

The one thing missing from this path is the folder separator.
So far we've assumed that we're working in a Mac/Linux environment and used `/`.
But in a Windows environment, folder separators go the other direction `\`.
To write cross-platform code, we need something that detects the environment and then uses the appropriate character.

That is something we could write, but we would need to code for a lot of edge cases.
It's better to use an existing module.
In this case, there are two potential built-in modules, `os` and `pathlib`.
`os` is for operating system interactions, including but not limited to filepaths.
`pathlib` is a newer module that is only for working with paths.
The following demonstrates how to join together folder and filenames with each module.

```py
import os

os.path.join(['path', 'to', 'directory'])
```

```py
import pathlib

pathlib.Path('path').joinpath('to').joinpath('directory')
```

Before moving on, it's useful to look at the differences between these two methods.
With `os`, we have to have all components of the final path ready and in a list structure before we run the `join()` method from the `path` submodule.
With `pathlib`, we can chain together the operations and add one component at a time.
The core structure of `os.path` is inputting strings and returning strings.
In contrast, `pathlib` takes strings and returns Path objects.
These Path objects have attached methods like `joinpath`.

We will be using `pathlib`.
Since it is newer, you may not find as many posts and articles for it on the Internet.
In those cases, you can always use ideas from `os.path` but you'll need to translate to the `pathlib` syntax.

Back to our use case, we have three strings that we want to turn into a path.
To make the script do this, we need to import `pathlib`.
Because we'll just be using the `Path` submodule and it's annoying to type `pathlib` repeatedly, we'll import just that submodule at the top of the script.

```py
from pathlib import Path
```

At the end of the script we can define our destination folder.

```py
dest_path = Path(ft_path, coll_id, args.id)
```

We can also define the subdirectories.

```py
md_path = dest_path.joinpath('metadata')
subdoc_path = md_path.joinpath('submissionDocumentation')
object_path = dest_path.joinpath('object')
```

### Looking before you leap

Before bringing these folders into existence, we should make sure that they do not already exist.
In `pathlib`, every Path object has an `is_dir()` method.
Whenever a method is called `is_...()`, it's a good assumption that it will probably return a value of `True` or `False`.
These make them very useful for conditional code that branches based on the result of a method.

To see if the `dest_path` exists:

```py
print(dest_path.is_dir())
```

In this case, the method should return `False`, for a few reasons.
In a production setting, hopefully we are not accidentally overwriting a transfer.
In a development setting, hopefully we are not experimenting on live data. Not only should `dest_path.is_dir()` return `False` but also for `ft_path.is_dir()`

So far, we've created programs that won't alter our computer.
However, as we begin to create folders and move files, it's useful to have test environments that provide a safe zone for testing.
That's the topic for next module.

### Current script with arguments

```py
#!/usr/bin/env python3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--source', required = True,
help='path to the root of the digital carrier', metavar='path/to/carrier')
parser.add_argument('--id', required = True,
help='media id assigned to the digital carrier', metavar='M######_####')

args = parser.parse_args()

ft_path = '/Volumes/DigArchDiskStation/Staging/ingest/fileTransfers'
coll_id = args.id.split('-')[0]
dest_path = Path(ft_path).joinpath(coll_id).joinpath(args.id)
md_path = dest_path.joinpath('metadata')
subdoc_path = md_path.joinpath('submissionDocumentation')
object_path = dest_path.joinpath('object')

```
