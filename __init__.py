# MyPromptSystem/__init__.py
import os
import json
import traceback # For better error reporting

# Print a message to confirm the script is running during ComfyUI startup
print("Initializing MyPromptSystem Nodes...")

try:
    # Import base classes and combiner node
    from .base_nodes import SelectorNodeBase, BaseCategoryNode, PROMPT_DATA
    from .combiner_node import PromptCombinerNode

    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}

    # Prepare dictionary to hold optional inputs for the combiner
    combiner_optional_inputs = {}
    category_order = list(PROMPT_DATA.keys()) # Use JSON order for combiner inputs

    # Dynamically generate nodes based on JSON data
    for category_key in category_order:
        if category_key not in PROMPT_DATA:
             print(f"[MyPromptSystem] Warning: Key '{category_key}' not found in PROMPT_DATA during node generation.")
             continue

        config = PROMPT_DATA[category_key]
        node_type = config.get("type")

        # Generate Class Name (e.g., "Body Type" -> "BodyTypeNode")
        class_name_safe = "".join(word.capitalize() for word in category_key.split())
        class_name = f"{class_name_safe}Node"

        base_class = None
        input_types_dict = {} # Reset for each node
        display_name = f"{category_key}" # Default display name
        combiner_input_name = "" # Initialize combiner_input_name

        if node_type == "selector":
            base_class = SelectorNodeBase
            items = config.get("items", [])
            default_item_value = config.get("default_item")

            actual_default = items[0] if items else "" # Fallback if items list is empty
            if default_item_value and default_item_value in items:
                actual_default = default_item_value
            elif items and "None" in items: # Prioritize "None" if present and no other default
                actual_default = "None"
            elif items: # Otherwise, first item
                actual_default = items[0]

            input_types_dict = {
                "required": {
                    "item": (items, {"default": actual_default})
                }
            }
            display_name = f"{category_key} Selector"
            combiner_input_name = category_key.lower().replace(" ", "_")

        elif node_type == "category_generator":
            base_class = BaseCategoryNode
            default_mode = config.get("default_mode", "Random")
            default_count = config.get("default_count", 1)
            input_types_dict = {
                "required": {
                    "enable": ("BOOLEAN", {"default": True}),
                    "mode": (BaseCategoryNode.MODES, {"default": default_mode}),
                    "random_count": ("INT", {"default": default_count, "min": 0, "max": 50}),
                    "specific_choices": ("STRING", {"multiline": True, "default": ""}),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                }
            }
            display_name = f"{category_key} Generator"
            combiner_input_name = category_key.lower().replace(" ", "_") + "_tags"

        else:
            print(f"[MyPromptSystem] Warning: Unknown node type '{node_type}' for category '{category_key}'. Skipping.")
            continue

        if base_class:
            # Factory function to create the INPUT_TYPES classmethod
            # This ensures that each class gets its own specific input_types_dict
            def get_input_types_factory(current_input_types):
                @classmethod
                def get_input_types(cls):
                    return current_input_types
                return get_input_types

            # Dynamically create the class using type()
            NewNodeClass = type(
                class_name,                     # New class name
                (base_class,),                  # Tuple of base classes
                {                               # Dictionary of attributes/methods
                    '__module__': __name__,     # Set module for proper identification
                    'CATEGORY_NAME': category_key, # Store the original JSON key
                    'INPUT_TYPES': get_input_types_factory(input_types_dict.copy()) # Use factory with a copy
                }
            )

            # Register the dynamically created class
            NODE_CLASS_MAPPINGS[class_name] = NewNodeClass
            NODE_DISPLAY_NAME_MAPPINGS[class_name] = display_name

            # Define the corresponding input for the combiner node
            # For selector nodes, we expect a single string. For generator nodes, a comma-separated string.
            # Both can be handled as STRING inputs in the combiner.
            if combiner_input_name: # Ensure combiner_input_name was set
                combiner_optional_inputs[combiner_input_name] = ("STRING", {"forceInput": False, "default": ""})


    # --- Combiner Node Setup ---
    # Set the dynamically generated optional inputs for the combiner node
    PromptCombinerNode.SetOptionalInputs(combiner_optional_inputs)

    # Register the combiner node
    NODE_CLASS_MAPPINGS["PromptCombinerNode"] = PromptCombinerNode
    NODE_DISPLAY_NAME_MAPPINGS["PromptCombinerNode"] = "Prompt Combiner"

    # Export the mappings
    __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

    print(f"Successfully initialized {len(NODE_CLASS_MAPPINGS)} nodes for MyPromptSystem.")

except Exception as e:
    print(f"Error initializing MyPromptSystem nodes: {e}")
    traceback.print_exc() # Print detailed traceback for debugging
    # Ensure __all__ is still defined even on error to avoid ComfyUI load issues
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
    __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']