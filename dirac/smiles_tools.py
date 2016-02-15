from collections import namedtuple
from enum import Enum
import re
from rdkit.Chem import MolFromSmiles, MolFromSmarts, MolToSmiles
from rdkit.Chem import FragmentOnBonds
from rdkit.Chem import BRICS

def is_cyclic(smiles):
    return len([a for a in MolFromSmiles(smiles).GetAtoms() if a.IsInRing()]) > 0

def molecules_fragmentation(smiles, template):
    """
    Separate molecule on fragments.
    :param smiles: smiles string
    :param template: smart template, for example [!R][R]
    :return: ChemFragment list
    """
    smiles = MolFromSmiles(smiles)
    bis = smiles.GetSubstructMatches(MolFromSmarts(template))
    bs = [smiles.GetBondBetweenAtoms(x, y).GetIdx() for x, y in bis]
    nm = FragmentOnBonds(smiles, bs)
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
    frag_name = lambda s: MolToSmiles(MolFromSmiles(re.sub('\(*\[+\d*\*+\]+\)*', '', s)))
    frag_smiles = lambda s: re.sub('\[+\d*\*+\]+', '[*]', s)
    frag_type = lambda s: FragmentType.heterocycle if is_cyclic(s) \
        else FragmentType.joiner if s.count('*') == 2 else FragmentType.attacher
    return [ChemFragment(frag_name(s), frag_smiles(s), frag_type(s)) for s in frags]


class FragmentType(Enum):
    heterocycle = 'HETEROCYCLE'
    joiner = 'JOINER'
    attacher = 'ATTACHER'

ChemFragment = namedtuple('ChemFragment', 'name, smiles, type')

print '.'.join(map(lambda s: s.smiles, molecules_fragmentation('C1CCN[C@@H](C1)C2(CN(C2)C(=O)C3=C(C(=C(C=C3)F)F)NC4=C(C=C(C=C4)I)F)O', '[!R][R]')))
