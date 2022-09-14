---
title: Virtual Environments
parent: Creating an Environment
nav_order: 2
---

## Goals

* Managing Python versions
* Managing Python modules

## What is a virtual environment

A shell session has an environment that includes many configurations.
If you want to change that environment, you can alter those configurations for the duration of the session, customize your profile to create a new default environment, or load a different shell.
None of these options work well if you want to repeatedly alter a part of the environment in the same way while retaining most of the existing environment.

For example, you have a set of scripts that was written in Python 3.6 and another set that was written in Python 3.10.
You don't have the resources to update the Python 3.6 scripts right now, but you still need to use them.
Ideally you would be able to do the following `python 3.6project/script.py` and `python 3.10project/script.py` and each would use the right version of Python.

Or maybe you are working on a project using the `bagit-python` module, and new version came out.
That new version has a feature that would make your day-to-day calls of `bagit.py` easier, but you also need some time to make sure that new version doesn't break your project.

This is what virtual environments are for.
They give you the ability to create environments with all the right tools installed and that you can turn on and off as needed.

There are a number of virtual environment managers.
If you have used anaconda, you might be familiar with `conda`.
You might have heard about the Python `virtualenv` module.
In Ruby contexts, `rbenv` is very common.

For this lesson, we're using a combination of two tools, `pyenv` and `pyenv-virtualenv`.
They combine very nice features of `rbenv` and `virtualenv`.
From `rbenv`, we get the ability to install multiple versions of Python and to associate any working directory with a specific version.

```sh
pyenv global 3.9.4
cd path/to/project/dir
pyenv local 3.7.13
python -V
> 3.7.13
cd ../
python -V
> 3.9.4
```

That means that once a version of Python is configured for a folder, we don't have to do anything extra as long as we are working within that directory.
In other virtual environments, you might have to run code like `source venv/bin/activate`.

We can also quickly change between versions quickly.

```sh
pyenv local 3.7.13
python script.py
# script works as expected
pyenv local 3.9.4
python script.py
# script returns an error that we'll need to address to upgrade to 3.9.4
```

`python-virtualenv` adds module management to the mix.
If we need a specific version of a module for a project, we can create a virtualenv associated just to the project's directory.

```sh
pip install bagit
cd path/to/project/dir
pyenv virtualenv 3.7.13 project-env
pyenv local project-env
pip install bagit==1.6.1
pip list
> ...
> bagit        1.6.1
> ...
cd ../
pip list
> ...
> bagit        1.8.1
> ...
```

There is a learning curve to using virtual environments.
They can require that you change some of your typical practices.
If you often call scripts from another working directory, e.g. `python ~/dev/project-dir/script.py`, you might need to change that practice.
If you forget which virtual environment you're using, you'll probably become very practiced at running `python -V` or `pyenv local`.

Once virtual environments feel familiar, they might become part of your default project start-up.

```sh
mkdir new-project
cd new-project
pyenv virtualenv 3.9.4 new-project-env
...
```

But to use them, we need to install the tools.

## Install `pyenv` and `pyenv-virtualenv`

The most up-to-date installation directions are available on the [`pyenv`](https://github.com/pyenv/pyenv#installation) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installation) GitHub repos.
This section presents one method installing the tools to demonstrate ideas from the previous lesson.

### Install via homebrew

```sh
brew install pyenv pyenv-virtualenv
```

### Configure your shell profile

In order for `pyenv` to pull up the correct version of Python, it needs to be part of the `PATH`.
The program also needs to be initialized whenever you start a new session.
Both of these are functions that can be run from a profile.

Open your profile in code, `code ~/.profile` and add the following if it has not been added already.

```sh
# Configure pyenv
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Save and close the profile.

### Test the installation

Open a new shell session and see if `pyenv` is correctly configured by running some of its commands.

```sh
pyenv versions
> system
pyenv global
> system
```

## Using `pyenv`

Once `pyenv` is installed, you have the power to run as many different Python environments as you need.

### Installing Python Versions

First, install a new version of Python.
`pyenv` tracks all major and minor releases of Python back to version 2.1.3.
It also track several related distributions, such as `minipython` and `pypy`.
To see the full list,

```sh
pyenv install --list
```

We're only interested in the main releases at the top of the list, like 3.9.6 and 3.7.13.
As an example, install one of the last versions of Python 2, 2.7.18.

```sh
pyenv install 2.7.18
```

Once the install finishes, list the versions of Python avaialable to `pyenv`.

```sh
pyenv versions
```

> Note, not all versions of Python are installable via `pyenv`.
> For example, any version less than 3.9 has to be specifically patched to work on a Mac with Apple Silicon.
> 2.7.18 is one of these patched versions.

### Using `pyenv` in a shell session

`pyenv` can be used to temporarily change the Python session for a shell session.
To demonstrate, we can try using f-strings, which were introduced in Python 3.6.

```sh
# change the python version in this shell session
pyenv shell 2.7.18
# run the python interpreter
python
```

```py
string = 'hello'
f'{string} f-strings are useful'
# should result in a syntax error
```

Starting a new shell session or switching `pyenv` back to the system Python version shows gets a version of Python that can use f-strings.

```sh
pyenv shell system
python3
```

```py
string = 'hello'
f'{string} f-strings are useful'
# 'hello f-strings are useful'
```

### Creating a `pyenv` environment

Setting `pyenv` for a shell session is useful for experimentation.
When you want to freeze a version of Python alongside a project, you can set a local `pyenv` variable.

```sh
mkdir ~/oldpy
cd ~/oldpy
pyenv local 2.7.18
# confirm the version
python -V
```

As with many things terminal related, this is accomplished by a text file.
`pyenv version` reports both the current version/environment and how that version was set.
When using a locally set version, this should be the path to a file called `.python-version` in that directory.

```sh
pyenv version
# ... oldypy/.python-version
cat ~/oldpy/.python-version
# 2.7.18
```

The extremely useful behavior is that `pyenv` will automatically use this version whenever the shell is in that directory or a child directory.
It will also stop using that version whenever it's not in that directory.

```sh
cd ../
pyenv version
cd oldpy
pyenv version
```

If you need to change the local version of Python, run `pyenv local (version number)`.
If you don't want to have a local version of Python, run `pyenv local system` or delete the `.python-version` file.

### Creating a `pyenv` virtual environment

Creating environments that use the same version of Python but different versions of Python modules is the next step in customization.
For this, you need to first create the environment with `pyenv virtualenv (Python version) (environment name)`.
Once created you can use that environment with the same `local` and `shell` commands.

```sh
# create the environment
pyenv virtualenv 2.7.8 oldbagit
# associate a directory with the environment
cd ~/oldpy
pyenv local oldbagit
```

When working in the virtual environment, new modules are installed only to that environment.

```sh
cd ~/oldpy
pip install bagit==0.1p
pip list
# ... bagit
pyenv shell 2.7.8
pip list
```

## Removing Environments

Eventually you might create a whole garden of Python versions and virtual environments that can be managed by `pyenv`.
Eventually that garden might feel overgrown and in need of pruning.
For that, `pyenv uninstall (version or name)` will remove all the source files.

```sh
pyenv uninstall oldbagit
pyenv uninstall 2.7.8
```

This removes the source files, but any folders that used those versions will still have that value in `.python-version`.

```sh
cd ~/oldpy
pyenv version
```

To clean this up, you will need to either set a new local version or delete the file.
