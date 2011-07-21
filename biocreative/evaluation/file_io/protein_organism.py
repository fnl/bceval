import logging

from biocreative.evaluation.file_io.base import BaseReader

class ProteinOrganismReader(BaseReader):
    "Read a accession to taxonomic ID mapping file."
    
    def __init__(self, file_path, field_separator):
        super(ProteinOrganismReader, self).__init__(
            file_path, field_separator
        )
        self.logger = logging.getLogger("ProteinOrganismReader")
    

