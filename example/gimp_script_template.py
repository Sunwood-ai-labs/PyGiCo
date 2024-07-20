# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
from gimpfu import *
import json

# JSONファイルから設定を読み込む
CONFIG_PATH = r"gimp_script_config.json"

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

# 引数を取得
ARGS = CONFIG["arguments"]


def log_info(message):
    print("INFO: " + message)

def log_success(message):
    print("SUCCESS: " + message)

def create_ascii_art(text):
    # 簡単なASCIIアートを生成する関数
    art = ""
    for line in text.split("\n"):
        art += "*" * (len(line) + 4) + "\n"
        art += "* " + line + " *\n"
        art += "*" * (len(line) + 4) + "\n"
    return art

def create_text_image():
    print("\n")
    print(create_ascii_art("Main flow"))
    
    # パラメータをハードコーディング
    input_path = ARGS["input_image"]
    output_path = ARGS["output_path"]
    text = ARGS["text"].replace("\\n", "\n")
    font_size = ARGS["font_size"]
    
    log_info("新しい画像を作成中...")
    width, height = 400, 200
    # 入力画像を開く
    image = pdb.gimp_file_load(input_path, input_path)
            
    log_info("テキストレイヤーを追加中...")
    text_layer = pdb.gimp_text_layer_new(image, text, "Yu Mincho", font_size, 0)
    pdb.gimp_image_insert_layer(image, text_layer, None, -1)
    
    log_info("テキストの色を設定中...")
    pdb.gimp_text_layer_set_color(text_layer, (0, 0, 0))
    
    log_info("テキストレイヤーを中央に配置しています...")
    pdb.gimp_text_layer_set_justification(text_layer, TEXT_JUSTIFY_CENTER)
    pdb.gimp_layer_set_offsets(text_layer, 
                               (image.width - pdb.gimp_drawable_width(text_layer)) // 2, 
                               (image.height - pdb.gimp_drawable_height(text_layer)) // 2)
    
    log_info("画像を保存中...")
    pdb.gimp_file_save(image, pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE), output_path, output_path)
    
    log_info("画像を閉じています...")
    pdb.gimp_image_delete(image)
    
    log_success("画像の作成が完了しました！")

print(create_ascii_art("GIMP Script Start"))

create_text_image()

log_success("画像が保存されました: " + ARGS["output_path"])
log_info("Gimpのバージョンは " + str(pdb.gimp_version()))
log_info("Pythonのバージョンは " + str(sys.version))

print(create_ascii_art("GIMP Script End"))

pdb.gimp_quit(1)
