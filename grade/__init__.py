class BioData(object):
    def __init__(self, path=None, type=None):
        self._path = path
        self._type = type
        self._data = None

    def __add__(self, other):
        self.data = dict([(k, dict(self.data[k], **other.data[k])) for k in self.data if k in other.data])
        return self

    def __iadd__(self, other):
        self.data = dict([(k, dict(self.data[k], **other.data[k])) for k in self.data if k in other.data])
        return self

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, d):
        self._data = d

class MetricData(object):
    def __init__(self, data=None):
        self._data = data

    def __add__(self, other):
        if isinstance(self, MetricData) and isinstance(other, MetricData):
            self.data = dict([(k, self.data[k] + other.data[k]) for k in self.data if k in other.data])
        elif isinstance(self, MetricData):
            self.data = dict([(k, self.data[k] + other) for k in self.data])
        return self
    def __sub__(self, other):
        if isinstance(self, MetricData) and isinstance(other, MetricData):
            self.data = dict([(k, self.data[k] - other.data[k]) for k in self.data if k in other.data])
        elif isinstance(self, MetricData):
            self.data = dict([(k, self.data[k] - other) for k in self.data])
        return self
    def __mul__(self, other):
        if isinstance(self, MetricData) and isinstance(other, MetricData):
            self.data = dict([(k, self.data[k] * other.data[k]) for k in self.data if k in other.data])
        elif isinstance(self, MetricData):
            self.data = dict([(k, self.data[k] * other) for k in self.data])
        return self
    def __div__(self, other):
        if isinstance(self, MetricData) and isinstance(other, MetricData):
            self.data = dict([(k, self.data[k] / other.data[k]) for k in self.data if k in other.data])
        elif isinstance(self, MetricData):
            self.data = dict([(k, self.data[k] / other) for k in self.data])
        return self
    def __floordiv__(self, other):
        if isinstance(self, MetricData) and isinstance(other, MetricData):
            self.data = dict([(k, self.data[k] // other.data[k]) for k in self.data if k in other.data])
        elif isinstance(self, MetricData):
            self.data = dict([(k, self.data[k] // other) for k in self.data])
        return self
    def intersect(self, other):
        self.data = dict([(k, self.data[k]) for k in self.data if k in other.data])
        return self

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, d):
        self._data = d


class Metrics(object):
    def __init__(self, data=None):
        self._data = data.data
        self._hbonds = self._get_data('hbonds')
        self._docking_score = self._get_data('docking_score')
        self._stacking = self._get_data('stacking')

    @property
    def hbonds(self):
        return self._hbonds
    @hbonds.setter
    def hbonds(self, hb):
        self._hbonds = hb

    @property
    def docking_score(self):
        return self._docking_score
    @docking_score.setter
    def docking_score(self, ds):
        self._docking_score = ds

    @property
    def stacking(self):
        return self._stacking
    @stacking.setter
    def stacking(self, st):
        self._stacking = st


    def _get_data(self, name):
        if not self._data:
            raise Exception
        res = MetricData()
        res.data = dict([(k, self.data[k].get(name)) for k in self.data])
        return res

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, d):
        self._data = d


class ScoringFunction(object):
    def __init__(self):
        self._sf = None

    @property
    def initialize(self):
        pass
    @initialize.setter
    def initialize(self, sf):
        self._sf = sf

    def filter(self, treshold, metric):
        res = MetricData()
        if metric == '<':
            res.data = dict([k, self._sf.data[k]] for k in self._sf.data if self._sf.data[k] < treshold)
        if metric == '>':
            res.data = dict([k, self._sf.data[k]] for k in self._sf.data if self._sf.data[k] >= treshold)
        if metric == '==':
            res.data = dict([k, self._sf.data[k]] for k in self._sf.data if self._sf.data[k] == treshold)
        return res

    def separate(self, split_points, direct='fwd'):
        baskets = []
        start_point, end_point = 0, 0
        for i in split_points:
            (start_point, end_point) = (end_point, i) if direct == 'fwd' else (i, end_point)
            baskets.append(self.filter(start_point, '>').intersect(self.filter(end_point, '<')))
        return baskets


# ============Examples============

data1 = BioData()
data1.data = {'q1': {'hbonds':2, 'docking_score':2, 'c':3}, 'q2': {'hbonds':33, 'docking_score':32, 'e': 2}}

data2 = BioData()
data2.data = {'q1': {'stacking':1, 'd':2, 'sc':3}, 'q2': {'stacking':33, 'd':32, 'se': 2}}

m = Metrics(data1 + data2)
sf = ScoringFunction()

sf.initialize = (m.hbonds + m.docking_score) * 0.3 + m.stacking

print sf.filter(10, '<').data
print sf.filter(100, '<').data

print map(lambda x: x.data, sf.separate([3, 50, 100]))