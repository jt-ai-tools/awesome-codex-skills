import os

def scan_files():
    target_extensions = ('.md', '.txt')
    exclude_dirs = {'.git', 'node_modules', 'scripts', '.gemini'}
    exclude_files = {'PROGRESS.md'}
    
    files_to_translate = []
    
    for root, dirs, files in os.walk('.'):
        # 移除排除目錄
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(target_extensions) and not file.endswith('_zh_TW.md') and file not in exclude_files:
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                files_to_translate.append(rel_path)
    
    files_to_translate.sort()
    
    with open('PROGRESS.md', 'w', encoding='utf-8') as f:
        f.write('# 翻譯進度追蹤 (Translation Progress Tracking)\n\n')
        f.write('## 任務說明\n')
        f.write('- [ ] 將所有 `.md` 與 `.txt` 檔案翻譯為繁體中文（台灣慣用語）。\n')
        f.write('- [ ] 翻譯後的檔名應為 `[原始檔名]_zh_TW.md`。\n')
        f.write('- [ ] 修正所有中文版文件中的內部連結，指向對應的 `_zh_TW.md` 檔案。\n\n')
        f.write('## 檔案清單\n\n')
        for file in files_to_translate:
            f.write(f'- [ ] {file}\n')

if __name__ == "__main__":
    scan_files()
