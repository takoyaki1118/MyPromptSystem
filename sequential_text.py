import random

class SequentialTextNode:
    current_index = 0

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
    CATEGORY = "MyPromptSystem/utils"

    @classmethod
    def IS_CHANGED(s, *args, **kwargs):
        # 毎回異なる乱数を返すことで、ComfyUIのキャッシュを強制的に無効化し、毎回ノードを実行させる
        return random.random()

    def get_next_text(self, text_1, text_2, text_3, text_4, reset_counter=False):
        texts = [text_1, text_2, text_3, text_4]
        
        if reset_counter:
            SequentialTextNode.current_index = 0
            
        # 現在のインデックスからテキストを取得
        current_text = texts[SequentialTextNode.current_index % len(texts)]
        
        # 次回のためにインデックスを進める
        SequentialTextNode.current_index += 1
        
        return (current_text,)