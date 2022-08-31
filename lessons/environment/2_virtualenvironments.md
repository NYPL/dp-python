---
title: Virtual Environments
parent: Creating an Environment
weight: 2
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
> awscli        1.6.1
> ...
cd ../
pip list
> ...
> awscli        1.8.1
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
