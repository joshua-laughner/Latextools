# Latextools
Command line tools to automate tedious tasks for Latex files.

## Quickstart (Linux/Mac)

Install with python3. In the top directory of the repository:

```
python3 setup.py install --user
```

(You may omit the `--user` flag if you have admin privileges
to install in the system directories of your machine, but that is
not recommended.)

Pay attention to the output during installation: look for the line
*"Installing latextools script to ..."*. This will be followed by
a directory, that directory must be on your path for `latextools` 
to be found by your shell.

To check: in Terminal, type `echo $PATH`. If you do see that path,
 then there's nothing else to do.

If you do not see that
directory, look in your home directory for one of the following 
hidden files:

1. `.profile`
2. `.bashrc`

Edit the first one that you have and add the line:

```
export PATH="$PATH:<install_dir>"
```

where `<install_dir>` is the directory latextools was installed into.

To get started, type `latextools -h` to see the list of possible subcommands.

## Utilities

Similar to `git`, `latextools` is broken down into several subcommands.
Therefore to execute one, you would type `latextools <sub-command> <options>`,
e.g. `latextools freeze-xrefs MyPaper.tex`.
 
Currently the available utilities are:

* `freeze-xrefs`: converts external references made using the package "xr" into
static text. Useful for scientific papers where you want to cross-reference
between the main paper and supplement, but the journal does not allow the "xr" 
package during final submission.
* `collect-figs`: makes copies of image files referenced in a Latex file into a 
specified folder, named by default "Fig1.png", "Fig2.eps", etc. Useful again for 
scientific journal submissions where you are expected to upload your figures as 
files numbered in that way.
