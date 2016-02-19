from collections import namedtuple
from enum import Enum
import re
from rdkit.Chem import MolFromSmiles, MolFromSmarts, MolToSmiles
from rdkit.Chem import FragmentOnBonds
from rdkit.Chem import BRICS

def is_cyclic(smiles):
    return len([a for a in MolFromSmiles(smiles).GetAtoms() if a.IsInRing()]) > 0

def rdkit_smiles(s):
    return MolToSmiles(MolFromSmiles(s))

def star_index(s):
    """
    Return points for attach.
    :param s: mol from rdkit
    :return: list of indexes
    """
    i = 0
    res = []
    for l in s.GetAtoms():
        if l.GetSymbol() == '*':
            for i in l.GetBonds():
                res.append(i.GetBeginAtomIdx())
    return res

def molecules_fragmentation(sm, template="[!R][R]"):
    """
    Separate molecule on fragments.
    :param smiles: smiles string
    :param template: smart template, for example [!R][R]
    :return: ChemFragment list
    """
    smiles = MolFromSmiles(sm)
    bis = smiles.GetSubstructMatches(MolFromSmarts(template))
    bs = [smiles.GetBondBetweenAtoms(x, y).GetIdx() for x, y in bis]
    nm = FragmentOnBonds(smiles, bs) if bs else smiles
    frags = []
    for f in MolToSmiles(nm, True).split('.'):
        if not is_cyclic(f):
            frags.append(f)
        else:
            if MolFromSmiles(f).GetRingInfo().NumRings() == 1:
                frags.append(f)
            else:
                for i in BRICS.BRICSDecompose(MolFromSmiles(f)):
                    frags.append(i)
    frag_name = lambda s: re.sub('\(*\[+\d*\*+\]+\)*', '', s)
    frag_smiles = lambda s: re.sub('\[+\d*\*+\]+', '[*]', s)
    frag_type = lambda s: FragmentType.heterocycle if is_cyclic(s) \
        else FragmentType.joiner if s.count('*') > 1 else FragmentType.attacher
    for s in frags:
        try:
            yield ChemFragment(frag_name(rdkit_smiles(s)), frag_name(rdkit_smiles(s)) if frag_type(s) == FragmentType.heterocycle else frag_smiles(s), frag_type(s))
        except:
            pass

class FragmentType(Enum):
    heterocycle = 'HETEROCYCLE'
    joiner = 'JOINER'
    attacher = 'ATTACHER'

ChemFragment = namedtuple('ChemFragment', 'name, smiles, type')