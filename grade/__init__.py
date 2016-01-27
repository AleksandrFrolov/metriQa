from enum import Enum

class DataType(Enum):
    mae = 'MAE'
    maegz = 'MAEGZ'
    pdb = 'PDB'
    adme = 'ADME'
    csv = 'CSV'

class BioData(object):
    def __init__(self, input=None, type=None):
        self._input = input
        self._type = type
        # TODO: function for read data file.
        self._data = None

    def __add__(self, other):
        self.data = dict([(k, dict(self.data[k], **other.data[k])) for k in self.data if k in other.data.keys()])
        return self

    def __iadd__(self, other):
        self.data = dict([(k, dict(self.data[k], **other.data[k])) for k in self.data if k in other.data.keys()])
        return self

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, d):
        self._data = d

    def __str__(self):
        return str(self._data)


class ScoringFunction(object):
    def __init__(self):
        self._scoring_function = None

    @property
    def initialize(self):
        return True if self._scoring_function else False
    @initialize.setter
    def initialize(self, sfunction):
        self._scoring_function = sfunction

    def filter(self, threshold):
        pass

    def separate(self, split_points):
        pass

class Metrics(object):
    def __init__(self, data):
        # INPUTS
        if isinstance(data, BioData):
            self._data = data
        else:
            raise Exception
        # METRICS
        # TODO: define functions for following params
        self._hbonds = self._get_data('hbonds')
        self._stacking = self._get_data('stacking')
        self._docking_score = self._get_data('docking_score')

    def _get_data(self, name):
        res = BioData()
        res.data = dict([(s, self._data.data[s].get(name)) for s in self._data.data])
        return MetricsVector(res)

    # ===========h-bond===========
    @property
    def hbonds(self):
        return self._hbonds
    @hbonds.setter
    def hbonds(self, hbonds_dict):
        self._hbonds = hbonds_dict

    # def hbond(self, ligand_atom):
    #     return self._hbonds.get(ligand_atom, 0)

    # ===========docking score===========
    @property
    def stacking(self):
        return self._stacking
    @stacking.setter
    def stacking(self, stacking):
        self._stacking = stacking

    # ===========docking score===========
    @property
    def docking_score(self):
        return self._docking_score
    @docking_score.setter
    def docking_score(self, ds):
        self._docking_score = ds

# =======helper class=======
class MetricsVector(object):
    def __init__(self, data):
        self._data = data

    def __add__(self, other):
        self.data = dict([(k, self._data.data[k] + (other._data.data.get(k) if isinstance(other, MetricsVector) else other)) for k in self._data.data])
        return MetricsVector(self)
    def __div__(self, other):
        self.data = dict([(k, self._data.data[k] / (other._datadata.get(k, 0) if isinstance(other, MetricsVector) else other)) for k in self._data.data])
        return MetricsVector(self)
    def __floordiv__(self, other):
        self.data = dict([(k, self._data.data[k] // (other._data.data.get(k, 0) if isinstance(other, MetricsVector) else other)) for k in self._data.data])
        return MetricsVector(self)
    def __mul__(self, other):
        self.data = dict([(k, self._data.data[k] * (other._data.data.get(k, 0) if isinstance(other, MetricsVector) else other)) for k in self._data.data])
        return MetricsVector(self)

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, data):
        self._data = MetricsVector(data).data


# ============Examples============

# my_data = BioData('path_to_file', DataType.mae) + BioData('path_to_qikprop', DataType.adme)
# my_data += BioData('path_to_csv', DataType.csv)
#
# my_sfunction = ScoringFunction()
# my_sfunction.initialize = Metrics.hbonds + 0.3*Metrics.docking_score + 2
#
# result = my_sfunction.filter(my_data, 3.2)

data1 = BioData()
data1.data = {'q1': {'hbonds':1, 'docking_score':2, 'c':3}, 'q2': {'hbonds':33, 'docking_score':32, 'e': 2}}

data2 = BioData()
data2.data = {'q1': {'stacking':1, 'd':2, 'sc':3}, 'q2': {'stacking':33, 'd':32, 'se': 2}}

my_sfunction = ScoringFunction()
m = Metrics(data1 + data2)
print ((m.docking_score + m.hbonds + m.stacking + 3) // m.hbonds).data.data