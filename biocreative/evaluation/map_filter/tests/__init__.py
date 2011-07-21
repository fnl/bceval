import unittest

from biocreative.evaluation.map_filter.int_dict import INTDataDict
from biocreative.evaluation.map_filter.ipt_dict import IPTDataDict
from biocreative.evaluation.container.results import ResultContainer as RC

class MapFilterTests(unittest.TestCase):
    
    def setUp(self):
        self.ho_map = {
            'H1': ['M1', 'F1', 'W1'],
            'H2': ['M2', 'W2'],
            'H3': ['F3', 'W1'],
            'F3': ['H3'], # NB: creates the circularity problem
        }
        self.tax_map = {
            'H1': 'H', 'H2': 'H', 'H3': 'H', 'H4': 'H',
            'M1': 'M', 'M2': 'M', 'M3': 'M', 'M4': 'M',
            'F1': 'F', 'F2': 'F', 'F3': 'F', 'F4': 'F',
            'W1': 'W', 'W2': 'W', 'W3': 'W', 'W4': 'W',
        }
    
    def set_up_INT(self):
        self.gs = INTDataDict(enumerate([
            [RC('H1'), RC('H2')],
            [RC('H4')],
            [RC('H1'), RC('H3')],
            [RC('H3')],
            [RC('H3'), RC('H1')],
            [RC('H3'), RC('F3')],
            [RC('H3'), RC('F3')],
        ]))
        self.results = INTDataDict(enumerate([
            [RC('M1', 1), RC('M2', 2), RC('M3', 3)], # 1:1
            [RC('M4', 1)], # 0:0
            [RC('W1', 3)], # 1:n
            [RC('F3', 1), RC('W1', 2)], # n:1
            [RC('W2', 2), RC('F1', 2), RC('W1', 3)], # n:m
            [RC('F3', 1), RC('H3', 2)], # 1:0
            [RC('F3', 1)], # 1:0
        ]))
        self.expected_ho_results = enumerate([
            ['H1', 'H2', 'M3'],
            ['M4'],
            ['H3', 'H1'],
            ['H3'],
            ['W2', 'H1', 'H3'],
            ['F3', 'H3'],
            ['F3'],
        ])
        self.expected_of_results = enumerate([
            ['H1', 'H2'],
            [],
            ['H3', 'H1'],
            ['H3'],
            ['H1', 'H3'],
            ['F3', 'H3'],
            ['F3'],
        ])
    
    def test_int_homonym_ortholog_mapping(self):
        self.set_up_INT()
        self.results.map_homonym_orthologs(self.ho_map, self.gs)
        self.assert_results(self.expected_ho_results)
    
    def test_int_organism_filtering(self):
        self.set_up_INT()
        self.results.map_homonym_orthologs(self.ho_map, self.gs)
        self.results.filter_organisms(self.tax_map, self.gs)
        self.assert_results(self.expected_of_results)
        
    
    def set_up_IPT(self):
        self.gs = IPTDataDict(enumerate([
            [RC(('H1', 'H2')), RC(('H1', 'H3'))],
            [RC(('H1', 'H4'))],
            [RC(('H1', 'H2'))],
            [RC(('H1', 'H2')), RC(('H2', 'H3'))],
            [RC(('H2', 'H3'))],
            [RC(('H2', 'H3')), RC(('H1', 'H2'))],
            [RC(('H2', 'H3')), RC(('F3', 'H2'))],
            [RC(('W1', 'H3'))],
        ]))
        self.results = IPTDataDict(enumerate([
            [RC(('M1', 'M2'), 1), RC(('F3', 'M1'), 2)], # 1:1
            [RC(('M1', 'M4'), 1)], # 0:0
            [RC(('H2', 'M1'), 1)], # partial
            [RC(('H2', 'W1'), 1)], # 1:n
            [RC(('M2', 'W1'), 1), RC(('M2', 'F3'), 2)], # n:1
            [
                 RC(('W2', 'W3'), 2), RC(('F1', 'W2'), 2),
                 RC(('M2', 'W1'), 3)
            ], # n:m
            [RC(('F3', 'M2')), RC(('H2', 'H3'))], # 1:0
            [RC(('W1', 'W3'))], # organism filter test
        ]))
        self.expected_ho_results = enumerate([
            [('H1', 'H2'), ('H1', 'H3')],
            [('M1', 'M4')],
            [('H1', 'H2')],
            [('H2', 'H3'), ('H1', 'H2')],
            [('H2', 'H3'), ('M2', 'F3')],
            [('W2', 'W3'), ('H1', 'H2'), ('H2', 'H3')],
            [('F3', 'H2'), ('H2', 'H3')],
            [('W1', 'W3')],
        ])
        self.expected_of_results = enumerate([
            [('H1', 'H2'), ('H1', 'H3')],
            [],
            [('H1', 'H2')],
            [('H2', 'H3'), ('H1', 'H2')],
            [('H2', 'H3')],
            [('H1', 'H2'), ('H2', 'H3')],
            [('F3', 'H2'), ('H2', 'H3')],
            [('W1', 'W3')],
        ])
    
    def test_ipt_homonym_ortholog_mapping(self):
        self.set_up_IPT()
        self.results.map_homonym_orthologs(self.ho_map, self.gs)
        self.assert_results(self.expected_ho_results)
    
    def test_ipt_organism_filtering(self):
        self.set_up_IPT()
        self.results.map_homonym_orthologs(self.ho_map, self.gs)
        self.results.filter_organisms(self.tax_map, self.gs)
        self.assert_results(self.expected_of_results)
    
    def assert_results(self, expected_results):
        for doi, expected in expected_results:
            items = [rc.item for rc in self.results[doi]]
            self.assertEqual(items, expected, "failed on DOI %i: %s != %s" % (
                doi, str(items), str(expected)
            ))
    

if __name__ == '__main__':
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()