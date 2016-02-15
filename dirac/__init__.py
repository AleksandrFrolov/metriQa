"""
Paul Dirac pipeline for create new molecules.
"""

class Singleton(type):
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class MolSet(object):
    __metaclass__ = Singleton

    def __init__(self, mol_set):
        self._mol_set = mol_set

    def filter(self, filter_function):
        pass

    def join(self, other):
        pass


def mol_gen(cores, frags):
    res_set = []
    for core in cores:
        for frag in frags:
            pass