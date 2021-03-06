## MEPReader
A python utility for interpreting EMG data

### System Prerequisites
=
#### Windows
* A Terminal: you can use `cmd.exe` but I recommend [Git for Windows](https://msysgit.github.io/)
* [Python 2.7.x](https://www.python.org)
  * Install python into the default option `C:\Python27` if you can.  Then, edit your PATH environment variable to include `C:\Python27` (instructions [here](https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/sysdm_advancd_environmnt_addchange_variable.mspx?mfr=true)).
* [Pip](https://pypi.python.org/pypi/pip) for python package management
  * Pip is included in the standard python installation on windows.  Simply add the `C:\Python27\Scripts` directory to your `PATH` variable (separate directories using a semicolon), and pip should be accessible from the command line.

#### Mac OS X
* [Python 2.7.x](https://www.python.org)
* [Pip](https://pypi.python.org/pypi/pip) for python package management
  * First, try this: open a terminal and run the command `sudo easy_install pip`.  If this doesn't work,
  * Download [get-pip.py](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py) and run the command `sudo python /path/to/get-pip.py` in your terminal.

=

### Python prerequisites
=
#### Windows
Many of these packages have been archived by Christopher Gohlke in order to be easy to install.  For several of these requirements, I'll link to his [Unofficial Windows Binaries page](http://www.lfd.uci.edu/~gohlke/pythonlibs/).  Simply find the package you want, select the correct version based on your architecture (32- or 64-bit) and python version (use "27" or "26" depending on the version of Python you downloaded).  For example:

| Your Python Version  | Your system architecture | You should download |
| -------------------- | ------------------------ | ------------------- |
| 2.6.x  | 32-bit  | numpy‑1.9.2+mkl‑cp26‑none‑win32.whl|
|        | 64-bit  | numpy‑1.9.2+mkl‑cp26‑none‑win_amd64.whl|
| 2.7.x  | 32-bit  | numpy-1.9.2+mkl-cp27-none-win32.whl|
|        | 64-bit  | numpy‑1.9.2+mkl‑cp27‑none‑win_amd64.whl|

A wheel is a ZIP-format archive with a specially formatted filename and the .whl extension. More info on python wheels [here](https://pypi.python.org/pypi/wheel).  Once you download the correct wheel file, use pip in the terminal to install it:
```bash
pip install C:\Users\chris\Downloads\numpy‑1.9.2+mkl‑cp27‑none‑win_amd64.whl
```

* [NumPy](http://www.numpy.org/) for numerical computing
  * [Gohlke's NumPy+MKL packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
  * Alternatively, try the most recent supported version [ 1.9.2 available on the sourceforge page](http://sourceforge.net/projects/numpy/files/NumPy/1.9.2/) (not much advantage since Gohlke has archived 1.9.2).
* [matplotlib](http://matplotlib.org/) for plotting
  * [Gohlke's matplotlib packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib)
  * Alternatively, the most recent wheels are available on the [matplotlib download page](http://matplotlib.org/downloads.html) (once again the previous link already has 1.4.3 which is sufficient).
* [neo](https://pythonhosted.org/neo/) for reading electrophysiology data in Python
  * Run the command `pip install neo` in your terminal.
 
=
#### Mac OS X
* [NumPy](http://www.numpy.org/) for numerical computing
  * Run `sudo pip install numpy` in your terminal.
* [matplotlib](http://matplotlib.org/) for plotting
  * Run `sudo pip install matplotlib` in your terminal.
* [neo](https://pythonhosted.org/neo/) for reading electrophysiology data in Python
  * Run `sudo pip install neo` in your terminal.

[ImportError: cannot import name _thread](http://stackoverflow.com/questions/27630114/matplotlib-issue-on-os-x-importerror-cannot-import-name-thread) -- Sometimes the matplotlib install fails on newer versions of OSX. The fix mentioned in the link is:
```bash
sudo pip uninstall python-dateutil
sudo pip install python-dateutil==2.2
```

### Download the MEPReader
If you have [git](https://git-scm.com/) available in your command line or terminal, execute:
```bash
git clone git://github.com/chrismullins/MEPReader.git
```
or simply download and extract the tarball from this page.

### Run
To run the application, start a terminal, then execute:
```bash
python bin/MEPReaderApp.py --help
usage: MEPReaderApp.py [-h] [--version] [-v] [--plot] [--plotDerivative]
                       [--pairedPulse] -i FILENAME [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         increases log verbosity for each occurence.
  --plot                Plot the signal. Requires matplotlib. (Helps to debug
                        missed triggers)
  --plotDerivative      Plot the derivative under the EMG signal. (Helps to
                        debug missed triggers)
  --pairedPulse         These are paired pulse data.
  -i FILENAME, --inputFile FILENAME
  -o OUTPUT_FILE        redirect output to a file
  ```
  
### Usage
The application takes one required argument (the `.smr` input file) and can be used to plot the results, write the results to a file in the comma-separated value format (CSV) or both.  For example, the command:
```bash
python bin/MEPReaderApp.py -i C:/Data/ppTMS_Visit_1/004_CSP000.smr --plot
```
will open a plot looking something like this:
![alt tag](https://raw.githubusercontent.com/chrismullins/MEPReader/793a06a7ceaa556d2e4e34cc42e55259ee4dc262/Resources/images/test_ppTMS_1.png)

Use the zoom-to-rectangle tool in the lower left-hand corner to isolate one trigger and the corresponding response.  If the script ran correctly, you should see something like this.  The green area indicates the window in which the script looks for a min and max response.  If any of the annotations for the trigger, min, or max responses are incorrect, open a bug report with the development team (walk over and tell me about it).
![alt tag](https://raw.githubusercontent.com/chrismullins/MEPReader/793a06a7ceaa556d2e4e34cc42e55259ee4dc262/Resources/images/test_ppTMS_2.png)

This provides a quick way to check whether the script is working incorrectly, or the data are just unusual.
