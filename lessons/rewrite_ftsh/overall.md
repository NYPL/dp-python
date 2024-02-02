---
title: Rewriting ft.sh
has_children: true
nav_order: 2
---

We're re-implementing `ft.sh` in order to learn features of Python scripting.
Part of this will be to add features that ft.sh never had.

While shell scripting is a very useful language, there are parts that I find really vague.
These include things like:

* [parsing command-line arguments](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/getopts.html)
* [converting between data types](https://tldp.org/LDP/abs/html/untyped.html)
* [how the shell expansions work](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html).

These are features that have made it harder for me to write scripts that work the way I want them to.
They are also things that I think Python handles more clearly or doesn't have to do.
I will be explaining the difference between bash and Python where I can, but these explanations may be hampered by my own misunderstandings of bash.

## What does `ft.sh` do?

`ft.sh` is a script used by NYPL Digital Archives to perform the following functions:

1. copy files from digital carriers into a bag
2. extract technical metadata from the files on the digital carrier
3. validate the transfer
4. report stats

The source code is in the program's [Github repository](https://github.com/NYPL/digarch_bash/blob/main/Mac/ft.sh).

One way to convert the bash script into Python would be to translate each line of code.
For example, the following code asks for the path to the digital carrier and stores that input to a variable named MediaID.

```bash
echo -e "${BLUE}Please enter the MediaID for this file transfer and hit return:${NC}"
read MediaID
```

This could be written in Python as follows.

```py
MediaId = input("Please enter the MediaID for this file transfer and hit return: ")
```

This approach will eventually run into snags when we encounter lines that don't have direct translations.

```bash
tree "$FTpath/$Collection/$MediaID/objects/$Bag/data" | tail -1
```

The `tree` command recursively lists the files in a directory followed by the total number of files listed.
Taking the final line of the output with `tail` extracts the file count from the output.
If we want to count files in a folder using Python, we would probably use a different method.
First, because there is no equivalent to `tree` in Python.
Second, because the file count is a byproduct of `tree`, and we might not need to produce the tree structure if we won't use it.

The new Python script still needs to accomplish the same goals, but it can accomplish them in a different way.
To do this, we will re-factor the script, first understanding what it accomplishes and then writing new code based on that understanding.
Technically, you re-factor in the same language in order to achieve some other goal, like faster, better documented, or more maintainable code.
For our purposes, it's still useful to think of this shell script to Python script jump as a re-factor.

## Understanding what `ft.sh` does

One way to approach re-factoring is to read through the existing code and then create a generic outline of its logic.
You can do this line-by-line, but `ft.sh` has plenty of comments and `echo`s that explain the intent of the code.

```bash
#This is a program to create Siegfried metadata, bags and validation for file transfers.
#Check that sf conf file is set properly
echo -e "${BLUE}This script will create a file transfer.${NC}"
echo -e "${BLUE}Please drag the SIP folder over this window. See the folder path displayed? Hit return!:${NC}"
echo -e "${BLUE}Please enter the MediaID for this file transfer and hit return:${NC}"
#remove - and disk# to create collection#
#echo -e $Collection
#echo -e $Bag
#designate base path
#create MediaID directory
#create sf csv
#create bag, set to verbose output and exclude hidden files
#verify bag is complete
#verify payload checksums
#output number of files in payload
#output size of payload in kb
```

Some of these comments are leftover code used to debug the script when it was first written, like `#echo -e $Collection`.
Using comments like this is a good intuition, but it can be confusing to other people that may use the script.
We'll talk about ways to limit the need for this.

From the list, I've extracted the following features for the Python version:

* Explain the purpose of the script
* Accept user input for the file path of the digital carrier
* Accept user input for the Media ID number (M######-####)
* Extract the Collection number from the Media ID
* Create folders for the bag and metadata based on the collection ID and Media ID
* Create a siegfried report from the digital carrier
* Transfer the files from the carrier to the bag
* Verify the bagging process
* Report the size and file count of the transfer

We'll break these features down into the following 4 lessons.

1. Creating a command-line interfaces to Python scripts
   * Explain the purpose of the script
   * Accept user input for the file path of the digital carrier
   * Accept user input for the Media ID number (M######-####)
2. Working with filepaths in Python
   * Extract the Collection number from the Media ID
   * Create folders for the bag and metadata based on the collection ID and Media ID
3. Using the bagit module
   * Transfer the files from the carrier to the bag
   * Verify the bagging process
   * Report the size and file count of the transfer
4. Running bash commands from a Python script
   * Create a siegfried report from the digital carrier

But before those lessons, we'll look at a programming concept called test-driven development.
