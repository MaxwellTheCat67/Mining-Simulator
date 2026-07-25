import builtins as _builtins
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from collections import Counter
import random

Tk = tk.Tk
Toplevel = tk.Toplevel
Label = tk.Label
StringVar = tk.StringVar
Frame = tk.Frame
X = tk.X
PhotoImage = tk.PhotoImage
Button = tk.Button

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except _builtins.ModuleNotFoundError:
    PIL_AVAILABLE = False

win = Tk()
win.title("Mine All The Way")
win.geometry("760x620")
win.minsize(760, 620)

mine_click_count = 0
mine_counter_text = StringVar(value="Mine Clicks: 0")
mine_loot_text = StringVar(value="Latest Loot: None")

def loot_showcase():
    loot = Toplevel(win)
    loot.title("Possible Loot")

    z = 1
    for i in cave_blocks:
        Label(loot,text=i).grid(row=z,column=1)
        z+=1
    a = 1
    for i in block_find_chance_percent:
        Label(loot,text=i).grid(row=a,column=2)
        a+=1
    x = 1
    for i in cave_blocks2:
        Label(loot,text=i).grid(row=x,column=3)
        x+=1
    y = 1
    for i in block_find_chance_percent2:
        Label(loot,text=i).grid(row=y,column=4)
        y+=1

    close_row = max(len(cave_blocks), len(block_find_chance_percent), len(cave_blocks2), len(block_find_chance_percent2)) + 2
    Button(loot, text="Close", command=loot.destroy, width=12).grid(row=close_row, column=1, columnspan=4, pady=10)

def direction():
    direction = Toplevel(win)
    Label(direction,text="Welcome to the Mining Simulator! Your goal is to collect valuable loot, earn \n experience, and improve your mining abilities. Use the XP button to gain experience \npoints (XP), which help you progress and unlock new opportunities. Click the \nEnchant button to spend your resources upgrading your Luck, increasing your \nchances of finding rarer and more valuable loot. When you're ready to search for \ntreasure, press the Mine button to dig into the mine and receive random loot,\n ranging from common materials to legendary treasures. Keep earning XP, upgrading \nyour Luck, and mining to discover the rarest rewards and become the ultimate \nminer!").pack()
    Button(direction, text="Close", command=direction.destroy, width=12).pack(pady=(0, 12))


def increment_loot_count(item_name, amount=1):
    key_overrides = {
        "lapis lazuli ore": "lapis_ore",
        "deepslate lapis lazuli ore": "deepslate_lapis_ore",
    }

    variable_name = key_overrides.get(item_name.lower(), item_name.lower().replace(" ", "_"))

    if variable_name in _builtins.globals() and _builtins.isinstance(_builtins.globals()[variable_name], _builtins.int):
        _builtins.globals()[variable_name] += max(1, amount)
        return variable_name, _builtins.globals()[variable_name]

    return variable_name, None


def get_loot_total(item_name):
    key_overrides = {
        "lapis lazuli ore": "lapis_ore",
        "deepslate lapis lazuli ore": "deepslate_lapis_ore",
    }

    variable_name = key_overrides.get(item_name.lower(), item_name.lower().replace(" ", "_"))
    value = _builtins.globals().get(variable_name, 0)

    if _builtins.isinstance(value, _builtins.int):
        return value

    return 0


def pick_loot_with_enchant():
    if luck_level <= 0:
        return random.choice(cave_blocks_for_rarity)

    frequency_by_item = Counter(cave_blocks_for_rarity)
    attempts = min(1 + luck_level * 2, 12)
    selected = random.choice(cave_blocks_for_rarity)

    for _ in range(attempts - 1):
        candidate = random.choice(cave_blocks_for_rarity)

        if frequency_by_item[candidate] < frequency_by_item[selected]:
            selected = candidate
        elif frequency_by_item[candidate] == frequency_by_item[selected] and random.random() < 0.5:
            selected = candidate

    return selected


def calculate_drop_amount(item_name):
    amount = 1

    if item_name.endswith("Ore") and fortune_level > 0:
        amount += random.randint(0, fortune_level)

    return amount


def mine_for_loot():
    global mine_click_count

    item_rolls = 1

    if efficiency_level >= 10:
        item_rolls = 10
    elif efficiency_level >= 5:
        item_rolls = 4
    elif efficiency_level >= 3:
        item_rolls = 2

    items_this_mine = []
    for _ in range(item_rolls):
        item = pick_loot_with_enchant()
        amount = calculate_drop_amount(item)
        variable_name, total = increment_loot_count(item, amount)

        if total is None:
            mine_loot_text.set(f"Latest Loot: {item} (missing var: {variable_name})")
            return

        items_this_mine.append(f"{item} (+{amount})")

    mine_click_count += 1
    mine_counter_text.set(f"Mine Clicks: {mine_click_count}")

    mine_loot_text.set(f"Latest Loot: {', '.join(items_this_mine)}")


def loot_gotten():
    loot2 = Toplevel(win)
    loot2.title("Inventory")
    loot2.geometry("900x650")

    container = tk.Frame(loot2)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    Label(scrollable_frame, text="cave_blocks", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(12, 6))
    Label(scrollable_frame, text="cave_blocks2", font=("Arial", 14, "bold")).grid(row=0, column=2, columnspan=2, padx=10, pady=(12, 6))
    Label(scrollable_frame, text="Loot", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=(0, 6), sticky="w")
    Label(scrollable_frame, text="Count", font=("Arial", 11, "bold")).grid(row=1, column=1, padx=10, pady=(0, 6), sticky="w")
    Label(scrollable_frame, text="Loot", font=("Arial", 11, "bold")).grid(row=1, column=2, padx=10, pady=(0, 6), sticky="w")
    Label(scrollable_frame, text="Count", font=("Arial", 11, "bold")).grid(row=1, column=3, padx=10, pady=(0, 6), sticky="w")

    for row, item in enumerate(cave_blocks, start=2):
        Label(scrollable_frame, text=item).grid(row=row, column=0, padx=10, pady=2, sticky="w")
        Label(scrollable_frame, text=f"({get_loot_total(item)})").grid(row=row, column=1, padx=10, pady=2, sticky="w")

    for row, item in enumerate(cave_blocks2, start=2):
        Label(scrollable_frame, text=item).grid(row=row, column=2, padx=10, pady=2, sticky="w")
        Label(scrollable_frame, text=f"({get_loot_total(item)})").grid(row=row, column=3, padx=10, pady=2, sticky="w")

    close_row = max(len(cave_blocks), len(cave_blocks2)) + 3
    Button(scrollable_frame, text="Close", command=loot2.destroy, width=12).grid(row=close_row, column=0, columnspan=4, pady=10)



def xp():
    global expierience_points
    expierience_points += 5
    xp_text.set(f"XP: {expierience_points}")


def buy_luck(level, cost, status_var):
    global expierience_points, enchant_level, luck_level

    if level > 1 and luck_level == 0:
        status_var.set("You need Luck 1 before buying higher Luck levels.")
        return

    if level == 10 and luck_level < 2:
        status_var.set("You need Luck 2 before buying Luck 10.")
        return

    if level == 10 and efficiency_level < 5:
        status_var.set("You need Efficiency 3 and Efficiency 5 before buying Luck 10.")
        return

    if luck_level >= level:
        status_var.set(f"Luck {level} already unlocked.")
        return

    if expierience_points < cost:
        status_var.set(f"Not enough XP for Luck {level} (need {cost}).")
        return

    expierience_points -= cost
    luck_level = level
    enchant_level += 1

    xp_text.set(f"XP: {expierience_points}")
    status_var.set(f"Applied Luck {level}. L:{luck_level} E:{efficiency_level} F:{fortune_level}")


def buy_efficiency(level, cost, status_var):
    global expierience_points, enchant_level, efficiency_level

    if level == 10:
        needed_luck = 10
    else:
        needed_luck = 1 if level == 3 else 2

    if luck_level < needed_luck:
        status_var.set(f"Need Luck {needed_luck} first for Efficiency {level}.")
        return

    if efficiency_level >= level:
        status_var.set(f"Efficiency {level} already unlocked.")
        return

    if expierience_points < cost:
        status_var.set(f"Not enough XP for Efficiency {level} (need {cost}).")
        return

    expierience_points -= cost
    efficiency_level = level
    enchant_level += 1
    xp_text.set(f"XP: {expierience_points}")
    status_var.set(f"Applied Efficiency {level}. L:{luck_level} E:{efficiency_level} F:{fortune_level}")


def buy_fortune(level, cost, status_var):
    global expierience_points, enchant_level, fortune_level

    if luck_level == 0:
        status_var.set("You need at least Luck 1 before buying Fortune.")
        return

    if fortune_level >= level:
        status_var.set(f"Fortune {level} already unlocked.")
        return

    if expierience_points < cost:
        status_var.set(f"Not enough XP for Fortune {level} (need {cost}).")
        return

    expierience_points -= cost
    fortune_level = level
    enchant_level += 1
    xp_text.set(f"XP: {expierience_points}")
    status_var.set(f"Applied Fortune {level}. L:{luck_level} E:{efficiency_level} F:{fortune_level}")


def enchant_table_gui():
    enchant_window = Toplevel(win)
    enchant_window.title("Enchant Table")
    enchant_window.geometry("560x480")

    status_text = StringVar(value=f"Levels -> L:{luck_level} E:{efficiency_level} F:{fortune_level}")

    Label(enchant_window, text="Enchant Table", font=("Arial", 20, "bold")).pack(pady=(12, 4))
    Label(enchant_window, textvariable=xp_text, font=("Arial", 11)).pack(pady=(0, 10))

    button_frame = Frame(enchant_window)
    button_frame.pack(pady=6)

    Button(
        button_frame,
        text="Luck I (500 XP)",
        width=16,
        command=lambda: buy_luck(1, 500, status_text),
    ).grid(row=0, column=0, padx=6, pady=6)

    Button(
        button_frame,
        text="Luck II (1000 XP)",
        width=16,
        command=lambda: buy_luck(2, 1000, status_text),
    ).grid(row=0, column=1, padx=6, pady=6)

    Button(
        button_frame,
        text="Efficiency 3 (250 XP)",
        width=16,
        command=lambda: buy_efficiency(3, 250, status_text),
    ).grid(row=1, column=0, padx=6, pady=6)

    Button(
        button_frame,
        text="Efficiency 5 (500 XP)",
        width=16,
        command=lambda: buy_efficiency(5, 500, status_text),
    ).grid(row=1, column=1, padx=6, pady=6)

    Button(
        button_frame,
        text="Efficiency 10 (1000000 XP)",
        width=34,
        command=lambda: buy_efficiency(10, 1000000, status_text),
    ).grid(row=2, column=0, columnspan=2, padx=6, pady=6)

    Button(
        button_frame,
        text="Fortune 1 (300 XP)",
        width=16,
        command=lambda: buy_fortune(1, 300, status_text),
    ).grid(row=3, column=0, padx=6, pady=6)

    Button(
        button_frame,
        text="Fortune 3 (500 XP)",
        width=16,
        command=lambda: buy_fortune(3, 500, status_text),
    ).grid(row=3, column=1, padx=6, pady=6)

    Button(
        button_frame,
        text="Luck 10 (1000000 XP)",
        width=34,
        command=lambda: buy_luck(10, 1000000, status_text),
    ).grid(row=4, column=0, columnspan=2, padx=6, pady=6)

    Label(
        enchant_window,
        text="Efficiency 3 gives 2 item rolls, Efficiency 5 gives 4 item rolls, and Efficiency 10 gives 10 item rolls. Luck 10 needs Efficiency 3 and 5. Efficiency 10 needs Luck 10. Fortune boosts ore amounts.",
        font=("Arial", 10),
        wraplength=520,
    ).pack(pady=(4, 0))
    Label(enchant_window, textvariable=status_text, font=("Arial", 11)).pack(pady=(10, 6))
    Button(enchant_window, text="Close", command=enchant_window.destroy, width=12).pack(pady=(0, 10))
    
cave_blocks = [
    "Stone",
    "Deepslate",
    "Tuff",
    "Calcite",
    "Dripstone Block",
    "Pointed Dripstone",
    "Granite",
    "Diorite",
    "Andesite",
    "Dirt",
    "Gravel",
    "Sand",
    "Clay",
    "Water",
    "Lava",
    "Coal Ore",
    "Deepslate Coal Ore",
    "Iron Ore",
    "Deepslate Iron Ore",
    "Copper Ore",
    "Deepslate Copper Ore",
    "Gold Ore",
    "Deepslate Gold Ore",
    "Redstone Ore",
    "Deepslate Redstone Ore",
    "Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Diamond Ore",
    "Deepslate Diamond Ore",
    "Emerald Ore",
    "Deepslate Emerald Ore",
    "Infested Stone",
    "Moss Block",
    "Moss Carpet",
    "Azalea",
    "Flowering Azalea",
    "Spore Blossom",
]

cave_blocks2 = [
    "Cave Vines",
    "Big Dripleaf",
    "Small Dripleaf",
    "Amethyst Block",
    "Budding Amethyst",
    "Amethyst Cluster",
    "Small Amethyst Bud",
    "Medium Amethyst Bud",
    "Large Amethyst Bud",
    "Smooth Basalt",
    "Basalt",
    "Sculk",
    "Sculk Vein",
    "Sculk Catalyst",
    "Sculk Sensor",
    "Sculk Shrieker",
    "Monster Spawner",
    "Cobweb",
    "Rail",
    "Chest",
    "Torch"
    ]

cave_blocks_for_rarity = [
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Stone",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Deepslate",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Tuff",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Calcite",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Dripstone Block",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Pointed Dripstone",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Granite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Diorite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Andesite",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Dirt",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Gravel",
    "Sand",
    "Clay",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Coal Ore",
    "Deepslate Coal Ore",
    "Iron Ore",
    "Deepslate Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Iron Ore",
    "Deepslate Iron Ore",
    "Deepslate Iron Ore",
    "Deepslate Iron Ore",
    "Deepslate Iron Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Copper Ore",
    "Deepslate Copper Ore",
    "Deepslate Copper Ore",
    "Deepslate Copper Ore",
    "Deepslate Copper Ore",
    "Deepslate Copper Ore",
    "Gold Ore",
    "Gold Ore",
    "Gold Ore",
    "Gold Ore",
    "Gold Ore",
    "Deepslate Gold Ore",
    "Deepslate Gold Ore",
    "Deepslate Gold Ore",
    "Deepslate Gold Ore",
    "Deepslate Gold Ore",
    "Redstone Ore",
    "Redstone Ore",
    "Redstone Ore",
    "Redstone Ore",
    "Redstone Ore",
    "Deepslate Redstone Ore",
    "Deepslate Redstone Ore",
    "Deepslate Redstone Ore",
    "Deepslate Redstone Ore",
    "Deepslate Redstone Ore",
    "Lapis Lazuli Ore",
    "Lapis Lazuli Ore",
    "Lapis Lazuli Ore",
    "Lapis Lazuli Ore",
    "Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Deepslate Lapis Lazuli Ore",
    "Diamond Ore",
    "Diamond Ore",
    "Deepslate Diamond Ore",
    "Deepslate Diamond Ore",
    "Deepslate Diamond Ore",
    "Emerald Ore",
    "Deepslate Emerald Ore",
    "Infested Stone",
    "Moss Block",
    "Moss Carpet",
    "Azalea",
    "Flowering Azalea",
    "Spore Blossom",
    "Cave Vines",
    "Big Dripleaf",
    "Small Dripleaf",
    "Amethyst Block",
    "Budding Amethyst",
    "Amethyst Cluster",
    "Small Amethyst Bud",
    "Medium Amethyst Bud",
    "Large Amethyst Bud",
    "Smooth Basalt",
    "Basalt",
    "Sculk",
    "Sculk Vein",
    "Sculk Catalyst",
    "Sculk Sensor",
    "Sculk Shrieker",
    "Monster Spawner",
    "Cobweb",
    "Rail",
    "Chest",
    "Torch"
]

stone = 0
deepslate = 0
tuff = 0
calcite = 0
dripstone_block = 0
pointed_dripstone = 0
granite = 0
diorite = 0
andesite = 0
dirt = 0
gravel = 0
sand = 0
clay = 0
water = 0
lava = 0
coal_ore = 0
deepslate_coal_ore = 0
iron_ore = 0
deepslate_iron_ore = 0
copper_ore = 0
deepslate_copper_ore = 0
gold_ore = 0
deepslate_gold_ore = 0
redstone_ore = 0
deepslate_redstone_ore = 0
lapis_ore = 0
deepslate_lapis_ore = 0
diamond_ore = 0
deepslate_diamond_ore = 0
emerald_ore = 0
deepslate_emerald_ore = 0
infested_stone = 0
moss_block = 0
moss_carpet = 0
azalea = 0
flowering_azalea = 0
spore_blossom = 0
cave_vines = 0
big_dripleaf = 0
small_dripleaf = 0
amethyst_block = 0
budding_amethyst = 0
amethyst_cluster = 0
small_amethyst_bud = 0
medium_amethyst_bud = 0
large_amethyst_bud = 0
smooth_basalt = 0
basalt = 0
sculk = 0
sculk_vein = 0
sculk_catalyst = 0
sculk_sensor = 0
sculk_shrieker = 0
monster_spawner = 0
cobweb = 0
rail = 0
chest = 0
torch = 0

block_find_chance_percent = [
    90.0, # Stone
    88.0, # Deepslate
    30.0, # Tuff
    14.0, # Calcite
    24.0, # Dripstone Block
    22.0, # Pointed Dripstone
    42.0, # Granite
    40.0, # Diorite
    41.0, # Andesite
    35.0, # Dirt
    45.0, # Gravel
    8.0, # Sand
    10.0, # Clay
    30.0, # Water
    20.0, # Lava
    34.0, # Coal Ore
    18.0, # Deepslate Coal Ore
    28.0, # Iron Ore
    16.0, # Deepslate Iron Ore
    24.0, # Copper Ore
    14.0, # Deepslate Copper Ore
    10.0, # Gold Ore
    6.0, # Deepslate Gold Ore
    12.0, # Redstone Ore
    7.0, # Deepslate Redstone Ore
    11.0, # Lapis Lazuli Ore
    6.0, # Deepslate Lapis Lazuli Ore
    4.0, # Diamond Ore
    2.5, # Deepslate Diamond Ore
    1.8, # Emerald Ore
    0.9, # Deepslate Emerald Ore
    1.2, # Infested Stone
    12.0, # Moss Block
    10.0, # Moss Carpet
    6.0, # Azalea
    4.0, # Flowering Azalea
    1.5, # Spore Blossom
]

block_find_chance_percent2 = [
    8.0, # Cave Vines
    5.0, # Big Dripleaf
    7.0, # Small Dripleaf
    3.0, # Amethyst Block
    0.5, # Budding Amethyst
    2.0, # Amethyst Cluster
    1.8, # Small Amethyst Bud
    1.5, # Medium Amethyst Bud
    1.2, # Large Amethyst Bud
    4.0, # Smooth Basalt
    6.0, # Basalt
    3.0, # Sculk
    2.8, # Sculk Vein
    0.7, # Sculk Catalyst
    0.6, # Sculk Sensor
    0.25, # Sculk Shrieker
    0.4, # Monster Spawner
    2.2, # Cobweb
    2.0, # Rail
    0.8, # Chest
    1.5 # Torch
]
expierience_points = 0
enchant_level = 0
luck_level = 0
efficiency_level = 0
fortune_level = 0
xp_text = StringVar(value="XP: 0")

frame = Frame()
frame.pack(fill=X)
title = Label(frame, text="Mine Sim", font=("Arial", 30))
title.pack(pady=10)

frame2 = Frame()
frame2.pack(pady=6)

actions_frame = Frame(win)
actions_frame.pack(pady=8)

base_path = Path(__file__).resolve().parent

if PIL_AVAILABLE:
    left_img = ImageTk.PhotoImage(Image.open(base_path / "h.jpg").resize((160, 160)))
    center_img = ImageTk.PhotoImage(Image.open(base_path / "mine_pickaxe.png").resize((160, 160)))
    right_img = ImageTk.PhotoImage(Image.open(base_path / "images.png").resize((160, 160)))
else:
    # Tkinter fallback: PNG works with PhotoImage, JPG requires Pillow.
    left_img = None
    center_img = PhotoImage(file=_builtins.str(base_path / "mine_pickaxe.png"))
    right_img = PhotoImage(file=_builtins.str(base_path / "images.png"))

left_button = Button(frame2, image=left_img, compound="top", width=160, height=160, command=xp)
left_button.grid(row=1, column=1, padx=8, pady=8)
xp_number = Label(frame2, textvariable=xp_text, font=("Arial", 11))
xp_number.grid(row=2, column=1, pady=(4, 0))

mine_button = Button(frame2, image=center_img, command=mine_for_loot)
mine_button.grid(row=1, column=2, padx=8, pady=8)

mine_counter_label = Label(frame2, textvariable=mine_counter_text, font=("Arial", 11))
mine_counter_label.grid(row=2, column=2, pady=(4, 0))

mine_loot_label = Label(frame2, textvariable=mine_loot_text, font=("Arial", 11), wraplength=220)
mine_loot_label.grid(row=3, column=2, pady=(2, 0))

right_button = Button(frame2, image=right_img, command=enchant_table_gui)
right_button.grid(row=1, column=3, padx=8, pady=8)

possible_loot = Button(actions_frame, text="POSSIBLE LOOT", command=loot_showcase, width=16)
possible_loot.grid(row=1, column=1, padx=12, pady=4)

directions = Button(actions_frame, text="DIRECTIONS", command=direction, width=16)
directions.grid(row=1, column=2, padx=12, pady=4)

inventory = Button(actions_frame, text="INVENTORY", command=loot_gotten, width=16)
inventory.grid(row=1, column=3, padx=12, pady=4)

close_app = Button(actions_frame, text="CLOSE", command=win.destroy, width=16)
close_app.grid(row=2, column=2, padx=12, pady=4)

win.mainloop()










































# 1000 lines :)
