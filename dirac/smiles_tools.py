from collections import namedtuple
from enum import Enum
import re
from rdkit.Chem import MolFromSmiles, MolFromSmarts, MolToSmiles
from rdkit.Chem import FragmentOnBonds

def molecules_fragmentation(smiles, template):
    """
    Separate molecule on fragments.
    :param smiles: smiles string
    :param template: smart template [!R][R]
    :return: list of ChemFragment's
    """
    smiles = MolFromSmiles(smiles)
    bis = smiles.GetSubstructMatches(MolFromSmarts(template))
    bs = [smiles.GetBondBetweenAtoms(x, y).GetIdx() for x, y in bis]
    nm = FragmentOnBonds(smiles, bs)
    frags =MolToSmiles(nm, True).split('.')
    frag_name = lambda s: re.sub('\(*\[+\d*\*+\]+\)*', '', s)
    frag_smiles = lambda s: re.sub('\[+\d*\*+\]+', '[*]', s)
    frag_type = lambda s: FragmentType.heterocycle \
        if len([a for a in MolFromSmiles(s).GetAtoms() if a.IsInRing()]) > 0 \
        else FragmentType.joiner if s.count('*') == 2 else FragmentType.attacher
    return [ChemFragment(frag_name(s), frag_smiles(s), frag_type(s)) for s in frags]


class FragmentType(Enum):
    heterocycle = 'HETEROCYCLE'
    joiner = 'JOINER'
    attacher = 'ATTACHER'

ChemFragment = namedtuple('ChemFragment', 'name, smiles, type')