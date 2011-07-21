import logging

from biocreative.evaluation.map_filter.protein_dict \
    import AbstractProteinDataDict

class IPTDataDict(AbstractProteinDataDict):
    """Homonyn ortholog mapping and organism filtering functionality for
    IPT data.
    """
    
    def __init__(self, *args, **kwds):
        super(IPTDataDict, self).__init__(*args, **kwds)
        self.logger = logging.getLogger('IPTDataDict')
    
    def extract_accessions_for(self, doi):
        "Accession/identifier extraction for IPT data."
        accessions = set(self._extract_accessions_for_partner(doi, 0))
        accessions.update(self._extract_accessions_for_partner(doi, 1))
        return accessions
    
    def _extract_accessions_for_partner(self, doi, pos):
        "Accession/identifier extraction helper for IPT data."
        return [rc.item[pos] for rc in self[doi]]
    
    # ============================
    # = homonym ortholog mapping =
    # ============================
    
    def _item_in_ho_map(self, gs_pair):
        "Return True if at least one accession is in the HO map."
        return any(map(self._ho_map.has_key, gs_pair))
    
    def _item_iterator(self, gs_pair):
        "Return HO pairs for the GS pair that are also found in the results."
        acc_lists = self._ho_lists_for_both_gs_accessions(gs_pair)
        
        for acc1 in acc_lists[0]:
            for ho_pair in [[acc1, acc2] for acc2 in acc_lists[1]]:
                ho_pair.sort()
                yield tuple(ho_pair)
    
    def _ho_lists_for_both_gs_accessions(self, gs_pair):
        """Return the list of HO accessions for both accessions in the GS
        pair, filtering any accessions that are not also found in the
        results.
        """
        acc_lists = ([], [])
                
        for pos in range(2):
            # report only relevant mappings that can be made (i.e.,
            # return accessions that are actually part of the results,
            # reducing the size of pairs we need to check to the possibly
            # relevant ones only)
            if gs_pair[pos] in self._ho_map:
                acc_lists[pos].extend(self._hos_in_results(gs_pair[pos]))
            
            if gs_pair[pos] in self._result_accessions:
                acc_lists[pos].append(gs_pair[pos])
        
        return acc_lists
    
    # ======================
    # = organism filtering =
    # ======================
    
    def _organisms_only_in(self, gs_taxa):
        """Organism filtering specifics for INT data.
        
        Return a filter function that returns True only if both accessions
        in the ResultContainer sent to the function match an organism ID in
        the gold standard annotations.
        """
        
        def both_accessions_map_to_gs_taxa(result_container):
            "Filter function."
            acc_a = result_container.item[0]
            acc_b = result_container.item[1]
            
            try:
                return (
                    self._org_map[acc_a] in gs_taxa and
                    self._org_map[acc_b] in gs_taxa
                )
            except KeyError:
                self.logger.debug("unknown accession %s or %s" % (
                    acc_a, acc_b
                ))
                return False
        
        return both_accessions_map_to_gs_taxa
    
