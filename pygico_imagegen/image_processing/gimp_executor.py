import json
from loguru import logger
from art import text2art
from pygimp.pygimp_core import PyGIMP

class GimpExecutor:
    def __init__(self, gimp_path='gimp-console-2.10.exe'):
        self.pygimp = PyGIMP(gimp_path)

    def add_text(self, input_image, text, output_path, config_path="gimp_script_config.json"):
        # ASCIIアートのタイトルを表示
        print(text2art(">> PyGIMP"))

        # 設定を読み込み
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # configが辞書であることを確認
        if not isinstance(config, dict):
            raise ValueError("読み込まれた設定が辞書ではありません")

        # 提供された引数でconfigを更新
        config["input_image"] = input_image
        config["output_path"] = output_path
        config["text"] = text

        # PyGIMPの設定を更新
        self.pygimp.update_config(**config)

        # GIMPスクリプトを実行
        self.pygimp.execute_script()

        logger.info(f"GIMPスクリプトが実行されました。出力: {output_path}")
