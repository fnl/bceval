import logging

import biocreative.evaluation.container.results as results

class AbstractDataDict(dict):
    """Base data container.
    
    Stores the results to a dictionary where the keys are the DOI and the
    values are a single result container (ACT) or a list of them (INT, IPT).
    """
    
    def __init__(self, *args, **kwds):
        super(AbstractDataDict, self).__init__(*args, **kwds)
        self.logger = logging.getLogger('BaseDataDict')
    
    def __iter__(self):
        return iter(self.keys())
    
    def assert_duplicates(self, doi, result):
        """Make sure no duplicate data is added to the dictionary.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def add_result(self, doi, result_container):
        """Add the result for that DOI as required by the data.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def sort_results(self):
        """Sort the results in the dictionary as required by the data.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def true_items(self):
        """Return the max. number of true items for this collection.
        
        Especially used to set the FN counters for AUC iP/R evaluation.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def keys(self):
        "Return the sorted keys of the dictionary."
        dois = super(AbstractDataDict, self).keys()
        dois.sort()
        return dois
    
    def load_from(self, data_iterator, gold_standard=None):
        """Load the data dictionary from a given iterator, skipping any DOIs
        in the GS if it is given and those DOIs are not found.
        """
        self.ignored = (
            set() if gold_standard and len(gold_standard) else None
        )
        
        for doi, result, rank, confidence in data_iterator:
            if self.ignored is not None and self._ignore(doi, gold_standard):
                continue
            
            self.assert_duplicates(doi, result)
            result_container = results.ResultContainer(
                result, rank=rank, confidence=confidence
            )
            self.add_result(doi, result_container)
        
        self.sort_results()
        
        if self.ignored is not None and len(self.ignored):
            self.logger.info("ignored %i documents not in GS" % len(
                self.ignored
            ))
        
        logging.info("loaded %i annotations" % 
            sum(len(i) for i in self.values())
        )
    
    def add_entries_only_in(self, other, Value_Type=list):
        """Add empty entries to this dictionary if the other has it.
        
        Value_Type is the data type value that will be added.
        """
        cases = 0
        for doi in other.keys():
            if doi not in self:
                cases += 1
                self[doi] = Value_Type()
        
        if cases > 0:
            self.logger.info("added %i documents to %s" % (
                cases, self.__class__.__name__
            ))
        
        return cases
    
    def delete_entries_not_in(self, other):
        "Delete entries in this dictionary if the other does not have it."
        cases = 0
        for doi in self.keys():
            if doi not in other:
                cases += 1
                del self[doi]
        
        if cases > 0:
            self.logger.info("removed %i documents from %s" % (
                cases, self.__class__.__name__
            ))
        
        return cases
    
    def prune_empty_sets(self):
        "Remove entries that have no results attached to it."
        cases = 0
        
        for doi, results in self.items():
            if len(results) == 0:
                del self[doi]
                cases += 1
        
        if cases > 0:
            self.logger.info("pruned %i empty documents from %s" % (
                cases, self.__class__.__name__
            ))
        
        return cases
    
    def _ignore(self, doi, other_dict):
        """Ignore the DOI if it is not found in the other dictionary and
        record the DOI in self.ignored.
        
        The ignored instance var must be initialized before calling this
        method as a set.
        
        Returns True if ignored was initialized and the DOI isn't a key in
        the other dictionary, False otherwise.
        """
        if doi in self.ignored:
            return True
        elif doi not in other_dict:
            self.ignored.add(doi)
            return True
        else:
            return False
    
