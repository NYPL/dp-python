---
title: Thinking ahead of bugs
parent: Rewriting ft.sh
nav_order: 2
---

## Goals

Bugs are bad.
Not just because our code doesn't do what we want.
But also because we're not sure exactly what our code is doing.
When using test-driven development, we can write tests for problems ahead of time, and design ways for our code to fail consistently and expectedly.

1. Design tests for expected issues
2. Write code to respond to those issues
3. Think about creating code to accomplish specific outcomes

## Defining expected behaviors for problems

At the end of the last section, we had code that could successfully create our needed folders.
But what if those folders already exist?

There are very real reasons for that to happen.
Maybe someone already transferred the disk.
Maybe someone typed in the ID for the disk wrong.
Maybe someone typed in another ID wrong.

Regardless, we don't want a script to overwrite those files without telling us about it.
We probably want the code to stop completely.

The typical approach to having a script tell you something is the `print` function.
For example:

```py
if bad_thing_happened:
    print("Bad thing happened")
```

However, we want the script to stop.
To do that we need to raise an exception.
This tells the script to exit immediately.

```py
if bad_thing_happened:
    # report that bad thing happened
    # stop script
```

Before we implement this in the script, we can write a test for this behavior.
The test should create a directory first, and then try to create with the same media ID.
In psuedo-code:

```py
def test_error_if_dest_path_exists(self):
        # create xfer_path/M1234/M1234-0001
        # run ft.py --id M1234-0001
        # expect ft.py to quit
        # expect ft.py to report "Media may have been transferred, make sure that the entered ID is correct"
```

In real-code we can use most of the code from the previous test.

```py
def test_error_if_dest_path_exists():
    tmpdir = tempfile.mkdtemp()
    preexisting_folder = Path(tmpdir, 'M1234', 'M1234-0001')
    self.assertRaise(Exception, ft.create_transfer_folders(media_id='M1234-0001', ft_path=tmpdir))
```

The new line here is `assertRaise`.
Exceptions require a control word called `raise`, and because they stop a script cold, we have to call the function from within the `assertRaise` function.
