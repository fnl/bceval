import logging

from biocreative.evaluation.map_filter.protein_dict \
    import AbstractProteinDataDict

class INTDataDict(AbstractProteinDataDict):
    """Homonyn ortholog mapping and organism filtering functionality for
    INT data.
    """
    
    def __init__(self, *args, **kwds):
        super(INTDataDict, self).__init__(*args, **kwds)
        self.logger = logging.getLogger('INTDataDict')
    
    def extract_accessions_for(self, doi):
        """Accession/identifier extraction for INT data."""
        return [rc.item for rc in self[doi]]
    
    # ============================
    # = homonym ortholog mapping =
    # ============================
    
    def _item_in_ho_map(self, gs_accession):
        "Return True if the accession is in the HO map."
        return self._ho_map.has_key(gs_accession)
    
    def _item_iterator(self, gs_accession):
        "see AbstractProteinDataDict._hos_in_results"
        return self._hos_in_results(gs_accession)
    
    # ======================
    # = organism filtering =
    # ======================
    
    def _organisms_only_in(self, gs_taxa):
        """Organism filtering specifics for INT data.
        
        Return a filter function that returns True only if the accession
        in the ResultContainer sent to the function matches an organism ID in
        the gold standard annotations.
        """
        
        def accession_maps_to_a_gs_taxon(result_container):
            "Filter function."
            accession = result_container.item
            
            try:
                return self._org_map[accession] in gs_taxa
            except KeyError:
                self.logger.info("unknown accession %s" % accession)
                return False
        
        return accession_maps_to_a_gs_taxon
    
