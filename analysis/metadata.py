
def extract_metadata(pdb_data):
    metadata = {     #dictionary
          
         "title" : None,
         "experimental_method" : None,
         "resolution": None,
         "deposition_date" : None,
         "num_chains" : 0,
         "num_atoms": 0
    }

    seen_chains = set()
    atom_count = 0


    for line in pdb_data.splitlines():
        if line.startswith("TITLE"):
            if metadata["title"]:
                metadata["title"] += " " + line[10:].strip()
            else:
                metadata["title"] = line[10:].strip()
        elif line.startswith("EXPDTA"):
            metadata["experimental_method"] = line[10:].strip() 
        elif line.startswith("REMARK   2 RESOLUTION."):
            parts = line.split()  
            if len(parts) >= 4 and parts[3].replace('.', '', 1).isdigit():
                metadata["resolution"] = float(parts[3])
        elif line.startswith("HEADER"):
            metadata["deposition_date"] = line[50:59].strip()
        elif line.startswith("ATOM"):
            atom_count += 1
            chain_id = line[21]
            seen_chains.add(chain_id)

    metadata["num_chains"] = len(seen_chains)
    metadata["num_atoms"] = atom_count
    return metadata


def print_metadata(metadata, pdb_id):
    print(f"\nMetadata for {pdb_id}:\n")
    for key, value in metadata.items():
        label = key.replace("_", " ").capitalize()
        print(f"{label}: {value}")
            





