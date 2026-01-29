"""
文本型PDF高亮示例
使用 PyMuPDF (fitz) 直接搜索文本并添加高亮注释

适用场景：文本型PDF（可以直接提取文本的PDF）
对于扫描版PDF，请使用 ocr_and_highlight_pdf 函数
"""

import os
import fitz  # PyMuPDF


def highlight_text_pdf(input_pdf_path, output_pdf_path, search_words, debug=True):
    """
    在文本型PDF中搜索敏感词并添加黄色高亮注释

    Args:
        input_pdf_path: 输入PDF文件路径
        output_pdf_path: 输出PDF文件路径
        search_words: 要搜索并高亮的敏感词列表
        debug: 是否输出调试信息

    Returns:
        bool: 成功返回True，失败返回False
    """
    try:
        # 打开PDF文档
        doc = fitz.open(input_pdf_path)

        print(f"Processing PDF: {input_pdf_path} ({len(doc)} pages)")
        print(f"Search words: {search_words}")

        total_highlights = 0

        # 遍历每一页
        for page_num, page in enumerate(doc):
            print(f"\n  Processing page {page_num + 1}/{len(doc)}...")

            # 调试：提取页面文本内容
            if debug:
                page_text = page.get_text()
                print(f"    [DEBUG] Page text length: {len(page_text)} chars")
                # 检查每个搜索词是否在文本中
                for word in search_words:
                    if word in page_text:
                        print(f"    [DEBUG] '{word}' found in page text")
                    else:
                        print(f"    [DEBUG] '{word}' NOT found in page text")

            page_highlights = 0

            # 遍历每个敏感词，使用多种搜索策略
            for word in search_words:
                text_instances = []

                # 策略1: 标准搜索（默认）
                if not text_instances:
                    text_instances = page.search_for(word)

                # 策略2: 使用 quads 参数搜索
                if not text_instances:
                    text_instances = page.search_for(word, quads=True)

                if text_instances:
                    print(f"    Found '{word}': {len(text_instances)} instance(s)")

                    # 为每个匹配的文本区域添加高亮注释
                    for inst in text_instances:
                        # 添加黄色高亮注释
                        # 颜色格式: (R, G, B, Alpha) 范围 0-1
                        # (1, 1, 0, 0.3) = 黄色，30%透明度
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=(1, 1, 0))  # 黄色边框
                        highlight.update()

                        page_highlights += 1
                        total_highlights += 1

            if page_highlights > 0:
                print(f"    Page {page_num + 1}: {page_highlights} highlights added")
            else:
                print(f"    Page {page_num + 1}: No matches found")

        # 保存修改后的PDF
        doc.save(output_pdf_path)
        doc.close()

        print(f"\n✓ Saved highlighted PDF to: {output_pdf_path}")
        print(f"✓ Total highlights added: {total_highlights}")

        return True

    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    示例：高亮PDF中的敏感词
    """
    # 配置路径 - 使用原始字符串避免转义问题
    # 获取项目根目录（test目录的上级目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    input_pdf = os.path.join(project_root, "outputs", "民事起诉状_从docx转换.pdf")
    output_pdf = os.path.join(project_root, "outputs", "文本型PDF高亮示例.pdf")

    # 定义要高亮的敏感词
    sensitive_words = [
        "中菱钢结构股份有限公司",
        "成都安正兴业建筑工程有限公司",

    ]

    # 执行高亮
    success = highlight_text_pdf(input_pdf, output_pdf, sensitive_words)

    if success:
        print("\n✓ PDF highlighting completed successfully!")
    else:
        print("\n✗ PDF highlighting failed!")


if __name__ == "__main__":
    main()
