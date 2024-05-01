import ijson

filename = "2024-04-07-DRE_dump.json"
data_dict = {}

with open(filename, "r", encoding="utf-8") as f:
    objects = ijson.items(f, "item")
    for idx, obj in enumerate(objects):
        if idx >= 10000:
            break
        if "claint" in obj and "notes" in obj:
            claint = obj["claint"]
            notes = obj["notes"].replace("\n", " ").replace("\r", " ")
            data_dict[claint] = notes

