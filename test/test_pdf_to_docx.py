"""
扫描版PDF转Word文档示例（使用OCR）
解析OCR返回的markdown格式文本，创建格式化的Word文档
"""

import os
import sys

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from pdf_utils import ocr_and_highlight_pdf_docx


def main():
    """
    示例：将扫描版PDF转换为格式化的Word文档
    """
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    input_pdf = os.path.join(project_root, "data", "test.pdf")
    output_docx = os.path.join(project_root, "outputs", "民事起诉状.docx")
    output_pdf = os.path.join(project_root, "outputs", "民事起诉状_从docx转换.pdf")

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
    print("扫描版PDF转Word文档示例（使用OCR）")
    print("=" * 60)
    print(f"输入文件: {input_pdf}")
    print(f"输出Word: {output_docx}")
    print(f"输出PDF: {output_pdf}")
    print(f"敏感词: {sensitive_words}")
    print("=" * 60)

    # 执行转换
    success = ocr_and_highlight_pdf_docx(
        input_pdf,
        sensitive_words,
        output_docx_path=output_docx,
        output_pdf_path=output_pdf
    )

    if success:
        print("\n✓ Document conversion completed successfully!")
        print(f"✓ Word document: {output_docx}")
        print(f"✓ PDF document: {output_pdf}")
    else:
        print("\n✗ Document conversion failed!")


if __name__ == "__main__":
    main()
