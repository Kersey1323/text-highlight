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

from pdf_utils import ocr_and_highlight_pdf


def main():
    """
    示例：使用OCR高亮扫描版PDF中的敏感词
    """
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    input_pdf = os.path.join(project_root, "data", "中菱钢诉兴业建筑、安州旅游起诉状.pdf")
    output_pdf = os.path.join(project_root, "outputs", "扫描版PDF高亮示例_OCR.pdf")

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
    print(f"输出文件: {output_pdf}")
    print(f"敏感词: {sensitive_words}")
    print("=" * 60)

    # 执行OCR高亮
    success = ocr_and_highlight_pdf(input_pdf, sensitive_words, output_pdf)

    if success:
        print("\n✓ PDF highlighting completed successfully!")
        print(f"✓ Output saved to: {output_pdf}")
    else:
        print("\n✗ PDF highlighting failed!")


if __name__ == "__main__":
    main()
