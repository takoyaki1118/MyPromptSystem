# MyPromptSystem/base_nodes.py
import random
import os
import json
import re

# Load prompt data globally (or find a better way to pass it if needed)
PROMPT_DATA_PATH = os.path.join(os.path.dirname(__file__), 'prompt_data.json')
PROMPT_DATA = {}
if os.path.exists(PROMPT_DATA_PATH):
    with open(PROMPT_DATA_PATH, 'r', encoding='utf-8') as f:
        PROMPT_DATA = json.load(f)
else:
    print(f"[MyPromptSystem] Warning: {PROMPT_DATA_PATH} not found.")

def _parse_specific_choices(choices_str):
    """Helper function to parse comma or newline separated strings."""
    if not choices_str or not choices_str.strip():
        return []
    # Normalize separators to commas, then split
    items = re.split(r'\s*,\s*|\s*\n\s*', choices_str.strip())
    return [item.strip() for item in items if item.strip()]

# --- Base class for simple selection ---
class SelectorNodeBase:
    CATEGORY = "MyPromptSystem" # All nodes in this system share the category
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_item",) # Consistent output name
    FUNCTION = "select_item"

    # CATEGORY_NAME will be set by the dynamic class creation
    CATEGORY_NAME = "Unknown"

    def select_item(self, item):
        # Simple passthrough for the selected item
        return (item,)

# --- Base class for category generation ---
class BaseCategoryNode:
    CATEGORY = "MyPromptSystem"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",) # Consistent output name
    FUNCTION = "generate_tags"

    MODES = ("Random", "Specific", "None")

    # CATEGORY_NAME will be set by the dynamic class creation
    CATEGORY_NAME = "Unknown"

    def generate_tags(self, enable, mode, random_count, specific_choices, seed):
        if not enable:
            return ("",) # Return empty string if disabled

        category_config = PROMPT_DATA.get(self.CATEGORY_NAME, {})
        pool = category_config.get("pool", [])
        generated_tags = []

        if mode == "Random":
            if random_count > 0 and pool:
                rng = random.Random(seed)
                actual_count = min(random_count, len(pool))
                try:
                    generated_tags = rng.sample(pool, actual_count)
                except ValueError:
                    pass # Pool empty or count invalid
        elif mode == "Specific":
            generated_tags = _parse_specific_choices(specific_choices)
        # elif mode == "None":
            # generated_tags remains empty

        # Join the tags into a single comma-separated string
        output_string = ", ".join(filter(None, generated_tags))
        return (output_string,)