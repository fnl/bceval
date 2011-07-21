import unittest

from mock import Mock, patch, sentinel
from random import random, randint

from biocreative.evaluation.container.data_dict import AbstractDataDict

class AbstractDataDictTest(unittest.TestCase):
    
    RAW_DATA_SENTINEL = [
        (sentinel.DOI, sentinel.Result, sentinel.Rank, sentinel.Confidence),
    ]
    
    def setUp(self):
        self.add = AbstractDataDict({"b": [1], "c": [1,2], "a": []})
    
    def test_init_state(self):
        self.assertTrue(isinstance(self.add, dict))
    
    def test_iterator(self):
        keys = [k for k in self.add]
        self.assertEqual(keys, ["a", "b", "c"])
    
    def test_keys(self):
        self.assertEqual(self.add.keys(), ["a", "b", "c"])
    
    @patch('biocreative.evaluation.container.results.ResultContainer')
    def test_load_from_with_GS_None(self, rc_mock):
        dd, gs_dict = AbstractDataDictTest.set_up_load_from()
        
        self.assertEqual(None, dd.ignored)
        self.assertFalse(dd._ignore.called)
        self.assertTrue(dd.assert_duplicates.called)
        dd.assert_duplicates.assert_called_with(
            sentinel.DOI, sentinel.Result
        )
        self.assertTrue(rc_mock.called)
        rc_mock.assert_called_with(
            sentinel.Result,
            rank=sentinel.Rank, confidence=sentinel.Confidence
        )
        self.assert_add_result(dd, rc_mock)
        self.assertTrue(dd.sort_results.called)
    
    @patch('biocreative.evaluation.container.results.ResultContainer')
    def test_load_from_with_GS_Dummy(self, rc_mock):
        dd, gs_dict = AbstractDataDictTest.set_up_load_from(
            gs_dict={"dummy": None}
        )
        
        self.assertEqual(set([]), dd.ignored)
        self.assertTrue(dd._ignore.called)
        dd._ignore.assert_called_with(sentinel.DOI, gs_dict)
        self.assertTrue(dd.assert_duplicates.called)
        dd.assert_duplicates.assert_called_with(
            sentinel.DOI, sentinel.Result
        )
        self.assertTrue(rc_mock.called)
        rc_mock.assert_called_with(
            sentinel.Result, 
            rank=sentinel.Rank, confidence=sentinel.Confidence
        )
        self.assert_add_result(dd, rc_mock)
        self.assertTrue(dd.sort_results.called)
    
    @patch('biocreative.evaluation.container.results.ResultContainer')
    def test_load_from_with_GS_Sentinel(self, rc_mock):
        dd, gs_dict = AbstractDataDictTest.set_up_load_from(
            gs_dict={sentinel.DOI: None}, match_gs=True
        )
        
        self.assertEqual(set([]), dd.ignored)
        self.assertTrue(dd._ignore.called)
        dd._ignore.assert_called_with(sentinel.DOI, gs_dict)
        self.assertFalse(dd.assert_duplicates.called)
        self.assertFalse(rc_mock.called)
        self.assertFalse(dd.add_result.called)
        self.assertTrue(dd.sort_results.called)
    
    def test_add_entries_only_in(self):
        other = AbstractDataDict({"d": None, "c": None, "a": None})
        value_dummy = lambda: None
        added = self.add.add_entries_only_in(other, Value_Type=value_dummy)
        self.assert_changed_dictionary_size(added)
        received = self.add.values()
        received.sort()
        expected = [[], [1,2], [1], None]
        expected.sort()
        self.assertEqual(
            received, expected, "wrong value type added %s" % str(received)
        )
    
    def test_delete_entries_not_in(self):
        other = AbstractDataDict({"d": None, "c": None, "a": None})
        deleted = self.add.delete_entries_not_in(other)
        self.assert_changed_dictionary_size(deleted * -1)
    
    def test_prune_empty_sets(self):
        pruned = self.add.prune_empty_sets()
        self.assert_changed_dictionary_size(pruned * -1)
    
    def test_ignore(self):
        ignore = AbstractDataDict({"d": None, "c": None, "a": None})
        self.add.ignored = set()
        
        for item, expected in [
            ("a", False), ("b", True), ("c", False), ("b", True)
        ]:
            received = self.add._ignore(item, ignore)
            self.assertEqual(
                expected, received,
                "item was not ignored (expected: %s, received: %s)" % (
                    str(expected), str(received)
                )
            )
        
        self.assertEqual(
            set(["b"]), self.add.ignored,
            "ignored items mismatch (expected: %s, received: %s)" % (
                "set(['b'])", str(self.add.ignored)
            )
        )
    
    def assert_changed_dictionary_size(self, change):
        self.assertEqual(
            abs(change), 1, "unexpected change count (%i)" % abs(change)
        )
        self.assertEqual(
            len(self.add), 3 + change,
            "dictionary size did not change (%i/3 + %i)" % (
                len(self.add), change
            )
        )
    
    @staticmethod
    def set_up_load_from(gs_dict=None, match_gs=False):
        dd = AbstractDataDictTest.set_up_mocked_data_dict()
        dd._ignore.return_value = match_gs
        dd.load_from(
            AbstractDataDictTest.RAW_DATA_SENTINEL, gold_standard=gs_dict
        )
        return dd, gs_dict
    
    @staticmethod
    def set_up_mocked_data_dict():
        dd = AbstractDataDict()
        dd.assert_duplicates = Mock()
        dd.add_result = Mock()
        dd.sort_results = Mock()
        dd._ignore = Mock()
        return dd
    
    def assert_add_result(self, dd, rc_mock):
        self.assertTrue(dd.add_result.called)
        add_result_args, add_result_kwds = dd.add_result.call_args
        self.assertEqual(0, len(add_result_kwds))
        self.assertEqual(2, len(add_result_args))
        self.assertEqual(sentinel.DOI, add_result_args[0])
        self.assertEqual(type(rc_mock), type(add_result_args[1]))
    
    # ========================
    # = Behaviour-like Tests =
    # ========================
    
    @patch('biocreative.evaluation.container.results.ResultContainer')
    def test_load_from(self, rc_mock):
        dd = self.get_mocked_data_dict()
        dd.load_from(
            self.get_data_iterator()
        )
        self.assertEqual(dd.ignored, None)
        self.assertEqual(dd.assert_duplicates.call_count, 100)
        self.assertEqual(dd.add_result.call_count, 100)
        self.assertEqual(dd.sort_results.call_count, 1)
    
    @patch('biocreative.evaluation.container.results.ResultContainer')
    def test_load_from_with_gold_standard(self, rc_mock):
        dd = self.get_mocked_data_dict()
        gold_standard =  dict(
            (doi, None) for doi in range(1, 30, 2)
        )
        raw_data = [
            i for i in self.get_data_iterator()
        ]
        dd.load_from(raw_data, gold_standard)
        gs_dois = set(gold_standard.keys())
        raw_data_not_ignored = [i[0] for i in raw_data if i[0] in gs_dois]
        dois_ignored = set([i[0] for i in raw_data if i[0] not in gs_dois])
        raw_data_processed = len(raw_data_not_ignored)
        # check the ignored articles match
        self.assertEqual(type(dd.ignored), set)
        self.assertEqual(len(dd.ignored), len(dois_ignored))
        # check all functions have been called as often as expected
        self.assertEqual(dd.sort_results.call_count, 1)
        self.assertEqual(rc_mock.call_count, raw_data_processed)
        self.assertEqual(dd.add_result.call_count, raw_data_processed)
        self.assertEqual(dd.assert_duplicates.call_count, raw_data_processed)
        self.assertTrue(dd.add_result.call_count, raw_data_processed)
        
    
    @staticmethod
    def get_mocked_data_dict():
        dd = AbstractDataDict()
        dd.assert_duplicates = Mock()
        dd.add_result = Mock()
        dd.sort_results = Mock()
        return dd
    
    @staticmethod
    def get_data_iterator():
        for i in range(100):
            yield randint(1,30), "P%03iAB" % (i + 1), i, random()
    

if __name__ == '__main__':
    unittest.main()