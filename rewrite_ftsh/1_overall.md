---
title: Rewriting ft.sh
has_children: true
nav_order: 1
---

We're re-implementing `ft.sh` in order to learn features of Python scripting.
Part of this will be to add features that ft.sh never had.

While bash is a very useful language, there are parts that I find really vague.
These include things like [parsing command-line arguments](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/getopts.html), [converting between data types](https://tldp.org/LDP/abs/html/untyped.html), and [how all the shell expansions work](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html).
These are features that have made it harder for me to write scripts that work the way I want them to.
I will be explaining the difference between bash and Python where I can, but these explanations may be hampered by my own misunderstandings of bash.

## What does `ft.sh` do?

`ft.sh` is a script used by NYPL Digital Archives copy files from digital carriers into a bag, extract technical metadata from the files on the digital carrier, validate the transfer, and report stats.
We will not translate each line of the bash script into Python.
Instead, we'll first extract the features of the script and then implement those from scratch.
This is partly because bash and Python have different syntactic styles.
Like with language translation, our new script will work better if we capture the spirit of the bash script instead of a dictionary translation.

`ft.sh` has lots of comments and explanatory 'echo' statements.
We can use those to create a list of features we need to implement.

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

From this list, the features a Python version will need are:

* Explain the purpose of the script
* Accept user input for the file path of the digital carrier
* Accept user input for the Media ID number (M######-####)
* Extract the Collection number from the Media ID
* Create folders for the bag and metadata based on the collection ID and Media ID
* Create a siegfried report from the digital carrier
* Transfer the files from the carrier to the bag
* Verify the bagging process
* Report the size and file count of the transfer

We'll break these features down into the following lessons.

1. Creating a command-line script with arguments
2. Parsing filepaths and manipulating strings
3. Running bash commands and looking-before-you-leap
4. Using the bagit library and object-oriented programming
