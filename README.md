## MEPReader
A python utility for interpreting EMG data

### System Prerequisites
=
#### Windows
* A Terminal: you can use `cmd.exe` but I recommend [Git for Windows](https://msysgit.github.io/)
* [Python 2.7.x](https://www.python.org)

#### Mac OS X
* [Python 2.7.x](https://www.python.org)

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
  * Alternatively, the most recent wheels are available on the [matplotlib download page](http://matplotlib.org/downloads.html) (once again the previous link already has 1.4.3 which is sufficient)
