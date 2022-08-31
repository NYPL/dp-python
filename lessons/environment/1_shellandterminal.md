---
title: Shell and Terminal
parent: Creating an Environment
weight: 1
---

## Goals

* Understanding shell, terminal, and path
* Customizing the shell environment
* Customizing a prompt

## Terminal, Shell, and Session

The terminal/shell/bash/etc can be mysterious.
Everyone calls it something different.
The default interface gives you nothing, just a blinking cursor.

First off, terminology.

* shell - An interface by which to launch other programs. Typically refers to a command-line interface.
* `bash`/`zsh`/`fish`/`sh` - Different shells, each with different features. `sh` is one of the earliest shells. `bash` is the default Linux and pre-MacOS 10.11 shell. `zsh` is the current MacOs shell.
* terminal/console - The program/device that runs a shell. One terminal can run multiple shells.
* session - a single running instance of a shell.

As an example, when you open Terminal on macOS, it automatically starts a session of `zsh`.
If you don't like `zsh`, you can run a different shell, if it's installed.
Running the command `bash` starts a session of that shell, within the already running `zsh` session.
If you want to leave the `bash` session, run `exit` and you'll return to the original `zsh` session.
If you open a new tab in Terminal, it will start another `zsh` session.

The important thing about sessions is that programs depend on the session they were started in.
From the previous example, if you start transcoding a video file in the second tab and then close the first tab, it does not affect the transcode.
If you close the tab where the transcode is running or the terminal window that holds the tab, the transcode will stop.

It's useful to build an understanding of how these concepts relate as you use command line more often.
For example, using `ssh` to connect to a virtual machine starts a shell session on that virtual machine.
Closing the `ssh` session, the shell session you ran `ssh` in, or the terminal for that shell session, will stop whatever process you started on the VM, unless you take specific actions to avoid it.

It's also useful to know and use the more correct terminology.
Since macOS now uses `zsh` by default, it feels strange to advise someone to "learn `bash`".
Better advise would be to learn command-line interfaces, using terminals, programming in a shell, or other more general statements.
Of course, we're not going to fix the general confusion over terminology here, and these lessons likely still make plenty of mistakes.
As will all things technology, ["Be liberal in what you accept, and conservative in what you send."](https://en.wikipedia.org/wiki/Robustness_principle)

## PATH

How does a shell take input like `ls` and understand to run a program called program that returns a directory listing?
In brief, the shell is configured to look in a few locations for a program called `ls`.
Those locations are defined in a variable called `PATH` in most shells.
To see your `PATH`, print it in a shell session.

```sh
echo $PATH
```

(The `$` in the command is required for the shell to understand to look for a variable.
Otherwise, `echo`  will try to open a file in the current working directory called `PATH`, which probably doesn't exist.)

A default `PATH` might look like this.
`/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`
The shell interprets this as four locations: `/usr/local/bin`, `/usr/bin`, `/bin`, `/usr/sbin`, and `/sbin`.
It will looks for a file called `ls` in each location starting from `/usr/local/bin` until it finds a file, and then run that file.

We can mimic this behavior by listing the contents of each folder, and searching for a file called `ls`

```sh
ls /usr/local/bin | grep ^ls$
ls /usr/bin | grep ^ls$
ls /bin | grep ^ls$
> ls
```

It doesn't matter if there is an `ls` in `/usr/sbin` or `/sbin`.
The shell stops searching as soon as it finds the copy in `/bin`.

If we wanted to use a different version of `ls` without overwriting the default version, we could install a file to `/usr/local/bin` or `/usr/bin`.
We could also install it to a different folder, and add that folder to the `PATH`.

A more complex `PATH` might look like this.

`/Users/Alice/.pyenv/shims:/Users/Alice/.pyenv/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`

The user named Alice has configured their shell with two additional programs, `pyenv` and `homebrew`.
Programs installed via `pyenv` and `homebrew` are found in `~/.pyenv/shims`, `~/.pyenv/bin`, `/opt/homebrew/bin`, and `/opt/homebrew/sbin`.
If Alice wants the updated version of `ls` available on homebrew, it is installed to `/opt/homebrew/bin`, leaving the original alone.

Adding instead of overwriting is a good technology practice.
What if the most recent version of `ls` is utterly broken with some bug?
We can use `homebrew uninstall ls`.
But, how do we go back to the working version that we and system process rely on?
Backups?
Finding the original from some online repository?
The most reliable solution is to not disturb the original program.

How do we update `PATH`?
You might have seen instructions like this during an installation.
(Do not run this example.)

```sh
export PATH=/some/path/to/dir/:$PATH
```

Reading this from right to left:

* `$PATH` returns the current `PATH`
* `/some/path/to/dir:` is a string that should be printed in front of `PATH`, the colon is the required separator for `PATH`
* `PATH=` assigns the total string constructed to the right to `PATH`, overwriting whatever `PATH` was before
* `export` updates the environment of the current shell session so that all process that use `PATH` retrieve the new value

It's important that `export` only updates `PATH` for the current session.
If you start a new session, `PATH` will not include the new value.
For that reason, you might see this command in installation instructions.

```sh
echo "export PATH=/some/path/to/dir/:$PATH" >> ~/.profile
```

Why the echo?
Why the `>>`?
What is `~/.profile`?

## Customizing your shell environment with a profile

Every time you load a shell session, it has a number of settings already configured.
These settings can be used by the programs you run during the session.
For example, `PATH` stores where programs should be searched for.
`HOME` stores the path of the directory that can be referenced as `~`.
These settings are the environment of the session.

Over time, you may wish to customize the default environment.
A common example is modifying `PATH` to access additional programs.
Part of the environment is a series of files where the settings are defined.
When the shell session starts, these files are loaded and executed in a specific order.
The first of these are system files that you generally shouldn't edit.
The last of these files are in your home folder, and are where you can customize the shell environment, even overriding settings from the earlier files.
These user-defined files are often referred to as your profile.

The name of the profile file depends on the shell.
For `bash`, the recommended profile is `~/.bash_profile`.
For `zsh`, the recommended profile is `~/.zshrc`.
There are additional potential locations that are beyond my ability to discuss but can be researched on your own.
In this lesson, `~/.profile` is used to generically refer to the profile that is most appropriate for you.

Then what does the `echo "export PATH..." >> ~/.profile`?

* `echo` returns the `"export ..."` as a string instead of running it
* `>> ~/.profile` appends that to the end of the profile file

The command only appends the command to the profile.
Future shell sessions will run the code, but the current session is still running on the old profile.
To update the session with the new profile session, run `source ~/.profile`

The problem with `>>` appending to your profile is that the profile becomes a long list of contextless commands.
Since you are configuring your environment, you probably want to organize and annotate these lines.
As the `echo ... >>` indicates, the profile is a text file.
So let's use a text editor instead.

There are shell-based text editors like `nano` (easier-to-use) and `vi` (more complicated).
These lesson use Visual Studio Code, so we'll use that.
Adapt the following command with the path to your profile.

```sh
"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ~/.profile
```

This should open the profile in a VS Code window.
Depending on how you've used your computer, this file might be empty or full.
If it is full, take some time to read through the various lines.
If there's anything you don't understand, you should probably add comments on the lines above.
If there's anything that looks like a duplicate or conflict, think about cleaning it up.
Keep in mind that the profile is read and executed from top to bottom.

### Adding to the profile

It is convenient to launch VS Code from the terminal, but cumbersome to use that path.
Let's update the profile by adding the path to `code` to `PATH`.
In future shell sessions, we can open any file or directory in VS Code with the command `code path/to/dir/or/file`

If the `PATH` has already been updated with the VS Code path, consider updating it with some of the advice below.

1. Go to the end of the file and add a couple new lines
2. Add a comment about you addition, like "Launch VS Code from shell"
3. Add a line to update the `PATH`. In this case, add the directory that contains `code` to the end of `PATH` since only one program will be found there. `export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"`
4. Add one more new line to the file to make it easier for future editors (yourself).
5. Save the file.
6. In your original shell session, run `source ~/.profile` and then `code` to test the change.

```txt

# Launch VS Code from shell
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"

```

Keep this loop of comment-code-save-load in mind.
Often, profile changes that make sense at the time unintelligible when you review them later.
Comments help you keep track of what you're doing and can prompt ideas about how to better organize your profile as you continue customizing it.

## Shell Prompts

One of the obvious changes between shells is the information presented to you at the prompt.
Using `sh`, the default prompt is `sh-3.2$`.
Using `bash`, the default prompt is `bash-3.2$`.

It's nice to know the shell and the version number, but maybe there's more useful information.
For example, I have made the following customization to my `zsh` prompt.

* A status indicator that says if the last command completed as expected (√ in green) or had an error (? in red)
* The name of the current working directory in bold to remind me where I am
* A percent sign instead of dollar sign as my delimiter because it looks nicer to me
* A timestamp on the right side of the terminal to keep track of when the last process completed

There are many ways to customize your prompt.
Each depends on the shell and sometimes it requires additional programs.
And often, the syntax for these customizations is cryptic.
To accomplish the above customizations on a base install of `zsh`, I added the following to my profile after cribbing a lot of examples.

```sh
# Configure ZSH prompt
```

I understand this enough to tweak aspects of it, but not enough to really change it.
My advice is to start from what other people have shared online and keep your configuration simple.
