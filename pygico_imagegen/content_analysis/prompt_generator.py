import os
from typing import Dict, Any
from loguru import logger
from dotenv import load_dotenv
from litellm import completion
import random
from art import text2art

class PromptGenerator:
    def __init__(self):
        load_dotenv()
        # self.api_key = os.getenv('GEMINI_API_KEY')
        # if not self.api_key:
        #     raise ValueError("GEMINI_API_KEYが設定されていません。")

    def generate(self, content: str) -> str:
        print(text2art(">> PromptGenerator"))
        """与えられたコンテンツを使用してプロンプトを生成する"""
        logger.info(f"コンテンツ \n'{content}'\n からプロンプトを生成します")
        prompt = f"下記のブログ記事の内容を表現するシンプルな画像の英語プロンプトを提案してください。英語プロンプトのみを出力してください：\n\n{content}"
        # os.environ['GEMINI_API_KEY'] = self.api_key
        response = completion(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}]
        )
        generated_prompt = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        logger.success(f"プロンプトを生成しました: \n{generated_prompt}")
        return generated_prompt

    def customize_workflow(self, workflow: Dict[str, Any], content: str) -> Dict[str, Any]:
        """ワークフローをカスタマイズし、プロンプトとシードを設定する"""
        logger.info("ワークフローをカスタマイズします")
        prompt = self.generate(content)
        workflow["283"]["inputs"]["text"] = f"""
        3D low poly model of [{prompt}], 
        isometric view, 
        2D game art style, 
        light background, 
        soft lighting, 
        low detail, white background, Intricate details and realistic textures, ((image center is blank area))
        """
        workflow["271"]["inputs"]["seed"] = random.randint(1, 1000000)
        logger.success("ワークフローのカスタマイズが完了しました")
        return workflow
