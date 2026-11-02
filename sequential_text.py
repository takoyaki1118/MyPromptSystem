class SequentialTextNode:
    def __init__(self):
        self.index = 0

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "default": ""}),
                "text_2": ("STRING", {"multiline": True, "default": ""}),
                "text_3": ("STRING", {"multiline": True, "default": ""}),
                "text_4": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "reset_counter": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_next_text"
    CATEGORY = "MyPromptSystem/utils"  # お好みのカテゴリに調整可能です

    def get_next_text(self, text_1, text_2, text_3, text_4, reset_counter=False):
        texts = [text_1, text_2, text_3, text_4]
        
        if reset_counter:
            self.index = 0
            
        current_text = texts[self.index % len(texts)]
        self.index += 1
        
        return (current_text,)