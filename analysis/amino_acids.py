import matplotlib.pyplot as plt
from collections import Counter

# Diccionario estándar de aminoácidos
AMINO_ACIDS = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLU": "E", "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "SEC": "U", "PYL": "O"
}

def extract_sequences(pdb_lines):
    """
    Extrae secuencias e IDs de residuos para ssvis y otros comandos.
    Retorna: { chain_id: (sequence_string, residue_id_list) }
    """
    chains = {}
    seen = set()
    for line in pdb_lines:
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            chain_id = line[21].strip()
            res_name = line[17:20].strip()
            res_id = line[22:26].strip()
            
            # Identificador único para evitar conformaciones alternativas
            uid = (chain_id, res_id)
            if uid not in seen:
                seen.add(uid)
                if res_name in AMINO_ACIDS:
                    if chain_id not in chains:
                        chains[chain_id] = {"seq": "", "ids": []}
                    
                    chains[chain_id]["seq"] += AMINO_ACIDS[res_name]
                    chains[chain_id]["ids"].append(int(res_id))
    
    return {cid: (data["seq"], data["ids"]) for cid, data in chains.items()}

def parse_chain_sequences(pdb_data):
    """
    Versión compatible con el comando 'sequence'.
    Retorna un dict: {chain_id: [res1, res2, ...]}
    """
    sequences_data = extract_sequences(pdb_data.splitlines())
    # Convertimos el string de secuencia en lista para mantener compatibilidad
    return {cid: list(seq) for cid, (seq, ids) in sequences_data.items()}

def parse_chain_sequence(pdb_data, chain_id="A"):
    """Retorna la secuencia (lista) de una sola cadena."""
    all_chains = parse_chain_sequences(pdb_data)
    return all_chains.get(chain_id, [])

def count_amino_acids(sequence):
    """Cuenta la frecuencia usando Counter."""
    return Counter(sequence)

def print_sequences(chains, line_length=60):
    """Imprime secuencias en formato FASTA-like."""
    for chain_id, seq_list in chains.items():
        sequence = "".join(seq_list)
        print(f"\n>Chain {chain_id}")
        for i in range(0, len(sequence), line_length):
            print(sequence[i:i+line_length])

def plot_amino_acid_counts(counts, title="Amino Acid Counts"):
    """Genera el gráfico de barras de los aminoácidos."""
    labels = sorted(counts)
    values = [counts[k] for k in labels]
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="skyblue")
    plt.title(title)
    plt.xlabel("Amino Acids")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()