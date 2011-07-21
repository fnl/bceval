from biocreative.evaluation.file_io.abstract import AbstractFieldReader

class ResultFieldReader(AbstractFieldReader):
    "Read lines for the result file."
    
    strict = False
    
    def result_scores(self, items):
        "Read confidence and rank according to ordering."
        total_columns = self.content_items + 1 # plus doi
        if self.ordering % 10 == 1:
            total_columns += 1 # plus confidence
        if self.ordering % 100 >= 10:
            total_columns += 1 # plus rank
        
        # report missing columns (any mode)
        # report additional columns (strict mode)
        # remove additional columns (non-strict mode)
        if len(items) < total_columns:
            self.logger.error("insufficient number of fields %s %s" % (
                str(items), self._at_line_x_in_file_y()
            ))
        elif self.strict and len(items) != total_columns:
            self.logger.warning("too many fields %s %s" % (
                str(items), self._at_line_x_in_file_y()
            ))
        elif len(items) > total_columns:
            self.logger.info("ignoring additional fields %s %s" % (
                str(items[total_columns:]), self._at_line_x_in_file_y()
            ))
            items = items[:total_columns]
        
        items, rank, confidence = self._extract_rank_and_confidence(items)
        doi = items[0]
        items = items[1:]
        
        assert not (rank is None and confidence is None), \
            "both rank and confidence undefined %s" % \
            self._at_line_x_in_file_y()
        return doi, items, rank, confidence
    
    def _extract_rank_and_confidence(self, items):
        """Extract rank and confidence values according to the ordering
        parameter.
        """
        rank, confidence = None, None
        
        if self.ordering % 10 == 1:
            items, confidence = self._confidence(items)
        
        if self.ordering % 100 >= 10:
            items, rank = self._rank(items)
        
        if self.ordering >= 100:
            rank = self.line_number + 1
        
        return items, rank, confidence
    

