"""
扫描版PDF高亮示例（使用OCR）
适用于无法直接提取文本的扫描版PDF
"""

import os
import sys

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from pdf_utils import ocr_and_highlight_pdf, ocr_and_highlight_pdf_text_layer


def main():
    """
    示例：使用OCR高亮扫描版PDF中的敏感词
    """
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    input_pdf = os.path.join(project_root, "data", "中菱钢诉兴业建筑、安州旅游起诉状.pdf")
    output_pdf_text_layer = os.path.join(project_root, "outputs", "扫描版PDF高亮_文本层.pdf")
    output_pdf_image = os.path.join(project_root, "outputs", "扫描版PDF高亮_图片方式.pdf")

    # 定义要高亮的敏感词
    sensitive_words = [
        "兴业建筑",
        "安州旅游",
        "中菱钢",
        "违约金",
        "质保金",
        "分包结算书",
        "安正兴业"
    ]

    print("=" * 60)
    print("扫描版PDF高亮示例（使用OCR）")
    print("=" * 60)
    print(f"输入文件: {input_pdf}")
    print(f"敏感词: {sensitive_words}")
    print("=" * 60)

    # 选择处理模式
    print("\n请选择处理模式:")
    print("1. 文本层模式 (保留原页面，添加可搜索文本层)")
    print("2. 图片模式 (重新渲染为图片)")

    # 默认使用文本层模式
    mode = 1

    if mode == 1:
        print(f"\n使用模式1: 文本层模式")
        output_pdf = output_pdf_text_layer
        success = ocr_and_highlight_pdf_text_layer(input_pdf, sensitive_words, output_pdf)
    else:
        print(f"\n使用模式2: 图片模式")
        output_pdf = output_pdf_image
        success = ocr_and_highlight_pdf(input_pdf, sensitive_words, output_pdf)

    if success:
        print("\n✓ PDF highlighting completed successfully!")
        print(f"✓ Output saved to: {output_pdf}")
    else:
        print("\n✗ PDF highlighting failed!")


if __name__ == "__main__":
    main()
