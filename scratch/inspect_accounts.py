import json

with open("data/system_configuration.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

print("Account Groups:")
print(json.dumps(cfg.get("account_groups", []), indent=2))

print("\nAccounts:")
print(json.dumps(cfg.get("accounts", []), indent=2))

