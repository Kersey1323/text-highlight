# PDF 文本高亮与 OCR 处理工具

一个用于处理 PDF 和图片的 OCR 工具，支持敏感词高亮、PDF 转 Word 文档（标准公文格式）等功能。

## 功能特性

- **自动识别**：自动检测输入文件类型（Text PDF, Scanned PDF, Image）
- **PDF 文本高亮**：
    - **文本型 PDF**：直接搜索文本并高亮
    - **扫描版 PDF**：对扫描版 PDF 进行 OCR 识别并高亮显示敏感词
- **图片 OCR**：支持 PNG, JPG 等图片格式的 OCR 识别
- **敏感词标注**：自动识别并高亮敏感词汇
- **模块化设计**：配置与代码分离，易于扩展

## 环境要求

- Python 3.7+
- 本地 OCR API 服务（需要单独部署）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 目录结构

```
text-highlight/
├── main.py                  # 主程序入口
├── config.yaml              # 配置文件
├── src/                     # 源代码
│   ├── core/                # 核心逻辑 (Pipeline, Detector)
│   ├── processors/          # 处理器 (TextPDF, ScannedPDF, Image)
│   └── utils/               # 工具函数 (OCR, Renderer)
├── legacy/                  # 旧版代码
├── data/                    # 输入文件目录
├── outputs/                 # 输出文件目录
└── test/                    # 测试脚本
```

## 配置

项目使用 `config.yaml` 进行配置：

```yaml
paths:
  input_dir: "data"
  output_dir: "outputs"
  temp_dir: "temp"

sensitive_words:
  - "敏感词1"
  - "敏感词2"

ocr:
  lang: "ch_sim"
  dpi: 300
```

## 使用方法

### 方式一：命令行处理

```bash
# 处理单个文件
python main.py data/test.pdf

# 处理目录
python main.py data/
```

### 方式二：使用测试脚本

```bash
python test/test_pipeline.py
```

### 方式三：代码调用

```python
from src.core.pipeline import Pipeline

pipeline = Pipeline()
pipeline.process_file("data/test.pdf")
```

## 开发

### 添加新的处理器

1. 在 `src/processors/` 下创建新的处理器类，继承 `BaseHighlighter`。
2. 实现 `process` 方法。
3. 在 `src/core/pipeline.py` 中注册新的处理器。

## 许可证

MIT License
