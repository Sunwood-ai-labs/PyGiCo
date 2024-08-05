import os
from typing import Dict, Any
from loguru import logger
from dotenv import load_dotenv
from litellm import completion
import random
from art import text2art
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import print as rprint

console = Console(width=120)

class PromptGeneratorFlux:
    def __init__(self):
        load_dotenv()
        # self.api_key = os.getenv('GEMINI_API_KEY')
        # if not self.api_key:
        #     raise ValueError("GEMINI_API_KEYが設定されていません。")

    def generate(self, content: str) -> str:
        console.print(Panel(text2art("PromptGeneratorFlux", font="small"), expand=False))
        """与えられたコンテンツを使用してプロンプトを生成する"""
        with console.status("[bold green]プロンプトを生成中...", spinner="dots"):
            logger.info(f"コンテンツからプロンプトを生成します")
            console.print(Panel(content, title="入力コンテンツ", border_style="blue", expand=False))
            
            prompt = f"下記のブログ記事の内容を表現するシンプルな画像の英語プロンプトを提案してください。英語プロンプトのみを出力してください：\n\n{content}"
            # os.environ['GEMINI_API_KEY'] = self.api_key
            response = completion(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": prompt}]
            )
            generated_prompt = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            logger.success(f"プロンプトを生成しました")
            console.print(Panel(generated_prompt, title="生成されたプロンプト", border_style="green", expand=False))
            
        return generated_prompt

    def customize_workflow(self, workflow: Dict[str, Any], content: str) -> Dict[str, Any]:
        """ワークフローをカスタマイズし、プロンプトとシードを設定する"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task1 = progress.add_task("[cyan]ワークフローをカスタマイズ中...", total=3)
            
            progress.update(task1, advance=1, description="プロンプトを生成中...")
            prompt = self.generate(content)
            
            progress.update(task1, advance=1, description="ワークフローを更新中...")
            workflow["6"]["inputs"]["text"] = f"""
            3D low poly model of [{prompt}], 
            isometric view, 
            2D game art style, 
            light background, 
            soft lighting, 
            low detail, white background, Intricate details and realistic textures, ((image center is blank area))
            """
            workflow["25"]["inputs"]["seed"] = random.randint(1, 1000000)
            
            progress.update(task1, advance=1, description="カスタマイズ完了")
        
        logger.success("ワークフローのカスタマイズが完了しました")
        console.print(Panel(Syntax(str(workflow), "python", theme="monokai", line_numbers=True), title="カスタマイズされたワークフロー", expand=False))
        
        return workflow

# 使用例
if __name__ == "__main__":
    generator = PromptGeneratorFlux()
    sample_content = "AIと機械学習の進歩が私たちの日常生活にもたらす影響について"
    workflow = {
        "283": {"inputs": {"text": ""}},
        "271": {"inputs": {"seed": 0}}
    }
    customized_workflow = generator.customize_workflow(workflow, sample_content)
    rprint("[bold green]処理が完了しました！[/bold green]")
