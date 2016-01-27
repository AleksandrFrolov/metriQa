from data import DataType

class BioData(object):
    def __iit__(self, input, type):
        self._input = input
        self._type = type
        # TODO: function for read data file.
        self._data = None

    def __add__(self, other):
        pass

    def __iadd__(self, other):
        pass

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, d):
        self._data = d


class ScoringFunction(object):
    def __init__(self):
        self._scoring_function = None

    @property
    def initialize(self):
        return self._scoring_function
    @initialize.setter
    def initialize(self, sfunction):
        self._scoring_function = sfunction

    def filter(self, input):
        if not isinstance(input, BioData):
            raise Exception()

    def separate(self, input, split_points):
        if not isinstance(input, BioData):
            raise Exception()

class Metrics(object):
    def __init__(self, mae=None, pdb=None, adme=None):
        # INPUTS
        self._mae = mae
        self._pdb = pdb
        self._adme = adme
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
    @docking_score
    def docking_score(self, ds):
        self._docking_score = ds


# ============Examples============

my_data = BioData('path_to_file', DataType.mae) + BioData('path_to_qikprop', DataType.adme)
my_data += BioData('path_to_csv', DataType.csv)

my_sfunction = ScoringFunction()
my_sfunction.initialize = Metrics.hbonds + 0.3*Metrics.docking_score + 2

result = my_sfunction.filter(my_data)
