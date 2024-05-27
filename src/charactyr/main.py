# main.py

try:
    import vypyr
    from vypyr.src.medulla.main import *
    div()
    # ENVIRONMENT VARIABLES
    VYPYR_DIR = os.environ.get('VYPYR_DIR')
    cwd = os.getcwd()
    if cwd == VYPYR_DIR:
        pass
    else:
        os.chdir(f'{VYPYR_DIR}/src')
except ImportError as e:
    print('ERROR:')
    print(f'        {e}')
finally:
    import datetime
    import json
    import numpy as np
    import os
    import pandas as pd
    import pathlib
    import random
    import sys
    from contextlib import suppress
    from datetime import datetime as dt
    from pathlib import Path
'''

C O N T R Y V E
(a character builder & manager)

'''


# Disease States
def reduce_health(persona):
    persona.health -= 10  # Reduce health by 10 points
    typyr(f"{persona.name} has lost 10 health due to illness.")


def decrease_energy(persona):
    if hasattr(persona, 'energy'):
        persona.energy -= 20  # Reduce energy by 20 points if energy attribute exists
        typyr(f"{persona.name}'s energy is reduced by 20 due to fatigue.")
    else:
        typyr(f"{persona.name} has no energy attribute to affect.")


class Persona:

    def __init__(self, god, **kwargs):
        self.god = god
        self.date = kwargs.get('date',
                               dt.now().strftime('%A, %B %d %Y %H:%M:%S'))
        self.name = kwargs.get('name', 'nameless').upper()
        self.age = kwargs.get('age', 21)
        self.species = kwargs.get('species', 'human').upper()
        self.ability = kwargs.get('ability', 'unknown').upper()
        self.level = kwargs.get('level', 0)
        self.type = kwargs.get('type', 'ambivalent').upper()
        self.id = kwargs.get('id', random.randint(1000000000, 9999999999))
        self.universe = kwargs.get('universe', 'unnamed universe').upper()
        self.xp = kwargs.get('xp', 0.00)
        self.health = kwargs.get('health', 100)
        self.energy = kwargs.get('energy', 100)
        self.diseases = [
            self.god.get_disease(name)
            for name in (kwargs.get('diseases') or [])
        ]
        self.god.register(self)
        self.conversations = kwargs.get('conversations', {'sent': [], 'received': []})
        self.sent = self.conversations['sent']
        self.received = self.conversations['received']

    def __getitem__(self, key):
        """Allow dictionary-like access to attributes."""
        return getattr(self, key,
                       None)  # Returns None if attribute doesn't exist

    def __setitem__(self, key, value):
        """Allow dictionary-like setting of attributes."""
        setattr(
            self, key, value
        )  # Sets the attribute if it exists or creates a new one if it doesn't

    def list_diseases(self):
        if not self.diseases:
            return f"{self.name} is currently healthy and has no diseases."
        return f"{self.name} is currently suffering from: " + ", ".join(
            [d.name for d in self.diseases if d])

    def summarize(self):
        clear()
        typyr(
            f'Name:                       {BOLD}{GOLDENROD}{self.name}{NORM}')
        typyr(f'Type:                       {BOLD}{BLUE}{self.type}{NORM}')
        typyr(f'Level:                      {BOLD}{CYAN}{self.level}{NORM}')
        typyr(f'XP:                         {BOLD}{PEACH}{self.xp}{NORM}')
        typyr(f'Health:                     {BOLD}{RED}{self.health}{NORM}')
        typyr(f'Energy:                     {BOLD}{BLUE}{self.energy}{NORM}')
        div()
        typyr(f'Afflictions:                {BOLD}{LIGHT_RED}' +
              ', '.join([d.name for d in self.diseases if d]) + f'{NORM}')
        div()
        typyr(f'Date of Instantiation:      {BOLD}{self.date}{NORM}')
        typyr(f'Identification Number:      {BOLD}{TEAL}{self.id}{NORM}')
        typyr(f'Age:                        {BOLD}{self.age}{NORM}')
        typyr(f'Species:                    {BOLD}{self.species}{NORM}')
        typyr(f'Ability:                    {BOLD}{self.ability}{NORM}')
        typyr(f'Universe:                   {BOLD}{self.universe}{NORM}')
        div()

    def speak(self, recipient, message):
        """Initiates sending a message through God."""
        self.god.mediate_speak(self, recipient, message)

    def attack(self, target, damage):
        """Initiates an attack through God."""
        self.god.mediate_attack(self, target, damage)


class Roster:

    def __init__(self, god):
        self.roster = {}  # Initialize as an empty dictionary
        self.god = god

    def build(self):
        path = f'{VYPYR_DIR}/src/charactyr/characters'
        with suppress(OSError), os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.json'):
                    with open(entry.path, 'r') as file:
                        data = json.load(file)
                        if 'name' in data:
                            persona = Persona(god=self.god, **data)
                            self.roster[data['name']] = persona
                        else:
                            typyr(
                                f"No 'name' key in {entry.name}; skipping...")

    def __getitem__(self, name):
        # Return Persona object directly
        return self.roster[name]

    def __str__(self):
        return str(self.roster)  # Optionally, for easier debugging


class God:

    def __init__(self):
        self.personas = []
        self.diseases = {}
        self.inventories = {}

    def list_personas(self):
        """Returns a list of all personas currently registered with God."""
        if not self.personas:
            return "No personas are currently registered."
        return "\n".join([
            f"{persona.name} - Level {persona.level}"
            for persona in self.personas
        ])

    def open_inventory(self, persona):
        div()
        if persona.name in self.inventories:
            typyr(f"{persona.name}'s inventory is already open.")
        else:
            typyr(f"Opening {persona.name}'s inventory...")
            self.inventories[persona.name] = Inventory()
            os.chdir(f"{VYPYR_DIR}/src/charactyr/characters")
            try:
                with open(f'{persona.name}.json', 'r') as f:
                    data = json.load(f)
                    inv = data['inventory']
                    for key, value in inv.items():
                        self.inventories[persona.name].items.update({f"{key}": f"{value}"})
                    typyr(f"Successfully loaded {persona.name}'s inventory from JSON.")
            except KeyError:
                typyr(
                    f"God instantiated a new inventory for {persona.name}, who has not yet acquired any items."
                    )
            finally:
                typyr(f"{BOLD}{GOLDENROD}{persona.name}'s inventory is now open.{NORM}")
                os.chdir('..')

    def close_inventory(self, persona):
        if persona.name in self.inventories:
            typyr(f"Closing {persona.name}'s inventory...")
            del self.inventories[persona.name]
        else:
            typyr(f"{persona.name}'s inventory is not open.")

    def inventory(self, persona):
        if persona.name in self.inventories:
            inventory = self.inventories[persona.name]
            if inventory.items:
                div()
                for item in inventory.items:
                    typyr(f"{BOLD}{GOLDENROD}[ {item} ]{NORM}\n> {inventory.items[item]}\n")
            else:
                typyr(f"{persona.name}'s inventory is empty.")
        else:
            typyr(f"{persona.name}'s inventory is not open.")

    def add_item_to_inventory(self, persona, item_name, description):
        """Add an item to a persona's inventory."""
        if persona.name in self.inventories:
            self.inventories[persona.name].add_item(item_name, description)
            print(f"Added {item_name} to {persona.name}'s inventory.")
        else:
            print(f"{persona.name} does not have an inventory opened.")

    def remove_item_from_inventory(self, persona, item_name):
        """Remove an item from a persona's inventory."""
        if persona.name in self.inventories:
            self.inventories[persona.name].remove_item(item_name)
        else:
            print(f"{persona.name} does not have an inventory opened.")

    def list_inventory(self, persona):
        """List all items in a persona's inventory."""
        if persona.name in self.inventories:
            items_list = self.inventories[persona.name].list_items()
            print(items_list)
        else:
            print(f"{persona.name} does not have an inventory opened.")

    def register(self, persona):
        """Register a persona with God."""
        self.personas.append(persona)

    def unregister(self, persona):
        """Unregister a persona from God's registry."""
        if persona in self.personas:
            self.personas.remove(persona)
            typyr(f"{persona.name} has been removed from the registry.")
        else:
            typyr(f"{persona.name} is not registered.")

    def register_disease(self, name, effect):
        """Register a new disease, if it doesn't already exist."""
        if name not in self.diseases:
            self.diseases[name] = Disease(name, effect)

    def get_disease(self, name):
        """Retrieve a disease by name."""
        return self.diseases.get(name)

    def afflict(self, persona, disease):
        """Infect a persona with a disease by name."""
        disease = self.get_disease(disease)
        if disease and persona:
            if disease not in persona.diseases:  # Correct way to check if the disease is not already in the list
                disease.apply(persona)
                persona.diseases.append(disease)
                typyr(
                    f"{persona.name} has been afflicted with {disease.name}.")
            else:
                typyr(
                    f"{persona.name} is already afflicted with {disease.name}."
                )
        else:
            typyr(
                f"Failed to afflict {persona.name} with {disease}: Disease not found."
            )

    def cure(self, persona, disease_input):
        """Cure a persona of a specific disease, either by name or by Disease instance."""
        disease = None
        if isinstance(disease_input, Disease):
            disease = disease_input
        elif isinstance(disease_input, str):
            disease = self.get_disease(disease_input)

        if disease and disease in persona.diseases:
            persona.diseases.remove(disease)
            typyr(f"{persona.name} has been cured of {disease.name}.")
        else:
            typyr(
                f"{persona.name} does not have the disease {disease.name} or the disease was not found."
            )

    def export(self, persona):
        """Export a single persona's data to a JSON file."""
        if persona.name in self.inventories:
            inventory_items = self.inventories[persona.name].items
        else:
            inventory_items = "Inventory not initialized."

        data = {
            'date': persona.date,
            'name': persona.name,
            'age': persona.age,
            'species': persona.species,
            'ability': persona.ability,
            'level': persona.level,
            'type': persona.type,
            'id': persona.id,
            'universe': persona.universe,
            'xp': persona.xp,
            'health': persona.health,
            'energy': persona.energy,
            'diseases': [d.name for d in persona.diseases if d],
            'conversations':
            persona.conversations,  # Include the conversations dict
            'inventory': inventory_items  # Include inventory details
        }

        directory = f'{VYPYR_DIR}/src/charactyr/characters'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f'{persona.name}.json')
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Exported {persona.name}'s data to {file_path}.")

    def export_all(self):
        """Export data for all registered personas to JSON files."""
        directory = f'{VYPYR_DIR}/src/charactyr/characters'
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        for persona in self.personas:
            self.export(persona)

    def mediate_speak(self, sender, recipient, message):
        """Mediates sending a message from one persona to another."""
        if recipient in self.personas:
            conversation = {
                'from': sender.name,
                'to': recipient.name,
                'date': dt.now().strftime('%Y-%m-%d %H:%M:%S'),
                'message': message
            }
            sender.conversations['sent'].append(conversation)
            recipient.conversations['received'].append(conversation)
            typyr(f"{sender.name} said to {recipient.name}: {message}")
        else:
            typyr(f"{recipient.name} is not registered in God's system.")

    def mediate_attack(self, attacker, target, damage):
        """Mediate an attack between two personas."""
        if target in self.personas:
            if target.health > 0:
                target.health -= damage
                typyr(
                    f"{attacker.name} attacks {target.name}, dealing {damage} damage."
                )
                if target.health <= 0:
                    target.health = 0
                    typyr(f"{target.name} has been defeated.")
            else:
                typyr(f"{target.name} is already defeated.")
        else:
            typyr(f"{target.name} is not registered in God's system.")

    def __getitem__(self, name):
        # Return Persona object directly
        return self.personas[name]

    def __str__(self):
        return str(self.personas)  # Optionally, for easier debugging


class Stats:

    @staticmethod
    def deal_damage(attacker, defender, damage):
        '''Apply damage from one persona to another and handle defeat.'''
        defender.health -= damage
        message = f'{BOLD}{GOLDENROD}{attacker.name}{NORM} dealt {BOLD}{ORANGE}{damage}{NORM} damage to {BOLD}{TEAL}{defender.name}{NORM}.'
        if defender.health <= 0:
            defender.health = 0
            message += f'\n{BOLD}{TEAL}{defender.name}{NORM} has been defeated.'
        return message

    @staticmethod
    def award_xp(character, xp):
        """Award experience points to a persona."""
        character.xp += xp
        return f"{BOLD}{GOLDENROD}{character.name}{NORM} received {BOLD}{LIGHT_GREEN}{xp}{NORM} XP."


class Disease:

    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  # This should be a callable that modifies a Persona

    def apply(self, persona):
        """Apply the disease effect to a persona."""
        self.effect(persona)


class Inventory:

    def __init__(self):
        self.items = {}

    def add_item(self, item_name, description):
        """Add an item to the inventory."""
        self.items[item_name] = description

    def remove_item(self, item_name):
        """Remove an item from the inventory."""
        if item_name in self.items:
            del self.items[item_name]

    def list_items(self):
        """Return a dictionary of all items in the inventory."""
        return self.items if self.items else "Inventory is empty."
