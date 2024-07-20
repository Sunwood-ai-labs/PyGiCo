import os
import json
from dotenv import load_dotenv
from loguru import logger

class ConfigManager:
    def __init__(self):
        logger.info("設定マネージャーを初期化しています")
        self.config = {}
        self._load_env()
        self._load_config_file()
        self._set_defaults()

    def _load_env(self):
        """環境変数を読み込みます。"""
        logger.info("環境変数を読み込んでいます")
        load_dotenv()
        self.config['BLOG_PATH'] = os.getenv('BLOG_PATH')
        self.config['SERVER_ADDRESS'] = os.getenv('SERVER_ADDRESS')
        self.config['GIMP_PATH'] = os.getenv('GIMP_PATH')
        self.config['WORKFLOW_PATH'] = os.getenv('WORKFLOW_PATH')

    def _load_config_file(self):
        """コンフィグファイルを読み込みます。"""
        config_path = os.path.expanduser("~/.config/pygico-imagegen/config.json")
        logger.info(f"コンフィグファイルを読み込んでいます: {config_path}")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        else:
            logger.warning(f"コンフィグファイルが見つかりません: {config_path}")

    def _set_defaults(self):
        """デフォルト値を設定します。"""
        logger.info("デフォルト設定を適用しています")
        defaults = {
            'BLOG_PATH': './blog.txt',
            'SERVER_ADDRESS': '127.0.0.1:8188',
            'GIMP_PATH': 'gimp',
            'WORKFLOW_PATH': './workflow.json',
            'OUTPUT_DIR': './output'
        }
        for key, value in defaults.items():
            if key not in self.config or self.config[key] is None:
                self.config[key] = value

    def get(self, key):
        """指定されたキーの設定値を取得します。"""
        value = self.config.get(key)
        if value is None:
            logger.warning(f"設定 '{key}' が見つかりません")
        return value

    def get_workflow(self):
        """ワークフローファイルを読み込みます。"""
        workflow_path = self.get('WORKFLOW_PATH')
        logger.info(f"ワークフローファイルを読み込んでいます: {workflow_path}")
        with open(workflow_path, 'r') as file:
            return json.load(file)

    def set(self, key, value):
        """指定されたキーに設定値を設定します。"""
        self.config[key] = value
        logger.info(f"設定 '{key}' を '{value}' に更新しました")
