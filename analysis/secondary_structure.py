from collections import defaultdict

def parse_secondary_structure(pdb_lines):
    structure = defaultdict(dict)
    for line in pdb_lines:
        # HELIX: Columnas 20 (Chain), 22-25 (Start), 34-37 (End)
        if line.startswith("HELIX"):
            try:
                chain = line[19].strip()
                start = int(line[21:25].strip())
                end = int(line[33:37].strip())
                for res_num in range(start, end + 1):
                    structure[chain][res_num] = 'H'
            except (ValueError, IndexError):
                continue
                
        # SHEET: Columnas 22 (Chain), 23-26 (Start), 34-37 (End)
        elif line.startswith("SHEET"):
            try:
                chain = line[21].strip()
                start = int(line[22:26].strip())
                end = int(line[33:37].strip())
                for res_num in range(start, end + 1):
                    structure[chain][res_num] = 'E'
            except (ValueError, IndexError):
                continue
    return structure

def structure_to_ascii(residue_ids, chain_structure_map):
    result = ""
    for res_id in residue_ids:
        # Usamos '-' para loops para que sea más legible que un punto
        sec_type = chain_structure_map.get(res_id, '-')
        result += sec_type
    return result

def format_structure_output(sequence, structure_line, width=80):
    output = []
    for i in range(0, len(sequence), width):
        chunk_seq = sequence[i:i+width]
        chunk_struct = structure_line[i:i+width]
        output.append(f"Struct: {chunk_struct}")
        output.append(f"Seq   : {chunk_seq}\n")
    return "\n".join(output)