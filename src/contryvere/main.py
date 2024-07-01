import os
import json
import random
import re
from contextlib import suppress
from datetime import datetime as dt
from pathlib import Path

import pandas as pd
import vypyr
from vypyr.src.medulla.main import *
from vypyr.src.medulla.main import div

# ENVIRONMENT
VYPYR_DIR = Path(os.getenv("VYPYR_DIR"))

# UTILITIES
def get_spellbook_from_json() -> dict:
    p = VYPYR_DIR / "src/contryvere/spells.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_items_from_json() -> dict:
    p = VYPYR_DIR / "src/contryvere/items.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def spelld(spell: str) -> str:
    i = spell_indices[spell]
    name = SPELLBOOK[i].get("Name")
    lvl = SPELLBOOK[i].get("Level")
    time = SPELLBOOK[i].get("Casting Time")
    dur = SPELLBOOK[i].get("Duration")
    rng = SPELLBOOK[i].get("Range")
    desc = SPELLBOOK[i].get("Text")
    higher_lvl = SPELLBOOK[i].get("At Higher Levels")

    d = f"""
Name: {name}
Level: {lvl}
Casting Time: {time}
Duration: {dur}
Range: {rng}

--

{desc}

--

At Higher Levels: {higher_lvl}
"""
    return d

def itemd(item: str) -> str:
    i = item_indices[item]
    name = ITEMSLIST[i].get("Name")
    typ = ITEMSLIST[i].get("Type")
    rarity = ITEMSLIST[i].get("Rarity")
    attunement = ITEMSLIST[i].get("Attunement")
    props = ITEMSLIST[i].get("Properties")
    desc = ITEMSLIST[i].get("Text")
    weight = ITEMSLIST[i].get("Weight")
    val = ITEMSLIST[i].get("Value")

    d = f"""
Name: {name}
Type: {typ}
Rarity: {rarity}
Attunement: {attunement}
Properties: {props}
Weight: {weight}
Value: {val}

--

{desc}
"""
    return d


"""
Loading databases
"""
# Loading spellbook database
try:
    SPELLBOOK = get_spellbook_from_json()
    print(f"{PEACH}", end="")
    div()
    typyr("Successfully loaded spellbook database from `spells.json`.")
    spell_indices = {}
    for index, spell in enumerate(SPELLBOOK):
        spell_indices[spell['Name']] = index

except FileNotFoundError:
    print(f"{PEACH}", end="")
    div()
    typyr(f"""
{GOLDENROD}{BOLD}Contryvere{NORM}{TEAL} could not find `spells.json` 
in the current working directory.
""")
    pass
except Exception as e:
    raise e

# Loading items list database
try:
    ITEMSLIST = get_items_from_json()
    print(f"{PEACH}", end="")
    div()
    typyr("Successfully loaded items list database from `items.json`.")
    item_indices = {}
    for index, item in enumerate(ITEMSLIST):
        item_indices[item['Name']] = index
except FileNotFoundError:
    print(f"{PEACH}", end="")
    div()
    typyr(f"""
{GOLDENROD}{BOLD}Contryvere{NORM}{TEAL} could not find `items.json` 
in the current working directory.
""")
    pass
except Exception as e:
    raise e



class Persona:
    def __init__(self, god, **kwargs):
        self.god = god
        self.date = kwargs.get('date', dt.now().strftime('%A, %B %d %Y %H:%M:%S'))
        self.name = kwargs.get('name', str()).upper()
        self.age = kwargs.get('age', 0)
        self.race = kwargs.get('race', str()).capitalize()
        self.charclass = kwargs.get('charclass', str()).capitalize()
        self.level = kwargs.get('level', 1)
        self.alignment = kwargs.get('alignment', str()).capitalize()
        self.id = kwargs.get('id', random.randint(1000000000, 9999999999))
        self.universe = kwargs.get('universe', str()).capitalize()
        self.xp = kwargs.get('xp', 0)
        self.health = kwargs.get('health', 10)
        self.max_health = kwargs.get('max_health', 10)
        self.energy = kwargs.get('energy', 10)
        self.occupation = kwargs.get('occupation', str()).capitalize()
        self.diseases = [self.god.get_disease(name) for name in (kwargs.get('diseases') or [])]
        self.god.register(self)
        self.conversations = kwargs.get('conversations', {'sent': [], 'received': []})
        self.sent = self.conversations['sent']
        self.received = self.conversations['received']
        self.comments = kwargs.get('comments', [])

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        setattr(self, key, value)

class Roster:
    def __init__(self, god):
        self.roster = {}
        self.god = god

    def build(self):
        path = VYPYR_DIR / 'src/contryvere/characters'
        with suppress(OSError), os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.json'):
                    with open(entry.path, 'r') as file:
                        data = json.load(file)
                        if 'name' in data:
                            persona = Persona(god=self.god, **data)
                            self.roster[data['name']] = persona
                        else:
                            typyr(f"No 'name' key in {entry.name}; skipping...")

    def __getitem__(self, name):
        return self.roster.get(name)

    def __str__(self):
        return str(self.roster)

class God:
    def __init__(self):
        self.personas = []
        self.diseases = {}
        self.inventories = {}
        self.spellbooks = {}
        self.outdir = Path("~/repos/contryvere-site").expanduser()
        if not self.outdir.exists():
            self.outdir.mkdir(parents=True, exist_ok=True)
        self.ext = ".md"
        self.outname = Path("report")
        self.outpath = self.outdir / self.outname.with_suffix(self.ext)
        if not self.outpath.is_file():
            self.outpath.touch()
            
    def report(self):
        fp_md = self.outdir / self.outname.with_suffix(".md")
        fp_html = self.outdir / self.outname.with_suffix(".html")
        dateline = dt.now().strftime("Report generated at %H:%M:%S on %B %d, %Y.")
        stylesheet_path = "styles.css"
    
        # Profiles
        profiles_md = [dateline, "\n\n# `CONTRYVERE`\n\n----\n\n## PROFILES\n\n"]
        profiles_html = self.cl.reset_index().to_html(index=False, escape=False, classes='highlight')
        
        cl_df = self.cl
        profiles_md.append(cl_df.to_markdown(tablefmt="grid"))
    
        # Inventories
        inventories_md = ["\n\n## Inventories\n\n"]
        inventories_html = ["<p class='paragraph'>The information displayed below is current as of the date and time indicated at the top of the page.</p>"]
    
        for persona in self.personas:
            persona_inventory = self.inventories.get(persona.name, Inventory()).items
            inventories_md.append(f"\n\n### {persona.name}\n\n")
            if persona_inventory:
                inventory_data = []
                for item, details in persona_inventory.items():
                    inventory_data.append({
                        'Item': item,
                        'Description': details['description'].replace('\n', '<br>'),
                        'Quantity': details['quantity']
                    })
                df = pd.DataFrame(inventory_data)
                inventories_md.append(df.to_markdown(tablefmt="grid"))
                inventories_html.append(f"<h4>{persona.name}</h4>")
                inventories_html.append(df.to_html(index=False, escape=False, classes='highlight'))
            else:
                inventories_md.append(f"{persona.name}'s inventory is empty")
                inventories_html.append(f"<h4>{persona.name}</h4><p>{persona.name}'s inventory is empty</p>")
    
        # Spellbooks
        spellbooks_md = ["\n\n## Spellbooks\n\n"]
        spellbooks_html = ["<p class='paragraph'>The information displayed below is current as of the date and time indicated at the top of the page.</p>"]
    
        for persona in self.personas:
            persona_spellbook = self.spellbooks.get(persona.name, Spellbook()).spells
            spellbooks_md.append(f"\n\n### {persona.name}\n\n")
            if persona_spellbook:
                spellbook_data = [{'Spell': spell, 'Description': description.replace('\n', '<br>')} 
                                  for spell, description in persona_spellbook.items()]
                df = pd.DataFrame(spellbook_data)
                spellbooks_md.append(df.to_markdown(tablefmt="grid"))
                spellbooks_html.append(f"<h4>{persona.name}</h4>")
                spellbooks_html.append(df.to_html(index=False, escape=False, classes='highlight'))
            else:
                spellbooks_md.append(f"{persona.name}'s spellbook is empty")
                spellbooks_html.append(f"<h4>{persona.name}</h4><p>{persona.name}'s spellbook is empty</p>")
    
        # Combine content for markdown
        content_md = "".join(profiles_md) + "".join(inventories_md) + "".join(spellbooks_md) + "\n\n----\n\nEOF"
    
        # Combine content for HTML
        content_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contryvere | Reports</title>
    <!-- CSS -->
    <link rel="stylesheet" href="styles.css">
    <!-- Standard favicon -->
    <link rel="icon" href="favicon.png">
    <!-- Apple Touch Icon (recommended size) -->
    <link rel="apple-touch-icon" sizes="180x180" href="iOS/contryvere.appiconset/contryvere-60@3x.png">
    <!-- Additional Sizes -->
    <link rel="apple-touch-icon" sizes="120x120" href="iOS/contryvere.appiconset/contryvere-60@2x.png">
    <link rel="apple-touch-icon" sizes="152x152" href="iOS/contryvere.appiconset/contryvere-76@2x.png">
    <link rel="apple-touch-icon" sizes="167x167" href="iOS/contryvere.appiconset/contryvere-83.5@2x.png">
</head>
<body>
    <div class="container">
        <h6>{dateline}</h6>
        <a href="index.html" style="text-decoration: none">
            <div class="popbox">
                <h1><span style="font-weight: bolder;">CONTRYVERE</span><br />
                    Character Reports
                </h1>
            </div>
        </a>
        
        <button class="toggle-button" onclick="toggleVisibility('profiles', this)">
            <span class="icon">+ &nbsp;</span><span style='font-family: "Monaspace Krypton", "Menlo", "Courier New", Courier, monospace;'>Profiles</span>
        </button>
        <div id="profiles" class="toggle-content">
            <section>
                <h3>Roster</h3>
                <div class="table-bg">
                    {profiles_html}
                </div>
            </section>
        </div>

        <button class="toggle-button" onclick="toggleVisibility('inventories', this)">
            <span class="icon">+ &nbsp;</span><span style='font-family: "Monaspace Krypton", "Menlo", "Courier New", Courier, monospace;'>Inventories</span>
        </button>
        <div id="inventories" class="toggle-content">
            <section>
                <h3>Inventory Details by Character</h3>
                <div class="table-bg">
                    {''.join(inventories_html)}
                </div>
            </section>
        </div>

        <button class="toggle-button" onclick="toggleVisibility('spellbooks', this)">
            <span class="icon">+ &nbsp;</span><span style='font-family: "Monaspace Krypton", "Menlo", "Courier New", Courier, monospace;'>Spellbooks</span>
        </button>
        <div id="spellbooks" class="toggle-content">
            <section>
                <h3>Spellbook Lists by Character</h3>
                <div class="table-bg">
                    {''.join(spellbooks_html)}
                </div>
            </section>
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var allContents = document.querySelectorAll('.toggle-content');
            allContents.forEach(function(content) {{
                content.style.maxHeight = "0px"; // Initializes as collapsed
            }});
        }});
        function toggleVisibility(id, button) {{
            var content = document.getElementById(id);
            var icon = button.querySelector('.icon');
        
            if (content.style.maxHeight !== "0px" && content.style.maxHeight !== "") {{
                content.style.maxHeight = "0px";
                icon.textContent = '+ \\u00A0';
            }} else {{
                // Dynamically adjust max-height to the scrollHeight of the content
                content.style.maxHeight = content.scrollHeight + "px";
                icon.textContent = '- \\u00A0';
            }}
        }}
    </script>
</body>
</html>"""
    
        # Write markdown file
        with open(fp_md, "w") as f_md:
            f_md.write(content_md)
    
        # Write HTML file
        with open(fp_html, "w") as f_html:
            f_html.write(content_html)
    
        print("\n")
        typyr(f"{PEACH}Done.{NORM}")
        typyr(f"{PEACH}{BOLD}Wrote persona report to `{fp_md}` and `{fp_html}`:{NORM}")
        print("\n" * 2)
    
        with open(fp_md, "r") as f_md:
            data_md = f_md.read()
            print(f"{PEACH}{data_md}{NORM}")
    
        with open(fp_html, "r") as f_html:
            data_html = f_html.read()
            print(f"{PEACH}{data_html}{NORM}")    
    
    def open_inventory(self, persona):
        if persona.name in self.inventories:
            typyr(f"{persona.name}'s inventory is already open.")
        else:
            self.inventories[persona.name] = Inventory()
            try:
                with open(f'{VYPYR_DIR}/src/contryvere/characters/{persona.name}.json', 'r') as f:
                    data = json.load(f)
                    inv = data.get('inventory', {})
                    if isinstance(inv, dict):
                        for key, value in inv.items():
                            self.inventories[persona.name].items.update({f"{key}": {"description": value['description'], "quantity": value['quantity']}})
                    else:
                        typyr(f"Invalid inventory format for {persona.name}.")
            except KeyError:
                typyr(f"God instantiated a new inventory for {persona.name}, who has not yet acquired any items.")

    def open_spellbook(self, persona):
        if persona.name in self.spellbooks:
            typyr(f"{persona.name}'s spellbook is already open.")
        else:
            self.spellbooks[persona.name] = Spellbook()
            try:
                with open(f'{VYPYR_DIR}/src/contryvere/characters/{persona.name}.json', 'r') as f:
                    data = json.load(f)
                    spells = data.get('spellbook', {})
                    if isinstance(spells, dict):
                        for key, value in spells.items():
                            self.spellbooks[persona.name].spells.update({f"{key}": value})
                    else:
                        typyr(f"Invalid spellbook format for {persona.name}.")
            except KeyError:
                typyr(f"God instantiated a new spellbook for {persona.name}, who has not yet acquired any spells.")

    def export(self, persona):
        """Export a single persona's data to a JSON file."""
        inventory_items = self.inventories.get(persona.name, Inventory()).items
        spells = self.spellbooks.get(persona.name, Spellbook()).spells

        data = {
            'date': persona.date,
            'name': persona.name,
            'age': persona.age,
            'race': persona.race,
            'charclass': persona.charclass,
            'level': persona.level,
            'alignment': persona.alignment,
            'id': persona.id,
            'universe': persona.universe,
            'xp': persona.xp,
            'health': persona.health,
            'max_health': persona.max_health,
            'energy': persona.energy,
            'diseases': [d.name for d in persona.diseases if d],
            'conversations': persona.conversations,
            'inventory': inventory_items,
            'spellbook': spells
        }

        directory = VYPYR_DIR / 'src/contryvere/characters'
        os.makedirs(directory, exist_ok=True)
        file_path = directory / f'{persona.name}.json'
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Exported {persona.name}'s data to {file_path}.")

    def export_all(self):
        """Export data for all registered personas to JSON files."""
        for persona in self.personas:
            self.export(persona)

    @property
    def cl(self):
        names_list = []
        ages_list = []
        races_list = []
        universes_list = []
        occupations_list = []
        levels_list = []
        classes_list = []
        hp_list = []
        max_hp_list = []
        diseases_list = []
        alignments_list = []
        ids_list = []

        for persona in self.personas:
            names_list.append(persona.name)
            ages_list.append(persona.age)
            alignments_list.append(persona.alignment)
            races_list.append(persona.race)
            universes_list.append(persona.universe)
            occupations_list.append(persona.occupation)
            levels_list.append(persona.level)
            classes_list.append(persona.charclass)
            hp_list.append(persona.health)
            max_hp_list.append(persona.max_health)
            diseases_list.append(', '.join([d.name for d in persona.diseases]))
            ids_list.append(persona.id)

        cl = pd.DataFrame({
            "Name": names_list,
            "ID": ids_list,
            "Age": ages_list,
            "Alignment": alignments_list,
            "Race": races_list,
            "Universe": universes_list,
            "Occupation": occupations_list,
            "Level": levels_list,
            "Class": classes_list,
            "Disease(s)": diseases_list,
            "HP": hp_list,
            "Max HP": max_hp_list
        })

        cl = cl.set_index(["Name"])
        cl = cl.sort_values(by=["Name"], ascending=True)
        return cl

    def get_disease(self, name):
        return self.diseases.get(name)

    def register(self, persona):
        self.personas.append(persona)

    def add_item(self, persona_name, item, description, quantity=1):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.inventories:
            cleaned_description = "\n".join(line.strip() for line in description.strip().split("\n"))
            if item in self.inventories[persona_name].items:
                self.inventories[persona_name].items[item]['quantity'] += quantity
                self.inventories[persona_name].items[item]['description'] = cleaned_description
            else:
                self.inventories[persona_name].items[item] = {'description': cleaned_description, 'quantity': quantity}
            typyr(f"Added {quantity} x {item} to {persona_name}'s inventory.")
        else:
            typyr(f"No inventory found for {persona_name}.")

    def remove_item(self, persona_name, item, quantity=1):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.inventories:
            if item in self.inventories[persona_name].items:
                if self.inventories[persona_name].items[item]['quantity'] > quantity:
                    self.inventories[persona_name].items[item]['quantity'] -= quantity
                    typyr(f"Removed {quantity} x {item} from {persona_name}'s inventory.")
                elif self.inventories[persona_name].items[item]['quantity'] == quantity:
                    del self.inventories[persona_name].items[item]
                    typyr(f"Removed {item} from {persona_name}'s inventory.")
                else:
                    typyr(f"Cannot remove {quantity} x {item}; only {self.inventories[persona_name].items[item]['quantity']} in inventory.")
            else:
                typyr(f"{item} not found in {persona_name}'s inventory.")
        else:
            typyr(f"No inventory found for {persona_name}.")

    def add_spell(self, persona_name, spell, description):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.spellbooks:
            if spell not in self.spellbooks[persona_name].spells:
                cleaned_description = "\n".join(line.strip() for line in description.strip().split("\n"))
                self.spellbooks[persona_name].spells[spell] = cleaned_description
                typyr(f"Added {spell} to {persona_name}'s spellbook.")
            else:
                typyr(f"{spell} already in {persona_name}'s spellbook.")
        else:
            typyr(f"No spellbook found for {persona_name}.")

    def remove_spell(self, persona_name, spell):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.spellbooks:
            if spell in self.spellbooks[persona_name].spells:
                del self.spellbooks[persona_name].spells[spell]
                typyr(f"Removed {spell} from {persona_name}'s spellbook.")
            else:
                typyr(f"{spell} not found in {persona_name}'s spellbook.")
        else:
            typyr(f"No spellbook found for {persona_name}.")

    def list_inventory(self, persona_name):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.inventories:
            print(f"{GOLDENROD}{BOLD}[{persona_name}'S INVENTORY]{NORM}")
            for item, details in self.inventories[persona_name].items.items():
                print(f"{TEAL}Item: {item}{NORM}")
                print(f"> {PEACH}Description:{NORM}")
                for line in details['description'].split('\n'):
                    print(f"  {PEACH}{line}{NORM}")
                print(f"> {PEACH}Quantity: {details['quantity']}{NORM}\n")
        else:
            typyr(f"No inventory found for {persona_name}.")

    def list_spellbook(self, persona_name):
        if isinstance(persona_name, Persona):
            persona_name = persona_name.name
        if persona_name in self.spellbooks:
            typyr(f"{TEAL}{BOLD}[{persona_name}'S SPELLBOOK]{NORM}")
            for spell, description in self.spellbooks[persona_name].spells.items():
                print(f"{TEAL}Spell: {spell}{NORM}")
                print(f"> {PEACH}Description:{NORM}")
                for line in description.split("\n"):
                    print(f"  {PEACH}{line}{NORM}")
                print()
        else:
            typyr(f"No spellbook found for {persona_name}.")


class Inventory:
    def __init__(self):
        self.items = {}

class Spellbook:
    def __init__(self):
        self.spells = {}

def initialize():
    dm = God()
    roster = Roster(dm)
    roster.build()
    print(PEACH, end="", flush=True)
    div()
    data_path = VYPYR_DIR / "src/contryvere/characters"
    typyr(f"{PEACH}Your {BOLD}Contryvere{NORM}{PEACH} personas have been")
    typyr(f"{PEACH}reconstructed from the character data files saved in")
    typyr(f"{PEACH}`{data_path}`.\n\n")
    typyr(f"{PEACH}You can access this data via the {NORM}{BOLD}`dm.cl`{NORM}{PEACH} property.")
    typyr(f"{PEACH}For additional information, type `help(dm.cl)`.")

    div()
    print(NORM)

    return dm

# Initialize the manager and build the roster
dm = initialize()

# Open inventories and spellbooks for all personas
for persona in dm.personas:
    dm.open_inventory(persona)
    dm.open_spellbook(persona)
print(PEACH, end="", flush=True)
typyr(f"{BOLD}Opened {dm.personas.__len__()} personas' {GOLDENROD}inventories{PEACH} and {TEAL}spellbooks.{NORM}{PEACH}✨🎒🪄\n\n")
typyr(f"Indices:\n")
for c in range(len(dm.personas)):
    typyr(f"{[c]}  {dm.personas[c]['name']}")
