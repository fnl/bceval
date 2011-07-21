import logging

from biocreative.evaluation.file_io.gold_standard import \
    GoldStandardFieldReader
from biocreative.evaluation.file_io.result import \
    ResultFieldReader
from biocreative.evaluation.file_io.mixins import \
    ACTReaderMixin, INTReaderMixin, IPTReaderMixin

class GoldACTReader(ACTReaderMixin, GoldStandardFieldReader):
    "Gold-standard article reader."
    
    def __init__(self, *args, **kwds):
        super(GoldACTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("GoldACTReader")
    

class ResultACTReader(ACTReaderMixin, ResultFieldReader):
    "Article result file reader."
    
    def __init__(self, *args, **kwds):
        super(ResultACTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("ResultACTReader")
    

class GoldINTReader(INTReaderMixin, GoldStandardFieldReader):
    "Gold-standard normalization reader."
    
    def __init__(self, *args, **kwds):
        super(GoldINTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("GoldINTReader")
    

class ResultINTReader(INTReaderMixin, ResultFieldReader):
    "Normalization result file reader."
    
    def __init__(self, *args, **kwds):
        super(ResultINTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("ResultINTReader")
    

class GoldIPTReader(IPTReaderMixin, GoldStandardFieldReader):
    "Gold-standard pairs reader."
    
    def __init__(self, *args, **kwds):
        super(GoldIPTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("GoldIPTReader")
    

class ResultIPTReader(IPTReaderMixin, ResultFieldReader):
    "Pair result file reader."
    
    def __init__(self, *args, **kwds):
        super(ResultIPTReader, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("ResultIPTReader")
    

def reader_factory(reader_class, evaluation_type):
    """Return the appropriate reader given the reader class (GS or result)
    and the data/evaluation type.
    """
    return eval("%s%sReader" % (reader_class, evaluation_type))

