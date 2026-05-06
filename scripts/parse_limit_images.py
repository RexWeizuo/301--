# -*- coding: utf-8 -*-
"""
将 301 项目 '极限' 文件夹下的数学图片解析为 LaTeX 公式，
生成 Markdown 文件存入 301 项目的对应目录。
"""
import sqlite3
import json
import os
import glob
import base64
import urllib.request
import urllib.error
import time

# Configuration
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "极限")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "极限_latex")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "301_study.db")
API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY_HERE")
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

def call_vision(image_path):
    """Call qwen-vl-max-latest to extract LaTeX from an image."""
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "你是一个数学公式识别专家。请仔细查看图片中的数学公式，"
        "将所有公式转换为 LaTeX 格式。\n\n"
        "要求：\n"
        "1. 按照公式在图片中从上到下的顺序排列\n"
        "2. 如果图片包含解题过程，请保留每个关键步骤的公式\n"
        "3. 用 ```latex ... ``` 代码块包裹公式\n"
        "4. 不要输出任何解释性文字，只输出 LaTeX 代码\n"
        "5. 如果图片中有中文标注（如'洛'表示洛必达法则），也一并保留"
    )

    payload = json.dumps({
        "model": "qwen-vl-max-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }).encode('utf-8')

    for attempt in range(3):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }, method='POST')
            with urllib.request.urlopen(req, timeout=45) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"  [API Error] attempt {attempt+1}/3: {e}", flush=True)
            if attempt < 2:
                time.sleep(3)
    return None

def extract_latex_from_text(text):
    """Extract LaTeX code blocks from the response text."""
    results = []
    in_block = False
    current_block = []
    for line in text.split('\n'):
        if line.strip().startswith('```latex'):
            in_block = True
            continue
        elif line.strip().startswith('```') and in_block:
            in_block = False
            results.append('\n'.join(current_block))
            current_block = []
        elif in_block:
            current_block.append(line)
    
    if not results and text.strip():
        # If no code blocks found, return the whole text
        results.append(text.strip())
    
    return results

def main():
    print("=" * 60, flush=True)
    print("301 极限文件夹图片 -> LaTeX 解析脚本", flush=True)
    print("=" * 60, flush=True)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量", flush=True)
        return

    # Find all images
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    images = []
    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
    
    # Also check subdirectories
    images.extend(glob.glob(os.path.join(IMAGE_DIR, "**", "*.png"), recursive=True))
    images.extend(glob.glob(os.path.join(IMAGE_DIR, "**", "*.jpg"), recursive=True))
    images.extend(glob.glob(os.path.join(IMAGE_DIR, "**", "*.jpeg"), recursive=True))

    # Remove duplicates
    images = sorted(list(set(images)))
    total = len(images)
    print(f"\n📊 发现 {total} 张图片待解析\n", flush=True)

    if total == 0:
        print("没有找到图片文件，退出。", flush=True)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_lines = []
    md_lines.append("# 极限 - 数学公式笔记\n\n")
    md_lines.append("> 本文件由 AI 自动从图片中提取生成，包含 301 考研数学极限章节的手写公式笔记。\n\n")
    md_lines.append("---\n\n")

    success_count = 0
    fail_count = 0

    for i, img_path in enumerate(images):
        filename = os.path.basename(img_path)
        # Extract number from filename
        parts = filename.split()
        img_num = parts[1].split('.')[0] if len(parts) > 1 else str(i+1)
        
        print(f"[{i+1}/{total}] 解析 image {img_num} ...", flush=True)
        
        latex_text = call_vision(img_path)
        
        if latex_text:
            latex_blocks = extract_latex_from_text(latex_text)
            md_lines.append(f"## 图片 {img_num}\n\n")
            md_lines.append(f"![image {img_num}](../极限/{filename})\n\n")
            
            for j, block in enumerate(latex_blocks):
                md_lines.append(f"**公式 {j+1}:**\n\n")
                md_lines.append(f"```latex\n{block}\n```\n\n")
                # Also render as display math
                md_lines.append(f"$$\n{block}\n$$\n\n")
            
            md_lines.append("---\n\n")
            success_count += 1
            print(f"  ✅ 解析成功 ({len(latex_blocks)} 个公式块)", flush=True)
        else:
            fail_count += 1
            print(f"  ❌ 解析失败", flush=True)
        
        # Rate limit
        time.sleep(1)

    # Write markdown file
    output_path = os.path.join(OUTPUT_DIR, "极限公式笔记.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(md_lines))

    print(f"\n🎉 解析完成！", flush=True)
    print(f"   成功: {success_count} 张", flush=True)
    print(f"   失败: {fail_count} 张", flush=True)
    print(f"   输出文件: {output_path}", flush=True)

if __name__ == "__main__":
    main()
