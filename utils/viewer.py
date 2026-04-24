import os
import webbrowser
from pathlib import Path
import shutil

def launch_viewer(pdb_path):
    filename = Path(pdb_path).name
    temp_dir = Path("viewer_tmp")
    temp_dir.mkdir(exist_ok=True)

    html_path = temp_dir / "index.html"
    shutil.copy(pdb_path, temp_dir / filename)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Mol* Viewer</title>
      <script src="https://cdn.jsdelivr.net/npm/molstar/build/viewer/molstar.js"></script>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/molstar/build/viewer/molstar.css" />
      <style>html, body {{ margin:0; height:100%; }}</style>
    </head>
    <body>
      <div id="app" style="width:100%; height:100%;"></div>
      <script>
        const viewer = new MolStarViewer("app");
        viewer.loadStructureFromUrl('{filename}', 'pdb');
      </script>
    </body>
    </html>
    """

    with open(html_path, "w") as f:
        f.write(html)

    print("📂 To view the structure, run the following in terminal:")
    print(f"cd {temp_dir.resolve()} && python3 -m http.server")
    print("Then open your browser and go to: http://localhost:8000")

    try:
        webbrowser.open("http://localhost:8000")
    except:
        print("🌐 Could not open browser automatically.")
