#!/bin/bash

# PyGiCo-ImageGen CLIの使用例

echo "PyGiCo-ImageGen CLIの使用例を開始します..."

# ブログから画像を生成
echo "1. ブログから画像を生成します..."
pygico-imagegen generate --blog-path sample_blog.txt --output generated_image.png

# 生成された画像にテキストを追加
echo "2. 生成された画像にテキストを追加します..."
pygico-imagegen process --blog-path sample_blog.txt --text "サンプルテキスト" --output final_image.png

echo "処理が完了しました。final_image.png を確認してください。"
