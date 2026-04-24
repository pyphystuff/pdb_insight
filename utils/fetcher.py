import requests

'''def fetch_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{pdb_id}.pdb", "w") as f:
            f.write(response.text)
        print(f"✅ Downloaded {pdb_id}.pdb")
    else:
        print("❌ Failed to fetch PDB file")
'''
import os
import requests

def fetch_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{pdb_id}.pdb"
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"✅ Downloaded {filename}")
        return response.text  # <-- ✅ Add this line
    else:
        print(f"❌ Failed to download PDB ID {pdb_id}")
        return None
