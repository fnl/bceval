Official BioCreative Evaluation Script
**************************************

This package contains the official evaluation script for BioCreative challenges.

It is compatible with Python 2.5-2.7.
It is not compatible with earlier versions of Python.
It has not been tested with Python 3+ and will most likely not work.

Author: Florian Leitner <fleitner@cnio.es>
The BioCreative homepage: http://www.biocreative.org/

General information on the evaluation script: http://www.biocreative.org/resources/biocreative-ii5/evaluation-library/

============
INSTALLATION
============

Extract the library from the tar.gz:

  tar zxvf bc_evaluation-X.X.tar.gz

And move into the created directory:

  cd bc_evaluation-X.X.X

Global, system wide installation (you need to have admin/sudo permissions):

  sudo python setup.py install

Local, user-only installation (in your home directory, in "~/.local"):

  python setup.py install --user

In case you do a local (user) install, you will have to make sure that the bin directory in "~/.local" is on you PATH, otherwise the bc-evaluate executable will not be found:

  export PATH=$PATH:~/.local/bin

To only test if the installation command will work as you think it should, add the option '--dry-run' to the above commands - you will see what will happen, but the setup script will not copy or do anything.

Documentation on installing python packages (using setup.py):

  python setup.py --help
  python setup.py --help-commands
  python setup.py <command> --help
  python setup.py install --help

==================
USAGE INSTRUCTIONS
==================

UNIX, LINUX, OSX
----------------

The installation process should take care that the executable is installed in a way that it can be run from the command-line without further issues. If not, check the last lines when running the script:

copying build/scripts-2.X/bc-evaluate -> /path/to/some/bin

And make sure that path is in your shell's $PATH environment variable. By default, these locations should be:

- Global install: /usr/local/bin
- Local user-install: ~/.local/bin

After installing, you can read instructions on how to use this tool by running its help and documentation commands:

  bc-evaluate --documentation
  bc-evaluate --help

GENERAL NOTES
-------------

The general way of using this tool is:

  bc-evaluate [options] your_result_files... gold_standard_file

The default (w/o options) works for INT/normalizations and results files that have both confidence and rank values, returning a verbose evaluation report. For all other input/output options, please read the --documentation and the --help output carefully.

============
DEPENDENCIES
============

If you want to use the plotting functionality of the script, you need to install matplotlib, a Python plotting library:

http://matplotlib.sourceforge.net/

Matplotlib requires the following external packages:

python 2.4 (or later, but not python3)
numpy 1.1 (or later)
libpng 1.1 (or later)
freetype 1.4 (or later) [not required to use the plotting functionality of bc-evaluate]

For more information about installing matplotlib, see:
http://matplotlib.sourceforge.net/users/installing.html
