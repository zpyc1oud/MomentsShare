import os

class DFAFilter:
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'
        self.parse_vocabulary()

    def parse_vocabulary(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vocab_dir = os.path.join(base_dir, 'Vocabulary')
        
        # 1. 目录不存在时的保护
        if not os.path.exists(vocab_dir):
            print(f"[DFA Warning] 目录未找到: {vocab_dir}，敏感词过滤将暂时失效。")
            return

        count = 0
        for root, dirs, files in os.walk(vocab_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    # 2. 核心修复：自动兼容 UTF-8 和 GBK 编码
                    content = ""
                    try:
                        # 先试 UTF-8
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        try:
                            # 失败了再试 GBK (常见的 Windows 格式)
                            with open(file_path, 'r', encoding='gbk') as f:
                                content = f.read()
                        except Exception as e:
                            print(f"[DFA Error] 无法读取文件 {file}: {e}")
                            continue
                    
                    # 3. 处理文件内容
                    for keyword in content.splitlines():
                        key = keyword.strip()
                        if key:
                            self.add(key)
                            count += 1
        
        print(f"[DFA Success] 敏感词库加载完毕，共 {count} 个词条。")

    def add(self, keyword):
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def exists(self, message):
        if not message:
            return False, None
        message = message.lower()
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit in level[char]:
                        return True, message[start:start+step_ins]
                    level = level[char]
                else:
                    break
            start += 1
        return False, None

# 单例模式
gfw = DFAFilter()