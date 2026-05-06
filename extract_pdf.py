import fitz

pdf_path = r'd:\study\301\27亲带班课程文件\03 计算带练\01 三大计算带练讲义&答案\小崔说数-三大计算带练讲义.pdf'
doc = fitz.open(pdf_path)

text = ""
for page in doc:
    text += page.get_text()

with open(r'd:\study\301\pdf_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Total pages: {doc.page_count}")
print(f"Total characters: {len(text)}")
print("\n--- First 5000 characters ---\n")
print(text[:5000])
