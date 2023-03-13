import json


with open("config.json", "r", encoding="utf8") as f:
    data = json.load(f)


refresh_token = data.get("refresh_token")
key = data.get("key")
token_path = data.get("token_path")

warning_ranges = data.get("warning_ranges")

params = data.get("params")