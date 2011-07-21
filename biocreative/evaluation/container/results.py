import logging

class ResultContainer(object):
    """Stores the result together with the rank and confidence (if given).
    
    Implements result ordering:
    Orders the results by rank (if both have a rank) or by confidence (if
    both have a confidence), otherwise by the result itself.
    """
    
    def __init__(self, item, rank=None, confidence=None):
        """Initializes a special order logic for negative ACT classification
        results.
        """
        self.item = item
        self.rank = rank
        self.confidence = confidence
        self._boolean = False
        self._ordering = 1
        self.logger = logging.getLogger("ResultContainer")
        
        if isinstance(item, bool):
            self._boolean = True
            
            if item is False:
                # special ACT logic: change order sense for negative results
                self._ordering = -1
    
    def __cmp__(self, other):
        """Specialization for ordering the results.
        
        Takes care of the order logic for both protein and article
        classification results.
        """
        if type(self.item) != type(other.item):
            raise TypeError(
                "comparing items (%s: '%s' vs. %s: '%s')" % (
                    self.item.__class__.__name__, str(self.item),
                    other.item.__class__.__name__, str(other.item),
                )
            )
        elif self._boolean and self.item != other.item:
            # sort boolean result items by their boolean value first
            return self.__first_if_true()
        elif self.rank is not None and other.rank is not None:
            # comparing evaluation file data - both have a rank:
            return self.__cmp_rank(other)
        elif self.confidence is not None and other.confidence is not None:
            # comparing evaluation file data - both have a confidences score:
            return self.__cmp_confidence(other)
        else:
            # otherwise, comparing evaluation file data to gold standard data
            return cmp(self.item, other.item) * self._ordering
    
    def __len__(self):
        "Helper for calling len() directly on ResultContainers."
        return 1
    
    def __str__(self):
        "Presentation logic for any result container."
        rank = "" if self.rank is None else "\t%i" % self.rank
        conf = "" if self.confidence is None else "\t%f" % self.confidence
        return "%s%s%s" % (self.__str_item(), rank, conf)
    
    def __repr__(self):
        "Representation string for any result container."
        return "<%s '%s'>" % (
            self.__class__.__name__, str(self).replace('\t', ' ')
        )
    
    def __str_item(self):
        "Return tuples as a tab-separated item, everything else via str()."
        if isinstance(self.item, tuple):
            return "%s\t%s" % self.item
        else:
            return str(self.item)
    
    def __first_if_true(self):
        "Ordering of distinct boolean (article classification) values."
        if self.item is True:
            return -1 # True goes before False
        else:
            return 1 # False goes after True
    
    def __cmp_rank(self, other):
        "Ordering by rank, including special ACT logic."
        if self.rank == other.rank:
            raise RuntimeError("duplicate ranks: '%s' vs. '%s'" % (
                str(self), str(other)
            ))
            # unsafe version:
            # self.logger.warn("duplicate ranks: '%s' vs. '%s'" % (
            #     str(self), str(other)
            # ))
            # return cmp(self.item, other.item) * self._ordering
        
        # compare ranks on boolean False results inversely; regular int comp.
        return cmp(self.rank, other.rank) * self._ordering
    
    def __cmp_confidence(self, other):
        "Ordering by confidence, including special ACT logic."
        order = cmp(self.confidence, other.confidence) * self._ordering * -1
        
        if order == 0:
            # if the confidence is equal, try to sort by the result value
            # do not use the special ordering parameter here to ensure result
            # are always ordered alphanumerically in this case
            order = cmp(self.item, other.item)
        
        return order
    
