import unittest

class Constants(object):
    HITS_ATTRIBUTES = ('tp', 'fp', 'fn', 'tn')
    PROTEIN_PROPERTIES = ('recall', 'precision', 'f_score', 'avrg_p')
    article_auc_prOPERTIES = (
        'accuracy', 'mcc_score', 'sensitivity', 'specificity'
    )

class CalculationAssertions(unittest.TestCase):
    
    def assert_values(self, name, expected, received):
        self.assertEqual(
            expected, received,
            "%s mismatch (expected: %s, received: %s)" % (
                name, str(expected), str(received)
            )
        )
    
    def assert_hits(self, hits, **expected):
        for attr, value in expected.items():
            self.assert_values(
                "%s hits" % attr, value, getattr(hits, attr)
            )
    
    def assert_counter(self, hits, **expected):
        for prop, value in expected.items():
            real = getattr(hits, "_%s" % prop)
            self.assert_values(
                "%s internal hits count" % prop, value, real
            )
    
    def assert_property(self, prop, expected):
        received = getattr(self.evaluator, prop)
        self.assert_values(prop, expected, received)
    
if __name__ == '__main__':
    from biocreative.evaluation.calculation.evaluation \
        import AbstractEvaluationTest
    from biocreative.evaluation.calculation.article_auc_pr \
        import ArticleAucPrEvaluationTest
    from biocreative.evaluation.calculation.article_mcc \
        import ArticleMccEvaluationTest
    from biocreative.evaluation.calculation.hits \
        import HitsTest
    from biocreative.evaluation.calculation.macro_evaluation \
        import ProteinMacroEvaluationTest
    from biocreative.evaluation.calculation.protein \
        import ProteinEvaluationTest
    from biocreative.evaluation.calculation \
        import CalculationTests
    
    unittest.main()
    