import unittest

from mock import Mock, patch

from biocreative.evaluation.calculation.hits import Hits
from biocreative.evaluation.container.article_dict import ArticleDataDict
from biocreative.evaluation.container.results import ResultContainer
from biocreative.evaluation.controller.article import ArticleEvaluator

class ArticleEvaluatorTest(unittest.TestCase):
    
    calcpath = 'biocreative.evaluation.calculation.'
    
    @patch(calcpath + 'article_auc_pr.ArticleAucPrEvaluation', spec=True)
    @patch(calcpath + 'article_mcc.ArticleMccEvaluation', spec=True)
    def setUp(self, avrg_p_mock, mcc_mock):
        self.eval = ArticleEvaluator(0)
        self.avrg_p_mock = avrg_p_mock
        avrg_p_mock.hits = Mock(spec=Hits)
        self.mcc_mock = mcc_mock
        mcc_mock.hits = Mock(spec=Hits)
        self.logger_mock = self.eval.logger = Mock()
    
    def test_init_state(self):
        self.assertEqual(self.avrg_p_mock.call_count, 1)
        self.assertEqual(self.mcc_mock.call_count, 1)
        self.assertEqual(type(self.eval.primary_eval), Mock)
        self.assertEqual(type(self.eval.secondary_eval), Mock)
        self.assertEqual(self.eval.gold_standard, None)
        self.assertEqual(self.eval.results, None)
        self.assertEqual(type(self.eval.logger), Mock)
    
    def test_reset(self):
        pass # tested by init state already
    
    def test_prepare(self):
        # SETUP
        gs_mock = Mock(spec=ArticleDataDict)
        gs_mock.true_items.return_value = 10
        self.eval.gold_standard = gs_mock
        self.eval.primary_eval.hits = Mock(spec=Hits)
        self.eval.secondary_eval.hits = Mock(spec=Hits)
        # RUN TEST
        self.eval._prepare({}, gs_mock)
        # ASSERT
        self.assert_called_once_with(gs_mock.true_items)
        self.assertEqual(self.eval.primary_eval.hits.fn, 10)
        self.assertEqual(self.eval.secondary_eval.hits.fn, 0)
        self.assert_called_once_with(
            self.logger_mock.info, "ACT evaluation fn=10"
        )
    
    def test_process_doi(self):
        rc = Mock(spec=ResultContainer)
        rc.item = 'a'
        self.eval.gold_standard = {1: rc}
        self.eval.results = {1: rc}
        self.eval._process_doi(1)
        
        for mock in (self.eval.primary_eval, self.eval.secondary_eval):
            self.assert_called_once_with(mock.evaluate, 'a', 'a', 0)
    
    def assert_called_once_with(self, mock, *args, **kwds):
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(mock.call_args, (args, kwds))
    

if __name__ == '__main__':
    unittest.main()
