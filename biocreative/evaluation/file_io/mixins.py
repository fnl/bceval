class ACTReaderMixin(object):
    """Extend the FieldReader to return boolean values for the classifcation
    result_list as a Result item.
    """
    
    content_items = 1
    
    def next(self):
        """Return the next result data item in the file as a tuple.
        [doi, Result, rank, confidence]
        """
        doi, items, rank, confidence = super(ACTReaderMixin, self).next()
        classification = items[0]
        
        try:
            classification = bool(int(items[0]))
        except ValueError:
            classification = self._map_to_bool(items[0])
        
        return doi, classification, rank, confidence
    
    def _map_to_bool(self, value):
        "Try to cast a string value to a boolean value."
        if value.lower() in ("f", "false", "n", "+"):
            return False
        elif value.lower() in ("t", "true", "y", "-"):
            return True
        
        raise RuntimeError("illegal classification format '%s' %s" % (
            str(value), self._at_line_x_in_file_y()
        ))
    

class INTReaderMixin(object):
    """Extend the FieldReader to return string values for the normalization
    result_list as a Result item.
    """
    
    content_items = 1
    
    def next(self):
        """Return the next result data item in the file as a tuple.
        [doi, Result, rank, confidence]
        """
        doi, items, rank, confidence = super(INTReaderMixin, self).next()
        return doi, items[0], rank, confidence
    

class IPTReaderMixin(object):
    """Extend the FieldReader to return (ordered) string tuples for the pairs
    result_list as a Result item.
    """
    
    content_items = 2
    
    def next(self):
        """Return the next result data item in the file as a tuple.
        [doi, Result, rank, confidence]
        """
        doi, items, rank, confidence = super(IPTReaderMixin, self).next()
        items.sort()
        return doi, tuple(items), rank, confidence
    

