<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/PyGiCo.png" width="100%">
<br>
<h1 align="center">PyGiCo</h1>
<h2 align="center">
  ～ Seamless ComfyUI Integration ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pygico-imagegen">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/pygico-imagegen">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/pygico-imagegen">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/pygico-imagegen">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/pygico-imagegen">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/pygico-imagegen">
<a href="https://github.com/Sunwood-ai-labs/PyGiCo" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=PyGiCo&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/PyGiCo">
<a href="https://github.com/Sunwood-ai-labs/PyGiCo"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/PyGiCo/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/PyGiCo"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/PyGiCo"></a>
<a href="https://github.com/Sunwood-ai-labs/PyGiCo"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/PyGiCo"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/PyGiCo?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/PyGiCo?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/PyGiCo/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。


PyGiCo-ImageGenは、Python、GIMP、ComfyUIを使用して、ブログコンテンツから画像を生成し、テキストを追加するツールです。

## 機能

- ブログ記事からの内容抽出
- 抽出されたコンテンツに基づく画像生成プロンプトの作成
- ComfyUIを使用した高品質な画像生成
- GIMPを利用した画像へのテキスト追加
- コマンドラインインターフェース（CLI）とPythonパッケージの両方をサポート

## インストール

```bash
pip install pygico-imagegen
```

## 使用方法

### コマンドラインインターフェース

```bash
pygico-imagegen --blog path/to/blog.txt --output output.png --text "追加するテキスト"
```

### Pythonパッケージとして

```python
from pygico_imagegen import BlogExtractor, PromptGenerator, ComfyInterface, GimpExecutor

extractor = BlogExtractor("path/to/blog.txt")
content = extractor.extract()

generator = PromptGenerator()
prompt = generator.generate(content)

comfy = ComfyInterface()
image = comfy.generate_image(prompt)

gimp = GimpExecutor()
gimp.add_text(image, "追加するテキスト", "output.png")
```

## 設定

- 環境変数: `.env` ファイルまたはシステム環境変数で設定
- コンフィグファイル: `~/.config/pygico-imagegen/config.json` に配置

## 開発者向け情報

1. リポジトリのクローン:
   ```
   git clone https://github.com/yourusername/pygico-imagegen.git
   cd pygico-imagegen
   ```

2. 開発用依存関係のインストール:
   ```
   pip install -e .[dev]
   ```

3. テストの実行:
   ```
   pytest
   ```

4. コードスタイルのチェック:
   ```
   black .
   isort .
   ```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## コントリビューション

バグ報告、機能リクエスト、プルリクエストを歓迎します。大きな変更を加える前に、まずissueを開いて議論してください。
