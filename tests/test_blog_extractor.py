"""BlogExtractor のユニットテスト"""

import pytest
import os
from pygico_imagegen.content_analysis.blog_extractor import BlogExtractor

@pytest.fixture
def sample_blog_file(tmp_path):
    blog_content = """サンプルブログのタイトル
これはサンプルブログの内容です。
複数行にわたるコンテンツを含んでいます。
テスト用のデータとして使用します。
"""
    blog_file = tmp_path / "sample_blog.txt"
    blog_file.write_text(blog_content, encoding="utf-8")
    return str(blog_file)

def test_extract_content(sample_blog_file):
    extractor = BlogExtractor(sample_blog_file)
    content = extractor.extract()
    assert content.startswith("サンプルブログのタイトル")
    assert "複数行にわたるコンテンツ" in content

def test_extract_with_max_length(sample_blog_file):
    extractor = BlogExtractor(sample_blog_file)
    content = extractor.extract(max_length=20)
    assert len(content) == 20

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        extractor = BlogExtractor("non_existent_file.txt")
        extractor.extract()

def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding="utf-8")
    extractor = BlogExtractor(str(empty_file))
    content = extractor.extract()
    assert content == ""

def test_long_content(tmp_path):
    long_content = "A" * 1000
    long_file = tmp_path / "long_content.txt"
    long_file.write_text(long_content, encoding="utf-8")
    extractor = BlogExtractor(str(long_file))
    content = extractor.extract()
    assert len(content) == 300  # デフォルトの最大長が300文字であることを確認

def test_custom_max_length(sample_blog_file):
    extractor = BlogExtractor(sample_blog_file)
    content = extractor.extract(max_length=50)
    assert len(content) <= 50

def test_utf8_encoding(tmp_path):
    utf8_content = "こんにちは、世界！"
    utf8_file = tmp_path / "utf8_content.txt"
    utf8_file.write_text(utf8_content, encoding="utf-8")
    extractor = BlogExtractor(str(utf8_file))
    content = extractor.extract()
    assert content == utf8_content
