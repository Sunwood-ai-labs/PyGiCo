# pygico_imagegen/cli.py
import argparse
from loguru import logger
from .content_analysis.blog_extractor import BlogExtractor
from .content_analysis.prompt_generator import PromptGenerator
from .image_generation.comfy_interface import ComfyInterface
from .image_processing.gimp_executor import GimpExecutor
from .utils.config_manager import ConfigManager
from .config import settings

def main():
    parser = argparse.ArgumentParser(description="PyGiCo-ImageGen: ブログコンテンツから画像を生成し処理します。")
    parser.add_argument("--blog", help="ブログファイルのパス", default=settings.BLOG_PATH)
    parser.add_argument("--output", help="出力画像のパス", required=True)
    parser.add_argument("--text", help="画像に追加するテキスト", default=None)
    args = parser.parse_args()

    config = ConfigManager()
    logger.info("PyGiCo-ImageGen を開始します")

    try:
        # ブログ内容の抽出
        logger.info(f"ブログファイル {args.blog} から内容を抽出します")
        extractor = BlogExtractor(args.blog)
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

        # テキストの追加（オプション）
        if args.text:
            logger.info(f"画像にテキスト '{args.text}' を追加します")
            gimp = GimpExecutor(settings.GIMP_PATH)
            temp_path = f"{args.output}.temp.png"
            image[-1].save(temp_path)
            gimp.add_text(temp_path, args.text, args.output)
        else:
            logger.info(f"生成された画像を {args.output} に保存します")
            image[-1].save(args.output)

        logger.success(f"処理が完了しました。結果は {args.output} に保存されています")

    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    main()
