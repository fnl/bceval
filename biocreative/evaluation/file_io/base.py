import logging

class BaseReader(object):
    "Read lines that have been separated by a given field separator."
    
    def __init__(self, file_path, field_separator):
        self.file = file_path
        self.field_separator = field_separator
        self.handle = None
        self.line_number = None
        self.logger = logging.getLogger("BaseReader")
    
    def __iter__(self):
        self.handle = self.file.open()
        self.logger.info(
            "loading file '%s'" % self.file.basename
        )
        self.line_number = -1
        return self
    
    def next(self):
        "Return the next line in the file as a field-separated tuple."
        try:
            line = self.handle.next()
        except StopIteration:
            self.file.close()
            raise
        
        self.line_number += 1
        return line.strip().split(self.field_separator)
    

