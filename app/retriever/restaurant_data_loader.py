import os
import json

def load_restaurant_static_info(restaurant_name: str) -> str:
    path = f"app/restaurants/{restaurant_name}/static_info.md"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_restaurant_dynamic_info(restaurant_name: str) -> dict:
    path = f"app/restaurants/{restaurant_name}/dynamic_info.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_restaurant_menu(restaurant_name: str) -> dict:
    path = f"app/restaurants/{restaurant_name}/menu.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_full_restaurant_context(restaurant_name: str) -> dict:
    return {
        "static_info": load_restaurant_static_info(restaurant_name),
        "dynamic_info": load_restaurant_dynamic_info(restaurant_name),
        "menu": load_restaurant_menu(restaurant_name)
    }
