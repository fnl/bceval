import unittest

class EvaluationTests(unittest.TestCase):
    
    def setUp(self):
        self.fixture_path = config.fixture_path_for('evaluation')
    
    def test_int_evaluation(self):
        gs_file = self.fixture_file('%s_gold_standard.tsv' % Evaluate.INT)
        results_file = self.fixture_file('%s_results.tsv' % Evaluate.INT)
        GSReader = config.load_gs_reader(Evaluate.INT)
        ResultsReader = config.load_results_reader(Evaluate.INT)
        gs_reader = GSReader()
        results_reader = ResultsReader()
        gs_reader.load_from_file(gs_file)
        results_reader.load_from_file(results_file)
        