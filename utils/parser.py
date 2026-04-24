from Bio.PDB import PDBParser

def parse_pdb(filename):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("X", filename)
    chains = set()
    residues = 0
    atoms = 0
    ligands = set()

    for model in structure:
        for chain in model:
            chains.add(chain.id)
            for residue in chain:
                if residue.id[0] == " ":  # exclude water/hetatm
                    residues += 1
                else:
                    ligands.add(residue.resname)
                atoms += len(residue)

    print(f"📦 Chains: {len(chains)}")
    print(f"🧬 Residues: {residues}")
    print(f"🔬 Atoms: {atoms}")
    print(f"💊 Ligands: {', '.join(ligands) if ligands else 'None'}")

# utils/parser.py

from collections import defaultdict
from analysis.amino_acids import AMINO_ACIDS

def extract_sequence_and_residues(pdb_data):
    """
    Extract amino acid sequences and residue numbers per chain from ATOM records.
    Returns a dict: {chain_id: ([amino_acid_sequence], [residue_ids])}
    """
    chains = defaultdict(lambda: ([], []))
    seen = set()

    for line in pdb_data.splitlines():
        if line.startswith("ATOM"):
            res_name = line[17:20].strip()
            chain_id = line[21].strip()
            res_id = line[22:26].strip()
            uid = (chain_id, res_id)

            if uid not in seen and res_name in AMINO_ACIDS:
                seen.add(uid)
                chains[chain_id][0].append(AMINO_ACIDS[res_name])
                chains[chain_id][1].append(res_id)

    return chains


import requests


