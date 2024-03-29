# from sys import argv
import csv
from datetime import datetime
from decimal import Decimal
from rhinventory.app import create_app
from rhinventory.extensions import db
from rhinventory.db import Asset, AssetStatus, Category, CategoryTemplate, AssetMeta, Location, Transaction, TransactionType, log
# import json
from pprint import pprint


prep_file = {
    "categories": "./docs/categories.csv",
    "locations": "./docs/locations.csv",
    "category_templates": "./docs/category_templates.csv"
}
csv_file = {
    'game': './docs/GM.csv',
    'console': './docs/GC.csv',
    'console accesory': './docs/PP.csv',
    'other software': './docs/SW.csv',
    'keyboard': './docs/Kláv.csv',
    'computer mouse': './docs/Myš.csv',
    'television': './docs/TV.csv',
    'monitor': './docs/M.csv',

}


user_map = {
    "Morx": 2,
    "BlackChar": 4,
    "Blackie": 4,
    "BC?": 4,
    "Sanky": 5,
    "Scyther": 6,
    "scyther": 6,
    "Scyther?": 6,
    "Sczther": 6,
    "Behold3r": 7,
    "John Beak": 9,
    "Terrion": 10,
    "Arlette": 11,
    "Zdeněk": 103,
    "fiflik": 28,
    "František": 22,
    "Brambora": 56,
    "Buizel": 2,                     # vse od Buizela stejne domlouval morx
    '“Někdo to poslal Morxovi”': 2,  # wat
    "Retroherna": 6,                 # Scyther je RetroHerna
    "John Bleak Char": 4,            # facepalm



}

asset_titles = {
    "keyboard": "klávesnice",
    "computer mouse": "Myš",
    "television": "Televizor",
    "monitor": "Monitor",
}


# game_meta = {
#     "Platform": "Platforma",
#     "Medium": "Formát",
#     "Product No": "Písmena a čísla",
# }

# console_meta = {
# }

# mouse_meta = {
#     "Color": "Vzhled",
#     "Connection": "Typ",
#     "Type": "Styl",

# }

# keyboard_meta = {
#     "Color": "Vzhled",
#     "Connection": "Typ",
# }

# television_meta = {
#     "Size": "Úhlopříčka",

# }

# monitor_meta = {
#     "Size": "Úhlopříčka",
# }


def row_is_valid(row):
    if "Název" in row.keys():
        if row["Název"].strip() != '' and row["Název"].strip() != '-' and ('reserved' not in row["Název"].strip().lower()):
            return True
        else:
            return False
    elif "Typ" in row.keys():
        if row["Typ"].strip() != '':
            return True
        else:
            return False
    elif "Výrobce" in row.keys():
        if row["Výrobce"].strip() != '':
            return True
        else:
            return False
    else:
        return False


def add_meta(asset, skey, svalue):
    m = AssetMeta(
        key=skey,
        value=svalue
    )
    asset.metadata.append(m)


def coerce_int(value):  # F&&KIN PYTHON TO NEUMI NAPSAT NA JEDEN RADEK
    try:
        return int(value)
    except Exception:
        return None


def value_or_none(value):
    return value if value else None


app = create_app()
with app.app_context():
    db.create_all()

    exit()

   # CREATE LOCATIONS
    with open(prep_file["locations"], newline='') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            row = dict(zip(header, row))
            l = Location(
                name=row["name"],
                note=row["note"],
            )
            db.session.add(l)
        db.session.commit()

    # CREATE CATEGORIES
    with open(prep_file["categories"], newline='') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            row = dict(zip(header, row))
            c = Category(
                name=row["name"],
                prefix=row["prefix"],
                counter=row["counter"]
            )
            db.session.add(c)
        db.session.commit()

    # CREATE CATEGORY TEMPLATES
    with open(prep_file["category_templates"], newline='') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            row = dict(zip(header, row))
            cat = Category.query.filter(Category.name == row["category"]).one()
            ct = CategoryTemplate(
                category=cat,
                key=row["key"],
                value=row["value"],
            )
            db.session.add(ct)
        db.session.commit()

    for key in csv_file:
        with open(csv_file[key], newline='') as f:
            reader = csv.reader(f)
            cat = Category.query.filter(Category.name == key).one()
            pprint([key, csv_file[key], cat.prefix])
            header = next(reader)

            for row in reader:
                row = dict(zip(header, row))
                if row_is_valid(row):
                    # pprint(row)
                    title = row.get("Název",
                                    row.get("Typ", row.get("Technologie", "")).strip() + " " + asset_titles.get(key, "")).strip()

                    print(row["Inv. č."].strip() +
                          "\t- " + title + " :\t\t", end='')
                    asset = Asset(
                        category=cat,
                        name=title,
                        manufacturer=value_or_none(row["Výrobce"].strip()),
                        note=row.get("Poznámka", "").strip(),
                        model=value_or_none(row.get("Model", "").strip()),
                        serial=value_or_none(
                            row.get("Sériové číslo", "").strip()),
                        custom_code=int(
                            row["Inv. č."].strip().replace(cat.prefix, "")),
                        num_photos=0,
                        condition=0,
                        functionality=0,
                        status=AssetStatus.unknown
                    )
                    print(" ASSET", end='')
                    # pprint(asset)
                    tx = Transaction(
                        transaction_type=TransactionType.acquisition,
                        user_id=user_map.get(
                            row.get("Pořízeno kým", "").strip()),
                        counterparty=row.get("Pořízeno od", "").strip(),
                        cost=coerce_int(row.get("Pořízeno za", "")) or None,
                        date=None,
                        note="Import z Googlu:\nPořídil(a): " + row.get("Pořízeno kým", "").strip() + "\n za: " + row.get(
                            "Pořízeno za", "").strip() + "\n od: " + row.get("Pořízeno od", "").strip()
                    )
                    asset.transactions.append(tx)
                    print(" TX", end='')

                    if cat.name in ["television", "monitor"]:
                        add_meta(asset, "Status Note", row.get(
                            "Poznámky kompatibility"))
                    else:
                        add_meta(asset, "Status Note", row.get("Stav"))

                    if "Funkční" in row.keys():
                        add_meta(asset, "Functionality Note",
                                 "Funkční: " + row["Funkční"])

                    # if cat.name == "console":

                    if cat.name in ["game", "other software"]:
                        add_meta(asset, "Platform", row["Platforma"])
                        add_meta(asset, "Medium", row["Formát"])
                        add_meta(asset, "Product No", row["Písmena a čísla"])

                    if cat.name == "computer mouse":
                        add_meta(asset, "Color", row["Vzhled"])
                        add_meta(asset, "Type", row["Styl"])
                        add_meta(asset, "Connection", row["Typ"])
                        add_meta(
                            asset, "# of Buttons", 4 if row["4 tl"] == "TRUE" else 3 if row["mid b"] == "TRUE" else 2)
                        add_meta(asset, "# of Wheels",
                                 1 if row["kol"] == "TRUE" else 0)

                    if cat.name == "keyboard":
                        add_meta(asset, "Color", row["Vzhled"])
                        #add_meta(asset, "Type", row["Styl"])
                        add_meta(asset, "Connection", row["Typ"])

                    if cat.name == "television":
                        add_meta(asset, "Size", row["Úhlopříčka"])
                        add_meta(asset, "Needs remote", row["Ovladač potřeba"])
                        if row["Coax"].strip() == "1":
                            add_meta(asset, "Input", "Coaxial")
                        if row["Cinch"].strip() == "2":
                            add_meta(asset, "Input", "Cinch x2")
                        elif row["Cinch"].strip() == "1":
                            add_meta(asset, "Input", "Cinch")
                        if row["SCART"].strip() == "3":
                            add_meta(asset, "Input", "SCART x3")
                        elif row["SCART"].strip() == "2":
                            add_meta(asset, "Input", "SCART x2")
                        elif row["SCART"].strip() == "1":
                            add_meta(asset, "Input", "SCART")
                        if row["DIN"].strip() == "1":
                            add_meta(asset, "Input", "DIN")

                    if cat.name == "monitor":
                        add_meta(asset, "Size", row["Úhlopříčka"].strip())
                        add_meta(asset, "Visual notes",
                                 row["Pozn. znamení"].strip())
                        if row["VGA"].strip() in ["IN", "OUT", "in", "2 IN"]:
                            add_meta(
                                asset, "Input", "VGA x2" if row["VGA"].strip() == "2 IN" else "VGA")
                            if row["VGA"].strip() == "OUT":
                                add_meta(asset, "Fixed cable", "VGA")
                        if row["DVI"].strip() == "IN":
                            add_meta(asset, "Input", "DVI")
                        if row["AUDIO"].strip() == "1":
                            add_meta(asset, "Input", "Audio jack")
                        if row["AC"].strip() == "IN":
                            add_meta(asset, "Voltage", "AC 220V")
                        if "IN " in row["DC"]:
                            add_meta(asset, "Voltage",
                                     row["DC"].strip().replace("IN", "DC"))
                    print(" META", end='')
                    db.session.add(asset)
                    db.session.commit()
                    print(" SAVE", end='')
                    log("Create", asset)
                    # pprint(tx)
                    log("Create", tx)

                    # TODO: log neuklada MN vazbu
                    print(" LOG.")
