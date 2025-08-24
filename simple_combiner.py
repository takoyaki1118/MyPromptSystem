# MyPromptSystem/simple_combiner.py
from .base_nodes import _parse_specific_choices # 既存の便利なヘルパー関数を再利用

class SimpleTextCombinerNode:
    CATEGORY = "MyPromptSystem"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "combine_text"

    @classmethod
    def INPUT_TYPES(cls):
        """
        ノードの入力UIを定義します。
        - 1つの必須の複数行テキストフィールド
        - 5つのオプショナルなテキスト入力ピン
        """
        return {
            "required": {
                "main_text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "text_1": ("STRING", {"forceInput": True}),
                "text_2": ("STRING", {"forceInput": True}),
                "text_3": ("STRING", {"forceInput": True}),
                "text_4": ("STRING", {"forceInput": True}),
                "text_5": ("STRING", {"forceInput": True}),
            }
        }

    def combine_text(self, main_text, text_1=None, text_2=None, text_3=None, text_4=None, text_5=None):
        """
        すべてのテキスト入力を結合するメインの関数です。
        """
        # 結合するパーツを格納するリスト
        all_parts = []
        
        # 1. メインのテキストフィールドをパースして追加
        all_parts.extend(_parse_specific_choices(main_text))

        # 2. 5つのオプショナルな入力ピンを順番にパースして追加
        #    リストで処理を共通化
        optional_inputs = [text_1, text_2, text_3, text_4, text_5]
        for text_input in optional_inputs:
            if text_input: # 入力がNoneや空文字列でない場合のみ処理
                all_parts.extend(_parse_specific_choices(text_input))

        # 3. 空の要素を取り除き、カンマとスペースで結合
        #    filter(None, ...) でリスト内の空文字列などを除去
        final_prompt = ", ".join(filter(None, all_parts))

        # ComfyUIの出力はタプル形式である必要がある
        return (final_prompt,)