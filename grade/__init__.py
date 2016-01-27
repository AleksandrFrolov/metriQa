from enum import Enum

class DataType(Enum):
    mae = 'MAE'
    maegz = 'MAEGZ'
    pdb = 'PDB'
    adme = 'ADME'
    csv = 'CSV'

class BioData(object):
    def __iit__(self, input, type):
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
        pass
    @initialize.setter
    def initialize(self, sfunction):

        self._scoring_function = sfunction

    def filter(self, threshold):
        if not isinstance(input, BioData):
            raise Exception()

    def separate(self, split_points):
        if not isinstance(input, BioData):
            raise Exception()

class Metrics(object):
    def __init__(self, data):
        # INPUTS
        if isinstance(data, BioData):
            self._data = data
        else:
            raise Exception
        # METRICS
        # TODO: define functions for following params
        self._hbonds = None
        self._stacking = None
        self._docking_score = None

    # ===========h-bond===========
    @property
    def hbonds(self):
        return sum(self._hbonds.values()) if self._hbonds else 0
    @hbonds.setter
    def hbonds(self, hbonds_dict):
        self._hbonds = hbonds_dict

    def hbond(self, ligand_atom):
        return self._hbonds.get(ligand_atom, 0)

    # ===========docking score===========
    @property
    def docking_score(self):
        return self._docking_score or 0
    @docking_score.setter
    def docking_score(self, ds):
        self._docking_score = ds


# ============Examples============

# my_data = BioData('path_to_file', DataType.mae) + BioData('path_to_qikprop', DataType.adme)
# my_data += BioData('path_to_csv', DataType.csv)
#
# my_sfunction = ScoringFunction()
# my_sfunction.initialize = Metrics.hbonds + 0.3*Metrics.docking_score + 2
#
# result = my_sfunction.filter(my_data, 3.2)

data1 = BioData()
data1.data = {'q1': {'a':1, 'b':2, 'c':3}, 'q2': {'q':33, 'w':32, 'e': 2}}

data2 = BioData()
data2.data = {'q1': {'sa':1, 'sb':2, 'sc':3}, 'q2': {'sq':33, 'sw':32, 'se': 2}}

my_sfunction = ScoringFunction()
m = Metrics(data1 + data2)
my_sfunction.initialize = m.hbonds + 0.3*m.docking_score + 2
