# encoding: utf-8

from biocreative.evaluation.container import container_factory
from biocreative.evaluation.controller import controller_factory
from biocreative.evaluation.map_filter import map_filter_factory

class Manager(object):
    """Needs an initial set up after which a Manager instance can run
    evaluations on any given result iterator object with a given set of
    parameters (provided by the parameters.Parameters class).
    """
    
    def __init__(self, evaluation_type):
        """Initial setup only requires the evaluation type (ACT, INT, IPT) is
        set; the gold standard is initialized (but empty!), and the homonym
        ortholog and protein organism mapping are declared but initialized
        to None (i.e., no HOF is done by default).
        """
        self.evaluation_type = evaluation_type
        self.GS_Container = container_factory(evaluation_type)
        self.gold_standard = self.GS_Container()
        self.Result_Container = container_factory(evaluation_type)
        self.ho_map = None
        self.po_map = None
    
    def load_gold_standard(self, gs_iterator):
        "Load the gold standard from the given data iterator."
        self.gold_standard.load_from(gs_iterator)
    
    def do_homonym_ortholog_mapping(self, mapping_dict):
        """Set the mapping dictionary for homonym orthologs, making use of
        it in subsequent calls to evaluate().
        """
        self.ho_map = mapping_dict
        self._set_hof_containers()
    
    def do_organism_filtering(self, mapping_dict):
        """Set the mapping dictionary for organism filtering, making use of
        it in subsequent calls to evaluate().
        """
        self.po_map = mapping_dict
        self._set_hof_containers()
    
    def _set_hof_containers(self):
        self.GS_Container = map_filter_factory(self.evaluation_type)
        self.Result_Container = map_filter_factory(self.evaluation_type)
    
    def evaluate(self, result_iterator, params, debug=False):
        """Evaluate a result set given a data iterator for it using the
        params object (parameters.Parameters).
        
        Returns a tupe consisting of the primary and secondary evaluation
        result calculations (biocreative.evaluation.calculation classes).
        
        If debug is True, this method stops before doing the actual
        evaluation and returns the GS and results container after HOF
        instead of the primary and secondary evaluation results.
        """
        # make a copy of the gold standard, as we might delete some of the
        # annotations it has (related to the skip parameter, see below);
        # also needed because we actually have the GS in a regular container
        # always, while we might be doing HOF mapping & filtering
        gold_standard = self.GS_Container(self.gold_standard)
        
        results = self.Result_Container()
        results.load_from(result_iterator, gold_standard=gold_standard)
        
        if self.ho_map is not None:
            results.map_homonym_orthologs(self.ho_map, gold_standard)
        
        if self.po_map is not None:
            results.filter_organisms(self.po_map, gold_standard)
        
        # remove any DOIs in results that might no longer have annotations
        # because of the mapping or filtering step
        results.prune_empty_sets()
        
        # remove DOIs from GS (skip) or add them to results (do not skip)
        if params.skip_empty_results:
            # here we might be altering the gold standard (copied before)
            gold_standard.delete_entries_not_in(results)
        else:
            results.add_entries_only_in(gold_standard)
        
        if debug:
            return gold_standard, results
        
        controller = controller_factory(self.evaluation_type)(params.cutoff)
        
        # ===============================================
        # ==== The actual evaluation continues here. ====
        return controller.process(results, gold_standard)
        # ===============================================
    

        