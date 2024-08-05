import json
from urllib import request
import random
import os
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import print as rprint
from art import text2art
from pyfiglet import Figlet
from rich.text import Text

class ComfyUIPromptGeneratorFlux:
    """ComfyUIのプロンプトを生成し、サーバーにキューイングするクラス"""

    def __init__(self, server_address: str = "127.0.0.1:8188", workflow_path: Optional[str] = None):
        """
        コンストラクタ: クラスの初期化を行います
        
        :param server_address: ComfyUIサーバーのアドレス（デフォルトは localhost の 8188 ポート）
        :param workflow_path: ワークフローJSONファイルへのパス（デフォルトはNone）
        """
        self.console = Console(width=120)
        self.server_address = server_address
        
        if workflow_path is None:
            self.workflow_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workflow_api.json')
        else:
            self.workflow_path = workflow_path
        
        self.prompt = self._load_workflow()

    def _load_workflow(self) -> Dict[str, Any]:
        """ワークフローJSONファイルを読み込むプライベートメソッド"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Loading workflow...", total=None)
                with open(self.workflow_path, 'r') as file:
                    workflow = json.load(file)
                progress.update(task, completed=True)
            self.console.print(Panel(f"[green]Workflow loaded successfully from {self.workflow_path}[/green]"))
            return workflow
        except FileNotFoundError:
            self.console.print(Panel(f"[red]Workflow file not found: {self.workflow_path}[/red]", title="Error"))
            raise
        except json.JSONDecodeError:
            self.console.print(Panel(f"[red]Invalid JSON in workflow file: {self.workflow_path}[/red]", title="Error"))
            raise ValueError(f"Invalid JSON in workflow file: {self.workflow_path}")

    def set_clip_text(self, text: str, node_id: str = "283") -> None:
        """CLIPTextEncodeノードのテキストを設定するメソッド"""
        self.prompt[node_id]["inputs"]["text"] = text
        self.console.print(f"[yellow]CLIP text set to:[/yellow] {text}")

    def set_random_seed(self, node_id: str = "271") -> None:
        """KSamplerノードのシードをランダムに設定するメソッド"""
        seed = random.randint(1, 1_000_000)
        self.prompt[node_id]["inputs"]["noise_seed"] = seed
        self.console.print(f"[yellow]Random seed set to:[/yellow] {seed}")

    def queue_prompt(self) -> None:
        """プロンプトをComfyUIサーバーにキューイングするメソッド"""
        data = json.dumps({"prompt": self.prompt}).encode('utf-8')
        req = request.Request(f"http://{self.server_address}/prompt", data=data, headers={'Content-Type': 'application/json'})
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Queueing prompt...", total=None)
            try:
                request.urlopen(req)
                progress.update(task, completed=True)
                self.console.print(Panel("[green]Prompt queued successfully[/green]"))
            except Exception as e:
                progress.update(task, completed=True)
                self.console.print(Panel(f"[red]Failed to queue prompt: {str(e)}[/red]", title="Error"))
                raise ConnectionError(f"Failed to queue prompt: {str(e)}")

    def generate_and_queue(self, clip_text: str) -> None:
        """プロンプトを生成し、キューイングするメソッド"""
        self.console.rule("[bold blue]Generating and Queueing Prompt")
        self.set_clip_text(text=clip_text, node_id="6")
        self.set_random_seed(node_id="25")
        self.queue_prompt()
        self.console.rule("[bold blue]Process Completed")

    def display_prompt(self) -> None:
        """現在のプロンプトを表示するメソッド"""
        prompt_json = json.dumps(self.prompt, indent=2)
        syntax = Syntax(prompt_json, "json", theme="monokai", line_numbers=True)
        self.console.print(Panel(syntax, title="Current Prompt", expand=True))

if __name__ == "__main__":
    console = Console(width=220)
    # Figletを使用してASCIIアートを生成
    f = Figlet(font='slant', width=200)
    title = f.renderText('ComfyUI Prompt Generator')
    
    # ASCIIアートをRichのTextオブジェクトに変換し、色を付ける
    title_text = Text.from_ansi(title)
    title_text.stylize("bold magenta")
    
    # パネル内にASCIIアートを表示
    console.print(Panel(title_text, expand=False, border_style="bold blue"))
    
    console.print(Panel("[bold cyan]ComfyUI Prompt Generator Demo[/bold cyan]"))

    console.rule("[bold green]Using Custom Workflow")
    
    # カスタムワークフローパスを指定
    custom_workflow_path = r"workflow\workflow_api_flux.json"
    custom_generator = ComfyUIPromptGeneratorFlux(workflow_path=custom_workflow_path)
    custom_generator.generate_and_queue("Photorealistic landscape")
    custom_generator.display_prompt()
