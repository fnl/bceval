import os

class Files(object):
    "File handles and path names storage object."
    
    class File(object):
        "Wrapper"
        
        def __init__(self, name):
            """Name is usually a path name, but also can be an open handle 
            (such as sys.stderr or sys.stdout).
            """
            self.name = name
        
        def __str__(self):
            return str(self.name)
        
        def __repr__(self):
            return repr(self.name)
        
        def open(self, mode='r'):
            "Open FH if it is a named handle."
            if isinstance(self.name, str):
                self._fh = open(self.name, mode=mode)
            else:
                self._fh = self.name
            
            return self._fh
        
        def close(self):
            "Close FH is it is a named handle."
            if isinstance(self.name, str):
                self._fh.close()
        
        @property
        def basename(self):
            "Return the basename of this file."
            if isinstance(self.name, str):
                return os.path.basename(self.name)
            else:
                return "%s stream" % self.name.__class__.__name__
        
        @property
        def rootname(self):
            "Return the root name of this file without extension."
            if isinstance(self.name, str):
                return os.path.splitext(self.basename)[0]
            else:
                return "stream"
    
    def __init__(self, **paths):
        """Set up the File objects - defaults to None."""
        self.gold_standard = None
        self.results = None
        self.homonym_orthologs = None
        self.protein_organisms = None
        self.output = None
        
        for attr in paths:
            if attr == 'results':
                self.results = [
                    Files.File(path) for path in paths['results']
                ]
            elif hasattr(self, attr):
                if paths[attr] is not None:
                    setattr(self, attr, Files.File(paths[attr]))
            else:
                raise ValueError("unknown file type %s" % attr)
    
