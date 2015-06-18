#---------------------------------------------------------------------------
try:
    __IPYTHON__
except NameError:
    IN_IPYTHON = False
else:
    IN_IPYTHON = True

#---------------------------------------------------------------------------
def checkPathExists(name, path):
    if not os.path.isdir(path):
        raise Exception('%s path %s does not exist or is not a valid directory.' % (name, path))

#---------------------------------------------------------------------------
def checkFileExists(name, path):
    if not os.path.isfile(path):
        raise Exception('%s file %s does not exist or is not a valid file.' % (name, path))

#---------------------------------------------------------------------------
def mkdir_p(path):
    """Recursive directory creation function.
    See http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise