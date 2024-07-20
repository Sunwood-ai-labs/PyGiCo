import os
from loguru import logger
from art import text2art

class BlogExtractor:
    def __init__(self, blog_path):
        self.blog_path = blog_path

    def extract(self, max_length=300):
        """ブログファイルからコンテンツを抽出します。"""
        print(text2art(">> BlogExtractor"))
        logger.info(f"{self.blog_path} からブログコンテンツを抽出中...")

        if not os.path.exists(self.blog_path):
            logger.error(f"ブログファイルが見つかりません: {self.blog_path}")
            raise FileNotFoundError(f"ブログファイルが見つかりません: {self.blog_path}")

        try:
            with open(self.blog_path, 'r', encoding='utf-8') as file:
                content = file.read(max_length)
            
            logger.success(f"ブログコンテンツの抽出が完了しました（{len(content)}文字）")
            return content
        except Exception as e:
            logger.error(f"ブログコンテンツの抽出中にエラーが発生しました: {str(e)}")
            raise
