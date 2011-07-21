class Hits(object):
    """A storage for the current number of hits - stores only TP, FP, FN, and
    TN counts - from which the calculation classes then can produce the
    relevant evaluation scores.
    """
    
    def __init__(self, tp=0, fp=0, fn=None, tn=0):
        """The fn count by default is None and should be defined after or
        during instantiation as the respective relevant value.
        
        Usually, this will be either the max. FN count that can be achieved
        given the GS or 0.
        """
        self._tp = tp
        self._fp = fp
        self._fn = fn # needs to be intialized before using!
        self._tn = tn
    
    def all(self):
        """Return all counters."""
        return (self._tp, self._fp, self._fn, self._tn)
    
    def sum(self):
        """Return the sum of all counters."""
        return sum((self._tp, self._fp, self._fn, self._tn))
    
    def add_to(self, attr, value):
        """Adds a given value to a hit counter."""
        self._set("_%s" % attr, value + getattr(self, attr))
    
    def _get_tp(self):
        return self._tp
    
    def _set_tp(self, value):
        Hits.assert_non_negative_int(value)
        self._tp = value
    
    tp = property(_get_tp, _set_tp, doc="true positive")
    
    def _get_fp(self):
        return self._fp
    
    def _set_fp(self, value):
        Hits.assert_non_negative_int(value)
        self._fp = value
    
    fp = property(_get_fp, _set_fp, doc="false positive")
    
    def _get_fn(self):
        return self._fn
    
    def _set_fn(self, value):
        Hits.assert_non_negative_int(value)
        self._fn = value
    
    fn = property(_get_fn, _set_fn, doc="false negative")
    
    def _get_tn(self):
        return self._tn
    
    def _set_tn(self, value):
        Hits.assert_non_negative_int(value)
        self._tn = value
    
    tn = property(_get_tn, _set_tn, doc="true negative")
    
    def _set(self, attr, value):
        "Setter for the hit counters."
        assert hasattr(self, attr), \
            "_set(%s, %i): no such attribute" % (attr, value)
        Hits.assert_non_negative_int(value)
        setattr(self, attr, value)
    
    @staticmethod
    def assert_non_negative_int(value):
        assert isinstance(value, int) and value >= 0, \
            "the given value (%s) is illegal" % str(value)
    
