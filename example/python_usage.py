"""PyGiCo-ImageGenのPythonパッケージとしての使用例"""

from pygico_imagegen import BlogExtractor, PromptGenerator, ComfyInterface, GimpExecutor
from loguru import logger
from art import text2art
from pygico_imagegen.utils.config_manager import ConfigManager
from pygico_imagegen.config import settings
from pprint import pprint

def main():
    print(text2art("PyGIMP USAGE"))

    # 設定内容を表示
    logger.info("Current settings:")
    pprint(settings.model_dump())
    # raise

    config = ConfigManager()
    logger.info("PyGiCo-ImageGen を開始します")
    blog_path = "sample_blog.md"
    text = "Hello PyGiCo"
    output_path = "output1.png"
    gimp_path = "gimp-console-2.10.exe"
    
    # ブログ内容の抽出
    logger.info(f"ブログファイル {blog_path} から内容を抽出します")
    extractor = BlogExtractor(blog_path)
    blog_content = extractor.extract()

    # プロンプトの生成とワークフローのカスタマイズ
    logger.info("画像生成プロンプトを作成し、ワークフローをカスタマイズします")
    generator = PromptGenerator()
    workflow = config.get_workflow()
    customized_workflow = generator.customize_workflow(workflow, blog_content)

    # 画像の生成
    logger.info("ComfyUI を使用して画像を生成します")
    comfy = ComfyInterface(settings.SERVER_ADDRESS)
    image = comfy.generate_image(customized_workflow)

    # テキストの追加
    logger.info(f"画像にテキスト '{text}' を追加します")
    gimp = GimpExecutor(gimp_path)
    temp_path = f"{text}.temp.png"
    image[-1].save(temp_path)
    gimp.add_text(temp_path, text, output_path)


    logger.success(f"処理が完了しました。結果は {output_path} に保存されています")

if __name__ == "__main__":
    main()
