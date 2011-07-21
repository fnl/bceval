from biocreative.evaluation.file_io.abstract import AbstractFieldReader

class GoldStandardFieldReader(AbstractFieldReader):
    "Read lines from the gold standard file."
    
    def result_scores(self, items):
        "Expects neither confidence nor rank in the (GS) file."
        if len(items) - 1 != self.content_items:
            self.logger.warning("wrong number of fields %s %s" % (
                str(items[1:]), self._at_line_x_in_file_y()
            ))
        
        return items[0], items[1:], None, None
    

