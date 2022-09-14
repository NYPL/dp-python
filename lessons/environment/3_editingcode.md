---
title: Editing Code
parent: Creating an Environment
nav_order: 3
---

* Using a terminal within VS Code
* Linting Python in VS Code
* Extending VS Code functions

## Using a Text Editor for Code

There are two extremes of software for coding.
One extreme is a raw text editor that's not much more than a blank box, a blinking cursor, and a complex system of keyboard shortcuts developed in the days of mainframes.
`vi` is a good example of this.
The other extreme is an integrate development environment with a graphical user interface for your entire coding projects, available libraries, integrated documentation, compilers, and other bells and whistles.

Our work sits somewhere in the middle. We don't need a million features, but we also need a more forgiving user interface.

There are a few programs that fall in this space. Notepad++, Sublime Text, Atom, and, the program used in this lesson, Visual Studio Code.
These programs allow you to compose text.
They also support very useful features like:

* file browsers - ability to view and organize all the files in a project
* syntax highlighting - formatting to signify how text will be interpreted as code
* intellisense - on-demand help and syntax checking
* command palette - invoking additional tools
* built-in terminals - tabs to run the code while still looking at it
* extension systems - plugins to add additional features beyond the base set

Getting to know your text editor can remove some of the common frustrations of programming.

## Syntax Highlighting

VS Code comes with built-in syntax highlighters for hundreds of programming languages.
As an example of why this features can be useful, look at the following markdown code blocks, one with python syntax highlighting and one without.

```py
def list_printer(x):
    for item in x:
        print(x)
```

```html
def list_printer(x):
    for item in x:
        print(x)
```

The syntax highlighter changes the formatting for the key control words in this snippet. `def`, `for`, and `print` have a new color, and `in` is bolded.
The names of variables or functions that we define are rendered in plain text.
Compared to the un-highlighted snippet, it's much easier to begin making sense of the highlighted version.

The syntax highlighting in this Jekyll page is much less complex than what's available in VS Code.
There different classes of control words receive different colors.
If you import a module, but don't use it, it will be slightly darker.
Each kind of bracket, `(`, `[`, `{`, `<`, etc, is given a different color to improve their legibility when nested.

Since every coding language is different, the highlighting rules change for them as well.
To apply the correct highlighting, VS Code parses the file with machine learning to guess which language is being used.
Features like the file extension are very strong indicators.
Any file ending in `.py` is likely Python.
However, the text in the file is also useful.
Many Python files start with `# /usr/env/python` or `import os`.
The machine learning algorithm uses all of these hints to guess the language being used.

Of course, VS Code could get it wrong.
In that case, the current language is displayed on the bar at the bottom of the window.
Clicking that name brings up a new menu to select another language.

To see how this works in real-time

1. Open a new tab in VS Code. Look for "Plain Text" written on the bottom bar.
2. On the first line, type (don't copy-paste) `import os`
3. Press enter. You should see the color of the text change. The bottom bar should also display "Python".
4. Type `os.listdir()`. You should see the color of `os` on the first line brighten

Experiment with some typos.
For example, create a for-loop using a variable that hasn't been created.
Or nest parentheses within parentheses within parentheses.
Syntax highlighting helps.

## IntelliSense

As you type a statement like `os.listdir()`, you'll notice that a window pops up with possibilities that narrow as you type.
This feature is called IntelliSense.

Try typing the following statement piece-by-piece, `os.path.split()`

* `os.` - the box now shows the methods and classes of `os`
* `path.` - the box shows the methods of the `path` class
* `basename(` - the box shows the definition of the `basename()` method, including the expected arguments, output type, and a brief explanation.

This only works if you have the correct import statement.
IntelliSense is parsing the script, recognizing which modules have been imported, and then importing the definitions form those files.
When trying to write a similar statement like `pathlib.Path.name`, IntelliSense has suggestions for `pathlib` because it is a base Python module.
However, we don't have an import statement in our code, so IntelliSense doesn't offer suggestions after the first period.
Not only is the feature providing on-the-fly definitions, it's also parsing the code and giving feedback on common errors.

You might notice that as you type `pathlib`, an IntelliSense option to `auto-import` pops up.
Selecting this with `<tab>` or `<enter>`, auto-completes `pathlib` and adds the correct import statement at the top of the file.

A final nice feature to recognize is variable auto-completion.
Assign a variable to an inconveniently-long-named variable, like `longVariableName = 'Alice'`.
IntelliSense parses that there is now a variable with that name.
When you refer to the variable again, it is offered as a suggestion.
Try typing, `len(longV` and use tab to complete the statement.

This is both convenient but again can also help with error checking.
The following is example code where the value of a variable should change based on a condition.
Except, the line to reset the variable has a typo.
Now this code creates a variable based on the condition.

```py
longVariableName = 'Alice'
if (logical test):
    longVariablName = 'Bob'
```

IntelliSense will now offer both variables as potentials auto-completes, a subtle but useful alert that something might be wrong.

## Command Palette

Syntax highlighting and IntelliSense can be further configured and invoked differently, as well as many other tools, using a feature called the Command Palette.
Pressing `<cmd> + <shift> + <p>` brings up the Command Palette.
Typing in the desired the tool will narrow down the list of suggestions.

Useful commands include:

* Toggle Word Wrap - wrap long lines of text onto multiple lines to remove need to scroll
* Format Document - can turn a string of JSON into a nested hierarchy
* Create Jupyter Notebook - opens a Jupyter notebook session
* ...

Some of these tools have their own keyboard shortcuts, which are helpfully displayed on the right side of the command palette box.

You can also open the preferences for VS Code from the Command Palette.
As a `pyenv` user, there's a particularly useful setting to create.

1. In the Command Palette, launch `Open User Settings (JSON)`. It will open a new tab.
2. Within the top level of the JSON file (the first set of `{}`) paste the following, `"python.terminal.activateEnvironment": false`
3. Close the tab
4. In the Command Palette, launch `Open User Settings`. You should see a setting that says "Python > Terminal: Activate Environment"

VS Code is a deep system.
Many parts of the underlying system are exposed for customization.
So many parts in fact, that it would be impossible to build a good screen that describes all of them.
Instead, VS Code allows users to set any available setting in a text file, as long as they know the namespace for the appropriate setting.

## Terminal

VS Code has a built-in terminal.
So in addition to helping to check code as it is written, VS Code can be used to run that code while the editor is still visible.
This terminal has access to all of the same shells as the standalone terminal program.

To see it in action, press ``<alt> + <shift> + <`>``.
A pane should appear at the bottom of the VS Code window with the same prompt as your typical shell session.
Running commands like `echo $PATH` and `pwd` should give the same results.

The one issue is that `VS Code` attempts to override `pyenv` without it.
The setup done in the last section fixed this problem.

You may find having access to a terminal like this extremely convenient.

* You can have a Python session running to test out small pieces of code without running the entire script.
* You can bounce back and forth between writing code and editing code as you implement each feature.
* You can run a daemon that auto-recompiles and serves your static Jekyll website
* You can even have multiple shells running within your VS Code terminal so that you can do all of these things.

Like all things within VS Code, this is a matter of personal preference.
You could do all of the same things using a separate terminal program.

## Extension

The final VS Code feature to be aware of is the extension system.
Like browser extension systems, VS Code supports users adding additional functionality to their copy of VS Code.
These extensions range from very simple to very complex.
The only caution is that as you add more and more extensions, it may take VS Code longer and longer to load.

To see the extensions, click on the four square icon in the left sidebar.
It will open a pane with a search box and a list of installed extensions.

Core, useful extensions include:

* Python - which supports the IntelliSense system
* Jupyter - which allows you to run Jupyter notebooks in VS Code

Beyond that, it depends on the work that you do. Search for the following and decide if they make sense for you.

* Rainbow CSV
* markdownlint
* Code Spell Checker
