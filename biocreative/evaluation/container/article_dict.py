import logging

from biocreative.evaluation.container.data_dict import AbstractDataDict

class ArticleDataDict(AbstractDataDict):
    """Data container for ACT data.
    
    Loads the data using the ACTReader and ensures the keys are produced in
    the correct order when used in an iterator or via keys().
    """
    
    def __init__(self, *args, **kwds):
        super(ArticleDataDict, self).__init__(*args, **kwds)
        self.order = list()
        self.logger = logging.getLogger('ArticleDataDict')
    
    def __iter__(self):
        self.__pos = 0
        self.__len = len(self.order)
        return self
    
    def next(self):
        """Specialized method using rank/confidence/file ordering to
        iterate result containers.
        """
        if self.__pos < self.__len:
            self.__pos += 1
            return self.order[self.__pos - 1]
        
        raise StopIteration
    
    def keys(self):
        """Returns the rank/confidence/file-ordered keys, overriding the
        abstract definition.
        """
        return list(self.order)
    
    def assert_duplicates(self, doi, unused):
        "Assert no duplicate ACT result is read."
        assert doi not in self, "duplicate DOI %s" % doi
    
    def add_result(self, doi, result_container):
        "Add a given ResultContainer for a doi to the dictionary."
        self.order.append(doi)
        self[doi] = result_container
    
    def sort_results(self):
        "Sort the ACT results using the sorting logic of ResultContainers."
        result_doi = [(r, d) for d, r in self.items()]
        result_doi.sort()
        # store the final order in the order attr:
        self.order = [d for r, d in result_doi]
    
    def true_items(self):
        "Return the number of items in the collection annotated with True."
        return sum(1 for rc in self.values() if rc.item is True)
