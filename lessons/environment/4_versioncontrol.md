---
title: Version Control
parent: Creating an Environment
nav_order: 4
---

## Goals

* Understanding why version control is good practice
* Configuring git with a remote account
* Using git from where you are

## Why Use Version Control

Writing is almost never a straightforward process.
There are typos, syntax changes, and sometimes wholesale re-writes.
This applies in both document writing and code writing.

The difference with code is that we are frequently writing small machines.
These machines need to have all the right thing in the right places so that they accomplish their task.
And they can get pretty complicated.

When trying to make any changes to code, it could have many outcomes like unintended side effects, abandonment, or hopefully success.
Good practice says that we should make our changes in a copy, rather than overwriting the original.
That way a previously working version is irretrievably lost.
The question is how to do that.

One common technique is to create a new file yourself.
For example, scriptname_todaysdate.py to represent the state of the code today.
But these approaches run into issues quickly.
How do you decide when to save?
At the end of the day or at the last working version?
How do you manage the growing backlog of old version?
What do you do when you have two versions you want to save on the same day?

Rather than trying to develop a system ourselves, managing versions is best left to software designed for it.
That's version control software.
And of the many available systems to manage versions, `git` is one of the most common.

In `git`, the entire project is contained in a repository.
Each repository has at least one branch that represents a single state of all of the files.

1. If you want to make a change, you can make a new branch.
2. As you make changes, you can snapshot the state of the files with commits.
3. Once you finish making all the changes and your code works, you can merge it back into the main branch.

The above is one general method to use `git`.
There are other strategies, but all are generally built around one principle.
How can we make sure that our version history can manage both working code and code-in-progress.

### Sharing version control

If you stick to a good version control strategy, you can use that to better collaborate with others.
Multiple people can contribute to the same repository, as long as they have a shared service to keep everyone's copy up-to-date.
This is the role of services like Github and Gitlab.

To use them, you need to establish a user account with the service and then to configure your local `git` software with that account.

### Configuring git with a remote account

There are multiple methods to configuring `git`.
Currently, Github recommends using a [Personal Access Token](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git). Alternatively, you can setup [SSH authentication](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

Either method is fine for the purposes of this lesson; however, it is important that you're command-line version of `git` has access to these credentials.

## Using git wherever you are

Once you have `git` configured, you'll find that it's available wherever it needs to be.
Of course, it's available in the terminal where you set it up.
It's also available in any terminal that you are using, whether standalone or embedded in a program like VS Code.
Finally, it's probably available in the Github extension for VS Code.

### VS Code and `git`

One of the first icons in the left sidebar of VS Code is a branching set of three circles.
Clicking on that icon opens the version control panel.
By default, this panel will encourage you to open or clone an existing repository.
Once you do that, it will give you a visual interface to the version control system that you are using.

1. In a terminal session, create a new directory, `mkdir ~/gittest`.
2. Initialize the new directory as a git project, `git init ~/testdir`.
3. Open the directory with VS Code, `code ~/gittest`.

When you open the version control panel, the interface has changed.
The Explorer view (the two-file icon in the left sidebar) has also changed.

* Create a new file by opening a tab, entering some text, and saving the file.
* Open the Explorer view, and notice that the file name is highlighted green with a `U` to the right.
* Open the Version Control view, and notice that the file name is listed under Changes.
* Open a VS Code terminal, run `git status` and notice that the file is listed as "Untracked".

VS Code is keeping track of the repository and flagging information about its state in many ways.

You can also commit files to the repository through a combination of these tools.

1. Open the Version Control view, and click the `+` next to the file.
2. Open the Explorer view, and notice that the `U` has changed to `A`.
3. Open a VS Code terminal, run `git status` and notice that the file is listed as "New file to be committed".
4. Go back to the Version Control view, type "created new file" in the Message box, and press the "Commit" button.
5. Open the Explorer view, and notice that the file is now white.
6. Open a VS Code terminal, run `git status` and notice that there is nothing to report.

In practice, you will likely prefer one method (Version Control view or Terminal); however, it can be easier to have the visual reinforcement of the view or the speed of entry of the command-line.

A powerful feature of the VS Code `git` integration is live display of the changes to the file.

1. Open your file and add some more text, delete the original text, and/or edit the original text.
2. Save the file.
3. Open the Explorer view, and notice that the file name is now orange and there is an `M` next to it.
4. Look in the editor tab, and notice the colored bars next to the line numbers on the left side. Click on the bars to see a diff between the current state of the file and the committed state.
5. Look in the scroll bar to the right and notice those same colors appear.
6. Open a VS Code terminal, run `git diff` and notice the same differences displayed.

These indicators are extremely useful for understanding what changes have been made to a file since the last commit, especially accidental changes.

## Strategies for `git` usage

It's beyond the scope of this guide to discuss the best strategies and workflows for using `git`.
The following are general guidelines.

* Many small commits are better than one big commit.
Find a unit of content that makes sense for your work.
Maybe a function, a few paragraphs, an editing stage.
* Use the commit message to figure out a good commit strategy.
  * `Fixed typos` is good.
  * `Added section on disk imaging` is good.
  * `Refactored file listing function` is good.
  * `Added three new features and fixed some stuff` is too big.
* Commit changes from only a few files at a time, preferably 1.
* If you forgot to do the following, give yourself some slack and make some bulk commits, only after you check each change.
We're aiming for good practice, not best.
