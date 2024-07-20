import json
import requests
from loguru import logger
from PIL import Image
import io
import time
import os
from urllib import request, parse
from art import text2art

class ComfyInterface:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.base_url = f"http://{server_address}"
        logger.info(f"ComfyUIインターフェースを初期化しました。サーバーアドレス: {server_address}")

    def generate_image(self, workflow):
        print(text2art(">> ComfyInterface"))
        """ComfyUIを使用して画像を生成します。"""
        logger.info("ComfyUIを使用した画像生成プロセスを開始します")

        try:
            # 画像生成のキュー登録
            prompt_id = self._queue_prompt(workflow)
            
            # 生成完了を待機
            outputs = self._wait_for_generation(prompt_id)
            
            if not outputs:
                logger.warning("画像生成プロセスは完了しましたが、出力が見つかりません")
                return []

            # 画像の取得と返却
            images = []
            for node_output in outputs.values():
                for image_data in node_output.get('images', []):
                    images.append(self._get_image(image_data))
            
            logger.success(f"{len(images)}枚の画像の生成が完了しました")
            return images

        except Exception as e:
            logger.error(f"画像生成中にエラーが発生しました: {str(e)}")
            raise

    def _queue_prompt(self, workflow):
        """画像生成をキューに登録します。"""
        logger.info("画像生成をComfyUIのキューに登録しています")

        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        endpoint = f"{self.base_url}/prompt"
        logger.info(f"endpoint: {endpoint}")
        
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(endpoint, data=data, headers=headers)
            response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
            response_json = response.json()
            logger.info(f"サーバーレスポンス: {response_json}")
            return response_json['prompt_id']
        except requests.RequestException as e:
            logger.error(f"リクエスト中にエラーが発生しました: {str(e)}")
            raise


    def _wait_for_generation(self, prompt_id):
        """画像生成の完了を待機し、生成された画像の情報を返します。"""
        logger.info(f"画像生成の完了を待機しています。プロンプトID: {prompt_id}")
        max_attempts = 60  # 最大待機時間（秒）
        debug_folder = "debug_logs"
        os.makedirs(debug_folder, exist_ok=True)

        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/history/{prompt_id}")
                response.raise_for_status()
                data = response.json()

                # デバッグ用にJSONレスポンスを保存
                debug_file = os.path.join(debug_folder, f"response_{prompt_id}_{attempt}.json")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.debug(f"レスポンスをデバッグファイルに保存しました: {debug_file}")

                if prompt_id in data:
                    prompt_data = data[prompt_id]
                    if "outputs" in prompt_data:
                        outputs = prompt_data["outputs"]
                        # 出力が存在し、少なくとも1つのノードに画像がある場合
                        if any('images' in node_output for node_output in outputs.values()):
                            logger.success("画像生成が完了しました")
                            return outputs
                    elif "executing" in prompt_data and not prompt_data["executing"]:
                        logger.warning("生成プロセスが完了しましたが、出力が見つかりません")
                        return None

                logger.info(f"生成進行中... 試行回数: {attempt + 1}")
            except requests.RequestException as e:
                logger.warning(f"履歴の取得中にエラーが発生しました: {str(e)}")
            except json.JSONDecodeError as e:
                logger.error(f"JSONのデコードに失敗しました: {str(e)}")
                # JSONデコードエラーの場合、生のレスポンス内容をファイルに保存
                error_file = os.path.join(debug_folder, f"error_response_{prompt_id}_{attempt}.txt")
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logger.debug(f"エラーレスポンスを保存しました: {error_file}")
            except Exception as e:
                logger.error(f"予期せぬエラーが発生しました: {str(e)}")
            
            time.sleep(5)
        
        logger.error("画像生成がタイムアウトしました")
        raise TimeoutError("画像生成がタイムアウトしました")
    
    def _get_image(self, image_data):
        """生成された画像を取得します。"""
        logger.info("生成された画像を取得しています")
        try:
            # image_dataから直接ファイル名を取得
            filename = image_data.get('filename', '')
            subfolder = image_data.get('subfolder', '')
            image_type = image_data.get('type', 'output')  # デフォルトは'output'とする

            if not filename:
                raise ValueError("画像ファイル名が見つかりません")

            url = f"{self.base_url}/view?filename={filename}&subfolder={subfolder}&type={image_type}"
            logger.debug(f"画像取得URL: {url}")

            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            logger.success(f"画像の取得が完了しました: {filename}")
            return image
        except requests.RequestException as e:
            logger.error(f"画像の取得中にエラーが発生しました: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"画像の処理中に予期せぬエラーが発生しました: {str(e)}")
            raise
