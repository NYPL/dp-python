---
title: Editing Code
parent: Creating an Environment
weight: 3
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
* linting - syntax checking to ensure text meets the requirements to be interpreted
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

```
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

## Linting

## Built-In terminal

## Extension
