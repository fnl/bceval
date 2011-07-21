import logging

from biocreative.evaluation.file_io.base import BaseReader

class AbstractFieldReader(BaseReader):
    """Read lines returning DOI, result_list, rank, confidence tuples.
    
    If the file is_gold_standard, confidence is None.
    If the file has_intrinsic_ranking or is_gold_standard, rank is None.
    Reports and raises ValueErrors if the rank or confidence is not as
    expected.
    Asserts the correct value range for rank and confidence.
    """
    
    def __init__(self, file_path, field_separator, result_order=11):
        super(AbstractFieldReader, self).__init__(file_path, field_separator)
        self.ordering = result_order
        self.logger = logging.getLogger("AbstactFieldReader")
    
    def result_scores(self, items):
        raise NotImplementedError('abstract')
    
    def next(self):
        """Return the next line in the file as a tuple.
        
        [doi, data-list, rank, confidence]
        Rank and confidence are None when reading the gold standard file.
        """
        items = super(AbstractFieldReader, self).next()
        return self.result_scores(items)
    
    def _confidence(self, items):
        "Pop the confidence from the item list."
        new_items, confidence = self._pop_item_as(float, items)
        assert 0.0 < confidence <= 1.0, \
            "confidence not in range ]0..1] %s" % self._at_line_x_in_file_y()
        return new_items, confidence
    
    def _rank(self, items):
        "Pop the rank from the item list."
        new_items, rank = self._pop_item_as(int, items)
        assert rank > 0, "rank must be > 0 %s" % self._at_line_x_in_file_y()
        return new_items, rank
    
    def _pop_item_as(self, Type, my_list):
        "Pop an element from the list and cast to type Type."
        new_list = list(my_list)
        
        try:
            item = Type(new_list.pop())
        except ValueError:
            self.logger.critical("item not type %s %s" % (
                Type.__name__, self._at_line_x_in_file_y()
            ))
            self.logger.warning("possibly unexpected result file columns?")
            self.logger.info("check command line options (--help)!")
            raise
        
        return new_list, item
    
    def _at_line_x_in_file_y(self):
        "Error/debugging message helper."
        return "at line %i in file '%s'" % (
            self.line_number, self.file.basename
        )
    

