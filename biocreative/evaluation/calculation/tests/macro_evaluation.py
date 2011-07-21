import unittest

from math import sqrt
from mock import Mock, patch
from random import random, randint

from biocreative.evaluation.calculation.protein import ProteinEvaluation
from biocreative.evaluation.calculation.macro_evaluation import ProteinMacroEvaluation
from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions

class ProteinMacroEvaluationTest(CalculationAssertions):
    
    def setUp(self):
        RandomProteinEvaluation = \
            ProteinMacroEvaluationTest.init_random_protein_evaluation_mock
        self.random_mocks = [RandomProteinEvaluation() for i in range(10)]
        self.evaluator = ProteinMacroEvaluation(self.random_mocks)
    
    @staticmethod
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def init_random_protein_evaluation_mock(unused):
        mock = Mock(wraps=ProteinEvaluation())
        
        for prop in C.PROTEIN_PROPERTIES:
            setattr(mock, prop, random())
        
        for attr in C.HITS_ATTRIBUTES:
            setattr(mock.hits, attr, randint(0, 1000))
        
        return mock
    
    def test_std_dev(self):
        for prop in C.PROTEIN_PROPERTIES:
            expected = ProteinMacroEvaluationTest.calculate_std_dev(
                [getattr(m, prop) for m in self.random_mocks]
            )
            received = self.evaluator.std_dev(prop)
            self.assert_values(prop, expected, received)
    
    def test_properties_except_hits(self):
        for prop in C.PROTEIN_PROPERTIES:
            expected = self.get_average_for(prop)
            self.assert_property(prop, expected)
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def test_hits(self, unused):
        expected = dict()
        
        for attr in C.HITS_ATTRIBUTES:
            expected[attr] = sum(
                getattr(mock.hits, attr) for mock in self.random_mocks
            )
        
        received = self.evaluator.hits
        
        for attr in C.HITS_ATTRIBUTES:
            self.assertEqual(
                getattr(received, attr), expected[attr],
                "%s hits don't match (received: %i, expected: %i)" % (
                    attr, getattr(received, attr), expected[attr]
                )
            )
    
    def test_average_for(self):
        expected = self.get_average_for('precision')
        received = self.evaluator._average_for('precision')
        self.assert_values('average_for', expected, received)
    
    def test_static_calculations(self):
        for kind in ('variation', 'variance', 'std_dev'):
            self.run_static_calc_test_for(kind)
    
    def run_static_calc_test_for(self, name):
        rnd_floats = [random() for i in range(10)]
        expected_fun = eval('ProteinMacroEvaluationTest.calculate_%s' % name)
        test_fun = eval('ProteinMacroEvaluation._%s' % name)
        expected = expected_fun(rnd_floats)
        received = test_fun(rnd_floats)
        self.assert_values(name, expected, received)
    
    def get_average_for(self, prop):
        return ProteinMacroEvaluationTest.calculate_average(
            [getattr(m, prop) for m in self.random_mocks]
        )
    
    @staticmethod
    def calculate_average(numbers):
        total = sum(numbers)
        return float(total) / len(numbers)
    
    @staticmethod
    def calculate_variation(numbers):
        average = ProteinMacroEvaluationTest.calculate_average(numbers)
        return sum((i - average)**2 for i in numbers)
    
    @staticmethod
    def calculate_variance(numbers):
        variation = ProteinMacroEvaluationTest.calculate_variation(numbers)
        return variation / float(len(numbers))
    
    @staticmethod
    def calculate_std_dev(numbers):
        variance = ProteinMacroEvaluationTest.calculate_variance(numbers)
        return sqrt(variance)
    

if __name__ == '__main__':
    unittest.main()