import os
import re

def finalize():
    exclude_dirs = {'.git', 'node_modules', 'scripts', '.gemini'}
    # 這裡列出不翻譯的檔案關鍵字或路徑
    exclude_patterns = ['LICENSE', 'OFL.txt', 'PROGRESS.md', 'requirements.txt']
    
    # 1. 掃描檔案，建立映射表
    en_to_tw = {}
    all_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(('.md', '.txt')):
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                all_files.append(rel_path)
                if not rel_path.endswith('_zh_TW.md') and not any(p in rel_path for p in exclude_patterns):
                    # 預期要有對應的 _zh_TW 檔案
                    tw_path = rel_path.rsplit('.', 1)[0] + '_zh_TW.md'
                    if os.path.exists(tw_path):
                        en_to_tw[rel_path] = tw_path
                    else:
                        print(f"Missing translation for: {rel_path}")

    # 2. 修正中文版檔案中的連結
    # 我們要尋找 [Label](path/to/file.md) 並將其改為 [Label](path/to/file_zh_TW.md)
    # 如果路徑中有 #anchor 也要處理
    
    tw_files = [f for f in all_files if f.endswith('_zh_TW.md')]
    
    for tw_file in tw_files:
        with open(tw_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        
        # 尋找 Markdown 連結： [text](link)
        # Regex: \[([^\]]+)\]\(([^)]+)\)
        def link_replacer(match):
            label = match.group(1)
            link = match.group(2)
            
            # 排除網路連結
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                return match.group(0)
            
            # 拆分路徑與錨點
            base_link = link
            anchor = ""
            if '#' in link:
                base_link, anchor = link.split('#', 1)
                anchor = '#' + anchor
            
            if base_link.endswith(('.md', '.txt')) and not base_link.endswith('_zh_TW.md'):
                # 取得目標檔案的絕對相對路徑
                current_dir = os.path.dirname(tw_file)
                target_abs_rel = os.path.normpath(os.path.join(current_dir, base_link))
                
                # 如果該檔案有對應的中文版
                if target_abs_rel in en_to_tw:
                    # 改為中文版連結
                    new_base = base_link.rsplit('.', 1)[0] + '_zh_TW.md'
                    # print(f"Updating link in {tw_file}: {link} -> {new_base}{anchor}")
                    return f"[{label}]({new_base}{anchor})"
            
            return match.group(0)

        updated_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, updated_content)
        
        if updated_content != content:
            with open(tw_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            # print(f"Fixed links in {tw_file}")

    print("Finalization complete.")

if __name__ == "__main__":
    finalize()
