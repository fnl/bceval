import unittest

from mock import Mock, patch

from biocreative.evaluation.calculation.hits \
    import Hits
from biocreative.evaluation.calculation.macro_evaluation \
    import ProteinMacroEvaluation
from biocreative.evaluation.calculation.protein \
    import ProteinEvaluation
from biocreative.evaluation.container.protein_dict \
    import ProteinDataDict
from biocreative.evaluation.controller.protein \
    import ProteinEvaluator

class ProteinEvaluatorTest(unittest.TestCase):
    
    def setUp(self):
        self.eval = ProteinEvaluator(0)
        self.logger_mock = self.eval.logger = Mock()
    
    def test_init_state(self):
        self.assertEqual(self.eval.gold_standard, None)
        self.assertEqual(self.eval.results, None)
        self.assertEqual(type(self.eval.logger), Mock)
    
    def test_reset(self):
        pass # tested by init state already
    
    @patch('__builtin__.len')
    def test_prepare(self, len_mock):
        # SETUP
        self.eval.primary_eval = Mock(spec=ProteinEvaluation)
        self.eval.primary_eval.hits = Mock(spec=Hits)
        self.eval.primary_eval.hits.fn = 15
        gs_mock = Mock(spec=ProteinDataDict)
        results_mock = Mock(spec=ProteinDataDict)
        # use distinct return value to make sure things are set up right:
        gs_mock.true_items.return_value = 10
        self.eval._process_micro_scores = Mock()
        len_mock.return_value = 5 # again to make sure all as expected
        # RUN THE TEST
        self.eval._prepare(results_mock, gs_mock)
        # ASSERT RESULTS
        self.assertEqual(len_mock.call_count, 2)
        self.assertEqual(
            len_mock.call_args_list,
            [ ( (results_mock,), {} ), ( (gs_mock,), {} ) ]
        )
        self.assert_called_once_with(gs_mock.true_items)
        self.assert_called_once_with(self.eval.primary_eval.set_fn, 10)
        self.assert_called_once_with(
            self.logger_mock.debug, "INT/IPT evaluation: 15 GS annotations"
        )
        self.assert_called_once_with(self.eval._process_micro_scores)
    
    def test_prepare_raises_error(self):
        results = {1: None, 2: None}
        gold_standard = {1: None}
        self.assertRaises(
            AssertionError, self.eval._prepare, results, gold_standard
        )
    
    def test_process_doi(self):
        self.eval.gold_standard = {1: [1,2,3]}
        self.eval.results = {1: [1]}
        self.assertEqual(len(self.eval.secondary_eval), 0)
        self.eval._process_doi(1)
        protein_eval = self.eval.secondary_eval[0]
        self.assertEqual(type(protein_eval), ProteinEvaluation)
        self.assertEqual(protein_eval.doi, 1)
        self.assertEqual(protein_eval.hits.tp, 1)
        self.assertEqual(protein_eval.hits.fp, 0)
        self.assertEqual(protein_eval.hits.fn, 2)
    
    def test_process_micro_scores(self):
        # SETUP
        self.eval.results = {'a': [4,5,6], 'b': [4,5,6], 'c': [4,5,6]}
        self.eval.cutoff = 2
        self.eval._process_micro_doi = Mock()
        self.eval.primary_eval.store_p_at_current_r = Mock()
        # RUN THE TEST
        self.eval._process_micro_scores()
        # ASSERT RESULTS
        self.assertEqual(self.eval._dois, ['a', 'b', 'c'])
        self.assertEqual(self.eval._process_micro_doi.call_count, 6)
        result_list = []
        
        for r in (0, 1):
            for doi in self.eval._dois:
                result_list.append(((doi, r), {}))
        
        self.assertEqual(
            self.eval._process_micro_doi.call_args_list, result_list
        )
        self.assertEqual(
            self.eval.primary_eval.store_p_at_current_r.call_count, 2
        )
    
    def test_process_micro_doi(self):
        self.eval.primary_eval.evaluate_item = Mock()
        self.eval.results = {1: [1,2,3]}
        self.eval.gold_standard = {1: [1,]}
        self.eval._process_micro_doi(1, 1)
        self.assert_called_once_with(
            self.eval.primary_eval.evaluate_item, 2, [1,]
        )
    
    def test_process_micro_doi_with_index_error(self):
        self.eval.results = {1: [1,2,3]}
        self.eval.gold_standard = {1: [1,]}
        self.eval._dois = [1]
        self.eval._process_micro_doi(1, 3)
        self.assertEqual(len(self.eval._dois), 0)
    
    @patch('__builtin__.len')
    def test_processing_of_micro_scores(self, len_mock):
        # SETUP
        results = {'a': [1,2,3], 'b': [1,2], 'c': [3,4,5]}
        self.eval.results = results
        gold_standard = Mock()
        gold_standard.true_items.return_value = 3
        gold_standard.get.return_value = [3]
        self.eval.gold_standard = gold_standard
        self.eval.primary_eval = Mock(spec=ProteinEvaluation)
        self.eval.primary_eval.hits = Mock(spec=Hits)
        self.eval.primary_eval.hits.fn = 3
        len_mock.return_value = 3
        # RUN THE TEST
        self.eval._prepare(results, gold_standard)
        # ASSERT RESULTS
        # just make sure everything got called as often as this setup
        # would suggest; details are ensured in the tests before
        self.assertEqual(len_mock.call_count, 6)
        self.assertEqual(self.eval.primary_eval.set_fn.call_count, 1)
        self.assertEqual(
            self.eval.primary_eval.store_p_at_current_r.call_count, 3
        )
        self.assertEqual(gold_standard.get.call_count, 9)
        self.assertEqual(
            self.eval.primary_eval.evaluate_item.call_count, 8
        )
        self.assertEqual(self.eval._dois, ['a', 'c'])
    
    def assert_called_once_with(self, mock, *args, **kwds):
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(mock.call_args, (args, kwds))
    

if __name__ == '__main__':
    unittest.main()