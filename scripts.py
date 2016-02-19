from rdkit import Chem
from rdkit.Chem import AllChem
from dirac import smiles_tools
from dirac import db_tools


def db_create(in_file):
    try:
        source_f = open(in_file, 'r').readlines()
    except:
        print 'Error source file...'

    for data in source_f:
        data = data.strip()
        try:
            s = data.strip().split(' ')[0]
            print s
            frags = smiles_tools.molecules_fragmentation(s)
            db_tools.fragments_db(frags)
        except:
            pass


def structure_gen(cores=[], frags=[], convertToSmiles=True):
    cores = cores if type(cores) == list else [cores]
    frags = frags if type(frags) == list else [frags]
    out = []
    for CORE in cores:
        for FRAG in frags:
            try:
                for c_idx in smiles_tools.star_index(Chem.MolFromSmiles(CORE)):
                    cr = Chem.EditableMol(Chem.MolFromSmiles(CORE))
                    cr.RemoveAtom(c_idx)
                    core = cr.GetMol()
                    for f_idx in smiles_tools.star_index(Chem.MolFromSmiles(FRAG)):
                        # core = Chem.DeleteSubstructs(cr, Chem.MolFromSmiles('*'))
                        # frag = Chem.DeleteSubstructs(fr, Chem.MolFromSmiles('*'))
                        fr = Chem.EditableMol(Chem.MolFromSmiles(FRAG))
                        fr.RemoveAtom(0 if f_idx == 0 else f_idx + 1)
                        frag = fr.GetMol()
                        combo = Chem.CombineMols(frag, core)
                        edcombo = Chem.EditableMol(combo)
                        # edcombo.AddBond(c_idx, core.GetNumAtoms(), order=Chem.rdchem.BondType.SINGLE)
                        edcombo.AddBond(f_idx if f_idx == 0 else f_idx, frag.GetNumAtoms() + c_idx, order=Chem.rdchem.BondType.SINGLE)
                        if convertToSmiles == True:
                            out.append(Chem.MolToSmiles(edcombo.GetMol()))
                        else:
                            out.append(edcombo.GetMol())
            except:
                print 'Error...'

    return out


def geterocycle_attache(cores, cycles):
    for core in cores:
        core = Chem.MolFromSmiles(core)
        for cycle in cycles:
            cycle = Chem.MolFromSmiles(cycle)
            print cycle.GetAtoms()



# cores = ['[*]c1ccnc(c12)cccc2', 'c1cccc(c12)N=CC2[*]', 'n1cn([*])c(c12)cccc2', 'c1cccc(c12)ncnc2[*]', '[*]c1ccnc(c12)nccc2', '[*]c1cccc(c12)[nH]nc2']
# frags = [str(t[2]).strip() for t in db_tools.fragments_view() if t[3] == smiles_tools.FragmentType.joiner and str(t[2]).count('*') == 2]
# heterocycles = [str(t[2]).strip() for t in db_tools.fragments_view() if t[3] == smiles_tools.FragmentType.heterocycle]

# for i in structure_gen('[*]c1ccnc(c12)cccc2', '[*]NC(=O)C[*]'):
# for i in structure_gen(cores, frags):
#     for l in structure_gen(i, heterocycles):
#         print l

geterocycle_attache('c1ccnc(c12)cccc2', 'c1cccc(c12)N=CC2')