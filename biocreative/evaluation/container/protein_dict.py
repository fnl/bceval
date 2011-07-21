import logging

from biocreative.evaluation.container.data_dict import AbstractDataDict

class ProteinDataDict(AbstractDataDict):
    """Data container for INT and IPT data; Common homonym ortholog mapping
    and organism filtering functions to both data types.
    """
    
    def __init__(self, *args, **kwds):
        super(ProteinDataDict, self).__init__(*args, **kwds)
        self.logger = logging.getLogger('ProteinDataDict')
    
    def assert_duplicates(self, doi, result):
        """Assert no duplicate result is read and create the key with an
        empty list value if the DOI hasn't been added so far.
        """
        if doi in self:
            others = tuple(rc.item for rc in self[doi])
            assert result not in others, \
                "duplicate result '%s' for DOI %s" % (
                    str(result), doi
                )
        else:
            self[doi] = list()
    
    def add_result(self, doi, result_container):
        "Add a given ResultContainer for a doi to the dictionary's list."
        self[doi].append(result_container)
    
    def sort_results(self):
        "Sort the results using rank or confidence."
        for doi in self:
            r_list = self[doi]
            r_list.sort() # sort in place
    
    def true_items(self):
        "Return the number of items in the collection annotated."
        return sum(len(result_list) for result_list in self.values())