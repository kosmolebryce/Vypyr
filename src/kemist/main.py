import os
import sys
from pathlib import Path
from rdkit.Chem import Draw, MolFromSmiles, AllChem
import matplotlib.pyplot as plt
from PIL import Image
import io
import cairosvg

# CONSTANTS
HOME = Path.home().resolve()
WORKSPACES_DIR = HOME / 'workspaces'
VYPYR_DIR = WORKSPACES_DIR / 'vypyr'
SRC_DIR = VYPYR_DIR / 'src'
KEMIST_DIR = SRC_DIR / 'kemist'
KEMIST_IMG_DIR = Path('.').resolve() / 'images'

def typyr(message):
    print(message)  # Example function, replace with your actual typyr function implementation

def callback(event):
    typyr(f'Detected key press: {event.key}')  # Log the key-press event to the console
    typyr(f'    Exiting `kemist`...')
    if event.key in ['q', 'x', 'c', 'ctrl+c', 'ctrl+q', 'escape']:
        plt.close(event.canvas.figure)
    return

def main():
    if not os.path.exists(KEMIST_IMG_DIR):
        os.makedirs(KEMIST_IMG_DIR)
    os.chdir(KEMIST_IMG_DIR)

    # Loading the SMILES string        
    try:
        smiles = input("Enter the target SMILES string  -->  ")
        if smiles == "":
            sys.exit()
        else:
            mol = MolFromSmiles(smiles)
            AllChem.Compute2DCoords(mol)
            # Drawing the 3D structure
            fp = input("Save structure as ([input].svg) -->  ")
            options = Draw.DrawingOptions()
            options.wedgeDashedBonds = True
            options.wedgeDashedBondsWidth = 2.0
            options.bondLineWidth = 3.0  # Increasing overall bond line width
            options.atomLabelColor = (0, 0, 0, 1)  # RGBA for black, full opacity
            options.bondColorMap = {
                1: (0, 0, 0, 1),  # Map single bonds to black
                2: (0, 0, 0, 1),  # Map double bonds to black
                3: (0, 0, 0, 1)   # Map triple bonds to black
            }
            Draw.MolToFile(mol, f"{fp}.svg", size=(500, 500), options=options, imageType="svg")

            # Convert SVG to PNG using cairosvg for display
            with open(f"{fp}.svg", 'rb') as svg_file:
                svg = svg_file.read()
                png = cairosvg.svg2png(bytestring=svg)

            # Load the PNG into Matplotlib or IPython
            image = Image.open(io.BytesIO(png))
            typyr('Displaying with matplotlib...')
            fig, ax = plt.subplots()
            ax.imshow(image, interpolation='lanczos')
            ax.axis('off')
            title = f'{fp}'
            ax.set_title(title, color='black', fontsize=9)
            fig.canvas.mpl_connect('key_press_event', callback)
            plt.savefig(f"{fp}.png")  # Save the figure with the title as a part of the image
            plt.show()

    except Exception as e:
        typyr('Something went wrong...')
        typyr('Here\'s what Python had to say about it:      ')
        typyr(f'            {e}')

if __name__ == "__main__":
    main()
