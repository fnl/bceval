import logging

from collections import defaultdict

from biocreative.evaluation.container.protein_dict import ProteinDataDict
from biocreative.evaluation.container.results import ResultContainer

class AbstractProteinDataDict(ProteinDataDict):
    """Data container for INT and IPT data; Common homonym ortholog mapping
    and organism filtering functions to both data types.
    """
    
    def __init__(self, *args, **kwds):
        super(AbstractProteinDataDict, self).__init__(*args, **kwds)
        self.logger = logging.getLogger('AbstractProteinDataDict')
    
    def extract_accessions_for(self, doi):
        """Accession/identifier extraction for INT/IPT result data.
        
        Abstract method.
        """
        raise NotImplementedError("abstract")
    
    # ============================
    # = Homonym Ortholog Mapping =
    # ============================
    
    def map_homonym_orthologs(self, homonym_ortholog_map, gold_standard):
        "Map/replace results that are homonymous orthologs of GS annotations."
        self._mapping_setup(homonym_ortholog_map)
        
        for doi, gs_annotations in gold_standard.items():
            if doi not in self or len(self[doi]) == 0:
                self.logger.debug(
                    "skipping DOI '%s' not in results (or len 0)" % doi
                )
                continue # no need to map empty/nonexistent results...
            
            self.logger.debug("homonym ortholog mapping for DOI '%s'" % doi)
            self._ho_gs_lists = defaultdict(list)
            self._result_accessions = self.extract_accessions_for(doi)
            self._gs_items = [rc.item for rc in gs_annotations]
            
            for gs_container in gs_annotations:
                gs_item = gs_container.item
                self._add_ho_gs_mappings_for(gs_item)
            
            self[doi] = self._map(doi)
        
        self._mapping_logging_and_assertions()
    
    def _mapping_setup(self, ho_map):
        "Initialize all instance variables for the HO mapping operation."
        self.logger.info("mapping homonym ortholog pairs")
        self._ho_map = ho_map
        self._mapped_results = 0
        self._added_results = 0
        self._filtered_results = 0
        self._ho_gs_lists = None
        self._result_accessions = None
        self._gs_items = None
        self._result_container = None
        self._replaced_an_entry = False
        self._old_results_size = sum(len(rcl) for rcl in self.values())
    
    def _add_ho_gs_mappings_for(self, gs_item):
        """Find homonym ortholog mapping for this GS item.
        
        Adds homonym ortholog and gold standard items to the current
        HO GS dictionary list if there is a known mapping for the gold
        standard item, but only adds HO items if their accessions are also
        found in the results.
        """
        if self._item_in_ho_map(gs_item):
            self.logger.debug("searching HO for GS item %s" % str(gs_item))
            for ho_item in self._item_iterator(gs_item):
                if ho_item not in self._gs_items:
                    self.logger.debug(
                        "-> mapping to %s possible" % str(ho_item)
                    )
                    self._ho_gs_lists[ho_item].append(gs_item)
    
    def _item_in_ho_map(self, gs_item):
        """Return True if any accession is in the HO map.
        
        Abstract method.
        """
        raise NotImplementedError("abstract")
    
    def _item_iterator(self, gs_item):
        """Return HO items for this GS item.
        
        Abstract method.
        """
        raise NotImplementedError("abstract")
    
    def _map(self, doi):
        """Map/replace HO results with GS items and remove any duplicate
        results generated in the process.
        """
        self._replaced_an_entry = False
        new_results = list(self[doi])
        old_results = list(new_results)
        old_results.reverse()
        map(self._map_replace(new_results), enumerate(old_results))
        
        if self._replaced_an_entry:
            new_results = self._remove_duplicates(new_results)
            self._rerank_results(new_results)
        
        return new_results
    
    def _map_replace(self, new_results):
        "Map between the new and old result list and replace HO matches."
        len_r = len(new_results)
        
        def mapper(indexed_result_container):
            "Mapping function."
            self._result_container = indexed_result_container[1]
            pos = len_r - indexed_result_container[0] - 1
            
            if new_results[pos].item != self._result_container.item:
                raise IndexError("in homonym ortholog mapping algorithm")
            
            if self._result_container.item in self._ho_gs_lists:
                self._replace(new_results, pos)
        
        return mapper

    def _replace(self, new_results, pos):
        "Replace the result item with the HO mapped GS result."
        self._replaced_an_entry = True
        result_item = self._result_container.item
        gs_items = self._ho_gs_lists[result_item]
        
        if len(gs_items) > 1:
            self._replace_multiple(new_results, gs_items, pos)
        else:
            self.logger.debug("=! mapping %s to GS item %s" % (
                str(new_results[pos].item), str(gs_items[0])
            ))
            new_results[pos].item = gs_items[0]
            self._mapped_results += 1
    
    def _replace_multiple(self, new_results, gs_items, pos):
        "Add all possible HO mappings of GS items for this result item."
        conf = self._result_container.confidence
        rank = self._result_container.rank
        
        for item in gs_items:
            self.logger.debug("=! mapping %s to GS item %s" % (
                str(new_results[pos].item), str(item)
            ))
            new_results.insert(
                pos + 1, ResultContainer(item, rank, conf)
            )
            self._added_results += 1
        
        del new_results[pos]
        self._filtered_results += 1
    
    def _remove_duplicates(self, result_containers):
        """Remove eventual duplicates added to the results in the mapping
        process.
        """
        new_result_containers = list(result_containers)
        original_items = [rc.item for rc in result_containers]
        pos = len(original_items)
        
        while pos > 0:
            pos -= 1
            item = original_items.pop()
            
            if item in original_items:
                self.logger.debug("=! filtering duplicate item %s" % (
                    str(new_result_containers[pos].item)
                ))
                del new_result_containers[pos]
                self._filtered_results += 1
        
        return new_result_containers
    
    def _rerank_results(self, result_containers):
        "Assign ascending ranks to the results."
        for idx, rc in enumerate(result_containers):
            rc.rank = idx + 1
    
    def _mapping_logging_and_assertions(self):
        "Log the outcome of the mapping and assert the data is valid."
        self.logger.debug(
            "mapped %i, added %i - filtered %i = %i total result change" % (
                self._mapped_results, self._added_results,
                self._filtered_results,
                self._added_results - self._filtered_results
            )
        )
        change = self._added_results - self._filtered_results
        new_results_size = sum(len(rcl) for rcl in self.values())
        self.logger.info("%i results after mapping" % (
            sum(len(rcl) for rcl in self.values())
        ))
        assert new_results_size - change == self._old_results_size, \
            "result size changes do not match control"
    
    def _hos_in_results(self, gs_accession):
        """Return all HO accessions that are also found in the results
        for the given GS accession.
        """
        return filter(
            lambda acc: acc in self._result_accessions,
            self._ho_map[gs_accession]
        )
    
    # ======================
    # = Organism Filtering =
    # ======================
    
    def filter_organisms(self, organism_map, gold_standard):
        "Filter wrong organisms from the results according to the GS."
        self.logger.info("organism filtering")
        self._org_map = organism_map
        self._filtered = 0
        self._gold_standard = gold_standard
        
        for doi, gs_container in gold_standard.items():
            self[doi] = self._filter_organisms(doi, gs_container)
        
        self.logger.info("%i results were filtered" % self._filtered)
    
    def _filter_organisms(self, doi, gs_container):
        """Filter results where the source organisms of the accessions does
        not match the source organism of the gold standard accessions.
        """
        if doi not in self or len(self[doi]) == 0:
            return list() # no need to filter empty/non-existent results...
        
        gs_taxa = self._get_gs_taxa_for(doi)
        from_old_results = self[doi]
        new_results = filter(
            self._organisms_only_in(gs_taxa), from_old_results
        )
        self._filtered += (len(from_old_results) - len(new_results))
        return new_results
    
    def _get_gs_taxa_for(self, doi):
        "Return the set of taxa IDs according to the GS for the given DOI."
        gs_accessions = self._gold_standard.extract_accessions_for(doi)
        
        try:
            return set([self._org_map[acc] for acc in gs_accessions])
        except KeyError, e:
            raise RuntimeError(
                "Missing GS accession in organism map: %s" % str(e)
            )
    
    def _organisms_only_in(self, gs_taxa):
        """Return a filter function that returns True only if the accessions
        in the ResultContainer sent to the function matches organism IDs in
        the gold standard annotations.
        
        Abstract method.
        """
        raise NotImplementedError("abstract")
    
