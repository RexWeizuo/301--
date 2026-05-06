import fitz
from PIL import Image
import io
import os

pdf_path = r'd:\study\301\27亲带班课程文件\03 计算带练\01 三大计算带练讲义&答案\小崔说数-三大计算带练讲义.pdf'
output_dir = r'd:\study\301\pdf_images'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)

print(f"Total pages: {doc.page_count}")

for page_num in range(doc.page_count):
    page = doc[page_num]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(os.path.join(output_dir, f'page_{page_num+1:03d}.png'))
    print(f"Saved page {page_num+1}")

doc.close()
print("All pages extracted as images!")
