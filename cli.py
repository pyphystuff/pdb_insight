# cli.py
import click
import sys
import requests
from utils.fetcher import fetch_pdb
from utils.parser import parse_pdb
from utils.llm import generate_summary
from analysis import metadata, amino_acids
from analysis.secondary_structure import (
    parse_secondary_structure, 
    structure_to_ascii, 
    format_structure_output
)
from analysis.visualizer import animate_structure

@click.group()
def cli():
    """🔬 PDB Insight - Terminal Tool for Structure Analysis and quick reference"""
    pass

# --- 📥 GESTIÓN DE ARCHIVOS ---

@cli.command()
@click.argument("pdb_id")
def fetch(pdb_id):
    """Download a PDB file by ID"""
    fetch_pdb(pdb_id)

@cli.command()
@click.argument("filename")
def stats(filename):
    """Show structure statistics (atoms, residues, etc.)"""
    parse_pdb(filename)

@cli.command()
@click.argument("pdb_id")
def meta(pdb_id):
    """Show basic metadata for a PDB ID"""
    pdb_data = fetch_pdb(pdb_id)
    if pdb_data:
        meta_data = metadata.extract_metadata(pdb_data)
        metadata.print_metadata(meta_data, pdb_id)

# --- 🧬 ANÁLISIS DE SECUENCIA ---

@cli.command("count-amino-acids")
@click.argument("pdb_id")
@click.option("--plot", is_flag=True, help="Show bar chart of amino acid counts")
def count_amino_acids(pdb_id, plot):
    """Count amino acids for a PDB ID (chain A)"""
    pdb_data = fetch_pdb(pdb_id)
    if pdb_data:
        sequence = amino_acids.parse_chain_sequence(pdb_data)
        counts = amino_acids.count_amino_acids(sequence)
        click.echo(f"\nAmino acid counts for {pdb_id}:\n")
        for aa, count in sorted(counts.items()):
            click.echo(f"{aa}: {count}")
        if plot:
            amino_acids.plot_amino_acid_counts(counts, f"Amino Acid Counts for {pdb_id}")

@cli.command()
@click.argument("pdb_id")
def sequence(pdb_id):
    """Show amino acid sequences for all chains of a PDB ID"""
    pdb_data = fetch_pdb(pdb_id)
    if not pdb_data: 
        return
    try:
        chains = amino_acids.parse_chain_sequences(pdb_data)
        amino_acids.print_sequences(chains)
    except Exception as e:
        click.echo(f"❌ Error extracting sequence: {e}")

# --- 📊 VISUALIZACIÓN ---

@cli.command()
@click.argument('pdb_id')
def ssvis(pdb_id):
    """Visualize secondary structure (1D ASCII) for a given PDB ID."""
    pdb_data = fetch_pdb(pdb_id)
    if not pdb_data:
        click.secho(f"❌ Failed to fetch data for {pdb_id}", fg='red')
        return

    pdb_lines = pdb_data.splitlines()
    structure_map = parse_secondary_structure(pdb_lines)
    # Usa la función unificada de amino_acids.py
    sequences = amino_acids.extract_sequences(pdb_lines)

    for chain_id, (seq, residue_ids) in sequences.items():
        click.echo(f"\n===== Chain {chain_id} =====")
        struct_line = structure_to_ascii(residue_ids, structure_map.get(chain_id, {}))
        output = format_structure_output(seq, struct_line)
        click.echo(output)
    click.echo("\nLegend: H = Helix, E = Beta sheet, - = Loop/Other")

@cli.command()
@click.argument("pdb_id")
@click.option("--chain", default=None, help="Filter by chain (e.g., A)")
@click.option("--steps", default=100, help="Number of animation frames")
def view3d(pdb_id, chain, steps):
    """3D ASCII Animation of the protein backbone (CA-trace)"""
    pdb_data = fetch_pdb(pdb_id)
    if not pdb_data: 
        return

    # Limpiar pantalla y ocultar cursor
    sys.stdout.write("\033[2J\033[?25l") 
    try:
        animate_structure(pdb_data.splitlines(), steps=steps, chain_filter=chain)
    finally:
        # Asegurar que el cursor vuelva a aparecer siempre
        sys.stdout.write("\033[?25h\n")

# --- 💡 INTELIGENCIA ARTIFICIAL ---

@cli.command()
@click.argument("filename")
@click.option("--model", default="llama3.2", help="Ollama model to use")
def summary(filename, model):
    """Generate LLM-based summary of the protein structure"""
    generate_summary(filename, model)

if __name__ == "__main__":
    cli()

##LLM and visualization blocks
''' 
# 💡 LLM summary of the structure
@cli.command()
@click.argument("filename")
def summary(filename):
    """Generate LLM-based summary"""
    generate_summary(filename)

# 🔎 Open structure viewer
@cli.command()
@click.argument("filename")
def visualize(filename):
    """Visualize the PDB structure in the browser"""
    launch_viewer(filename)
@cli.command()
@click.argument("filename")
@click.option("--model", default="llama3.2", help="Ollama model to use")
def summarize(filename, model):
    """Summarize a local PDB file with LLM help"""
    generate_summary(filename, model)


'''    