import fitz
import os

# PDF文件路径
pdf_path = r"d:\BaiduNetdiskDownload\27亲带班课程文件\02 基础阶段\01 基础段讲义&习题集\数一\小崔说数-基础段讲义_数一.pdf"

# 输出根目录
output_base_dir = r"d:\BaiduNetdiskDownload\27亲带班课程文件\02 基础阶段\01 基础段讲义&习题集\数一\PDF图片输出"

# 每文件夹页数
PAGES_PER_FOLDER = 50

# 打开PDF
doc = fitz.open(pdf_path)
total_pages = len(doc)
print(f"PDF总页数: {total_pages}")

# 计算需要多少个文件夹
num_folders = (total_pages + PAGES_PER_FOLDER - 1) // PAGES_PER_FOLDER
print(f"需要创建 {num_folders} 个文件夹")

# 创建输出根目录
os.makedirs(output_base_dir, exist_ok=True)

# 转换每一页为图片
for page_idx in range(total_pages):
    page = doc[page_idx]
    
    # 计算当前页属于哪个文件夹
    folder_idx = page_idx // PAGES_PER_FOLDER + 1
    folder_name = f"第{folder_idx}批_第{(folder_idx-1)*PAGES_PER_FOLDER+1}-{min(folder_idx*PAGES_PER_FOLDER, total_pages)}页"
    folder_path = os.path.join(output_base_dir, folder_name)
    
    # 创建文件夹
    os.makedirs(folder_path, exist_ok=True)
    
    # 设置缩放比例(2倍分辨率以保证清晰度)
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    
    # 保存图片(页码从1开始)
    page_num = page_idx + 1
    image_path = os.path.join(folder_path, f"第{page_num}页.png")
    pix.save(image_path)
    
    print(f"已转换第 {page_num}/{total_pages} 页")

doc.close()
print(f"\n转换完成! 所有图片已保存到: {output_base_dir}")
