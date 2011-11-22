import unittest

from mock import Mock, patch_object

from biocreative.evaluation.controller.abstract import AbstractEvaluator

class AbstractEvaluatorTest(unittest.TestCase):
    
    @patch_object(AbstractEvaluator, 'reset')
    def setUp(self, reset_mock):
        self.eval = AbstractEvaluator(0)
        self.reset_mock = reset_mock
        self.logger_mock = self.eval.logger = Mock()
    
    def test_init_state(self):
        self.assertEqual(self.eval.cutoff, 0)
        self.assertEqual(self.eval.primary_eval, None)
        self.assertEqual(self.eval.secondary_eval, None)
        self.assertEqual(self.eval.results, None)
        self.assertEqual(self.eval.gold_standard, None)
        self.assertEqual(type(self.eval.logger), Mock)
        self.assertEqual(self.reset_mock.call_count, 1)
        self.assertEqual(self.reset_mock.call_args, ((), {}))
    
    @patch_object(AbstractEvaluator, '_prepare')
    @patch_object(AbstractEvaluator, '_process')
    def test_process(self, process_mock, prepare_mock):
        gold_standard = {1: 'a'}
        results = {1: 'a', 2: 'b'}
        primary, secondary = self.eval.process(results, gold_standard)
        self.assert_called_once_with(prepare_mock, results, gold_standard)
        self.assert_called_once_with(
            self.logger_mock.info, "processing results with cutoff=0"
        )
        self.assert_called_once_with(process_mock)
    
    def assert_called_once_with(self, mock, *args, **kwds):
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(mock.call_args, (args, kwds))
    

if __name__ == '__main__':
    unittest.main()
