import logging

from biocreative.evaluation.file_io.base import BaseReader

class HomonymOrthologReader(BaseReader):
    "Read a homonym ortholog mapping file."
    
    def __init__(self, file_path, field_separator):
        super(HomonymOrthologReader, self).__init__(
            file_path, field_separator
        )
        self.logger = logging.getLogger("HomonymOrthologReader")
    
    def next(self):
        items = super(HomonymOrthologReader, self).next()
        
        if len(items) == 1:
            return items[0], list()
        
        return items[0], items[1].split(',')
    

