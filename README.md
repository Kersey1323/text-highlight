# PDF 文本高亮与 OCR 处理工具

一个用于处理 PDF 和图片的 OCR 工具，支持敏感词高亮、PDF 转 Word 文档（标准公文格式）等功能。

## 功能特性

- **PDF 文本高亮**：对扫描版 PDF 进行 OCR 识别并高亮显示敏感词
- **PDF 转 Word**：将 PDF 内容转换为格式化的 Word 文档（标准公文排版）
- **图片 OCR**：支持 PNG、JPG 等图片格式的 OCR 识别
- **敏感词标注**：自动识别并高亮敏感词汇
- **标准公文格式**：生成符合公文排版规范的 Word 文档

## 环境要求

- Python 3.7+
- 本地 OCR API 服务（需要单独部署）

## 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖说明

```
pymupdf          # PDF 处理
requests         # HTTP 请求
Pillow           # 图像处理
opencv-python    # 图像处理
python-docx      # Word 文档生成
```

## 配置

### OCR API 配置

编辑 `ocr_utils.py` 中的 OCR API 配置：

```python
OCR_API_URL = "http://localhost:80/processVL"
MODEL_NAME = "qwen3-vl-8b-instruct"
PROMPT = "请识别这张图片的内容并以markdown的格式给出。"
```

确保 OCR API 服务已启动并可访问。

## 使用方法

### 方式一：批量处理

将需要处理的 PDF 或图片文件放入 `data/` 目录，然后运行：

```bash
python main.py
```

程序会自动处理 `data/` 目录下的所有文件，并在相同目录生成标注后的文件。

### 方式二：使用测试脚本

#### 1. PDF 转 Word（推荐）

```bash
python test/test_pdf_to_docx.py
```

功能：将扫描版 PDF 转换为格式化的 Word 文档，支持：
- 标题识别与格式化
- 正文与标题的区分
- 标准公文排版（仿宋_GB2312、首行缩进、固定行距等）
- Markdown 格式解析

#### 2. 文本型 PDF 高亮

```bash
python test/test_text_pdf_highlight.py
```

适用于可直接提取文本的 PDF（非扫描版）。

#### 3. 扫描版 PDF OCR 高亮

```bash
python test/test_ocr_pdf_highlight.py
```

适用于扫描版 PDF，通过 OCR 识别后添加文本层和高亮。

### 方式三：自定义代码使用

```python
from pdf_utils import ocr_and_highlight_pdf_docx

# PDF 转 Word
ocr_and_highlight_pdf_docx(
    pdf_path="input.pdf",
    sensitive_words=["敏感词1", "敏感词2"],
    output_docx_path="output.docx",
    output_pdf_path="output.pdf"  # 可选
)
```

## 敏感词配置

在 `data/` 目录下创建同名敏感词文件，例如：

```
data/
├── 合同.pdf
└── 合同-敏感词.txt
```

`合同-敏感词.txt` 文件内容示例：

```
违约金
质保金
兴业建筑
```

每行一个敏感词。

## Word 文档排版规范

生成的 Word 文档采用标准公文排版格式：

| 项目 | 正文 | 小标题（##）|
|------|------|-------------|
| 字体 | 仿宋_GB2312 | 仿宋_GB2312 加粗 |
| 英文/数字 | Times New Roman | Times New Roman |
| 字号 | 小四（12pt） | 小四（12pt） |
| 对齐 | 两端对齐 | - |
| 首行缩进 | 2字符（0.74cm） | 2字符（0.74cm） |
| 行距 | 固定值28磅 | 固定值28磅 |
| 段前段后 | 0行 | 0行 |

## 项目结构

```
text-highlight/
├── main.py                # 主程序入口
├── ocr_utils.py           # OCR API 调用
├── pdf_utils.py           # PDF 处理工具
├── text_renderer.py       # 文本渲染工具
├── requirements.txt       # 依赖列表
├── data/                  # 输入文件目录
├── outputs/               # 输出文件目录
├── temp/                  # 临时文件目录
└── test/                  # 测试脚本
    ├── test_pdf_to_docx.py
    ├── test_text_pdf_highlight.py
    └── test_ocr_pdf_highlight.py
```

## 常见问题

### 1. OCR API 连接失败

确保 OCR API 服务已启动，检查 `ocr_utils.py` 中的 API 地址和端口配置。

### 2. Word 文档字体显示异常

确保系统已安装仿宋_GB2312 字体。如果没有，可以：
- 修改代码使用其他字体（如仿宋）
- 安装仿宋_GB2312 字体

### 3. 生成的 Word 文档排版不符

检查 OCR 输出的 Markdown 格式是否正确，确保标题使用 `#` 或 `##` 标记。

## 开发计划

- [ ] 支持更多文档格式输出
- [ ] 添加批量处理进度显示
- [ ] 支持自定义排版模板
- [ ] 添加 GUI 界面

## 许可证

MIT License
