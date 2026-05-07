import os
import json
import requests
from pathlib import Path

API_KEY = "sk-9980a81fba7f4d948c30a04100e27e8c"
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# 课后练习所在的页码（从0开始索引）
EXERCISE_PAGES = {
    "专题一_极限的计算_练习1-6": 20,
    "专题一_极限的计算_练习7-13": 22,
    "专题一_极限的计算_练习14-20": 25,
    "专题二_导数与微分计算_练习1-4": 42,
    "专题二_导数与微分计算_练习5-7": 43,
    "专题二_导数与微分计算_练习8-10": 44,
    "专题二_导数与微分计算_练习11-13": 45,
    "专题二_导数与微分计算_练习14-16": 46,
    "专题二_导数与微分计算_练习17-20": 47,
    "专题二_导数与微分计算_练习21-25": 48,
    "专题三_积分的计算_练习1-2": 66,
    "专题三_积分的计算_练习3": 67,
    "专题三_积分的计算_练习4": 68,
    "专题三_积分的计算_练习5-7": 69,
    "专题三_积分的计算_练习8-9": 70,
    "专题三_积分的计算_练习10-12": 71,
    "专题三_积分的计算_练习13": 72,
}

PDF_IMAGES_DIR = r"d:\study\301\pdf_images"
OUTPUT_DIR = r"d:\study\301\scripts\exercises_extracted"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROMPT = """请提取这张图片中的所有课后练习题内容，包括题目编号、题目描述、所有数学公式。
要求：
1. 用Markdown格式输出
2. 所有数学公式用$$包裹（行间公式）或$包裹（行内公式）
3. 保持题目编号
4. 如果有选项题，列出所有选项
5. 不要输出解析或答案，只提取题目本身
6. 如果图片中有多个题目，按顺序全部提取"""

def encode_image_to_base64(image_path):
    import base64
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_exercise_with_qwen(page_num, section_name):
    image_path = os.path.join(PDF_IMAGES_DIR, f"page_{page_num:03d}.png")
    if not os.path.exists(image_path):
        print(f"  图片不存在: {image_path}")
        return None
    
    base64_image = encode_image_to_base64(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "qwen-vl-plus",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": PROMPT
                    }
                ]
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"  API调用失败: {e}")
        return None

def main():
    all_exercises = {}
    
    for section_name, page_num in EXERCISE_PAGES.items():
        print(f"\n正在提取: {section_name} (第{page_num}页)...")
        result = extract_exercise_with_qwen(page_num, section_name)
        if result:
            all_exercises[section_name] = result
            print(f"  提取成功，{len(result)} 字符")
        else:
            print(f"  提取失败")
    
    # 保存为单个文件
    output_path = os.path.join(OUTPUT_DIR, "所有课后练习.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 三大计算带练 - 课后练习汇总\n\n")
        f.write("> 小崔说数\n\n")
        f.write("---\n\n")
        
        for section_name, content in all_exercises.items():
            f.write(f"## {section_name}\n\n")
            f.write(content)
            f.write("\n\n---\n\n")
    
    print(f"\n\n提取完成！已保存到: {output_path}")
    print(f"共提取 {len(all_exercises)} 个练习部分")

if __name__ == "__main__":
    main()
