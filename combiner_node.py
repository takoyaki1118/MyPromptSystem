# MyPromptSystem/combiner_node.py
import re
from .base_nodes import _parse_specific_choices # Reuse the helper

class PromptCombinerNode:
    CATEGORY = "MyPromptSystem"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "combine_prompts"

    # Store dynamic inputs here
    _optional_inputs_config = {}

    @classmethod
    def SetOptionalInputs(cls, inputs_dict):
        """Class method to set the configuration for optional inputs."""
        cls._optional_inputs_config = inputs_dict

    @classmethod
    def INPUT_TYPES(cls):
        required = {
            "prefix_tags": ("STRING", {"multiline": True, "default": "masterpiece, best quality"}),
             # Add separator option if desired
             "separator": ("STRING", {"default": ", "}),
             "suffix_tags": ("STRING", {"multiline": True, "default": ""}),
        }
        # Add the dynamically configured optional inputs
        optional = cls._optional_inputs_config
        return {"required": required, "optional": optional}

    def combine_prompts(self, separator=", ", prefix_tags="", suffix_tags="", **kwargs):
        # kwargs will contain values from all optional inputs defined in _optional_inputs_config
        parts = []

        # 1. Prefix Tags
        parts.extend(_parse_specific_choices(prefix_tags))

        # 2. Tags from Category Nodes
        # Iterate through the expected optional inputs to potentially control order
        for input_name in self._optional_inputs_config.keys():
            if input_name in kwargs:
                tag_string = kwargs[input_name]
                # Category nodes output comma-separated strings, parse them back
                if tag_string and tag_string.strip():
                     parts.extend(_parse_specific_choices(tag_string))

        # 3. Suffix Tags
        parts.extend(_parse_specific_choices(suffix_tags))

        # Combine using the specified separator and clean up
        final_prompt = separator.join(filter(None, parts))

        # Clean up potential double separators (more robust cleaning might be needed depending on separator)
        if separator.strip(): # Avoid issues if separator is just whitespace
            sep_pattern = re.escape(separator.strip())
            final_prompt = re.sub(rf'{sep_pattern}(\s*{sep_pattern})+', separator.strip(), final_prompt) # Handle repeating separators
            final_prompt = re.sub(rf'^\s*{sep_pattern}\s*|\s*{sep_pattern}\s*$', '', final_prompt) # Trim leading/trailing separators

        # Final trim of whitespace
        final_prompt = final_prompt.strip()

        return (final_prompt,)