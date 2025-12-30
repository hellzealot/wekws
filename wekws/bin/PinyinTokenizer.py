from typing import List, Dict
import sys
from wenet.text.base_tokenizer import BaseTokenizer

# 如果 BaseTokenizer 在项目中定义了，请保留继承，否则可以去掉 (BaseTokenizer)
# from wekws.utils.tokenizer import BaseTokenizer 

class PinyinTokenizer(BaseTokenizer):
    def __init__(
        self,
        symbol_table_path: str,
        unk: str = '<unk>',
    ) -> None:
        self.p2idx = {}
        self.idx2p = {}
        self.unk = unk
        
        # 1. 加载词典文件 (units.txt)
        # 假设文件格式为每一行: "token id" (例如: "wo3 125")
        self._load_symbol_table(symbol_table_path)
        
        # 2. 获取 <unk> 的 ID，如果词典里没有 <unk>，默认给 1 (通常 0 是 <blank>)
        self.unk_id = self.p2idx.get(self.unk, 1) 
        self.connect_symbol = " "

    def _load_symbol_table(self, symbol_table_path: str):
        """加载 units.txt 生成映射表"""
        try:
            with open(symbol_table_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    
                    # 确保格式正确，至少有 token 和 id
                    if len(parts) >= 2:
                        token = parts[0]
                        idx = int(parts[-1])
                        self.p2idx[token] = idx
                        self.idx2p[idx] = token
        except FileNotFoundError:
            print(f"Error: Symbol table file not found at {symbol_table_path}")
            sys.exit(1)

    def text2tokens(self, line: str) -> List[str]:
        """
        直接读取已经转换好的拼音字符串。
        输入: "kou3 kou3 yin1 yue4"
        输出: ['kou3', 'kou3', 'yin1', 'yue4']
        """
        line = line.strip()
        if not line:
            return []
        # 直接按空格分割即可
        tokens = line.split(self.connect_symbol)
        filtered = [s for s in tokens if s]
        return filtered

    def tokens2text(self, tokens: List[str]) -> str:
        """将 token 列表拼接回字符串"""
        return self.connect_symbol.join(tokens)

    def tokens2ids(self, tokens: List[str]) -> List[int]:
        """将拼音 Token 转换为 ID"""
        ids = []
        for token in tokens:
            if token in self.p2idx:
                ids.append(self.p2idx[token])
            else:
                # 遇到词典里没有的拼音，映射为 <unk>
                ids.append(self.unk_id)
                print(f"Unknow token:{token}")
        return ids

    def ids2tokens(self, ids: List[int]) -> List[str]:
        """将 ID 转换为拼音 Token"""
        content = []
        for w in ids:
            # 兼容处理：如果 ID 越界或不存在，返回 <unk>
            token = self.idx2p.get(w, self.unk)
            content.append(token)
        return content

    def vocab_size(self) -> int:
        return len(self.p2idx)

    @property
    def symbol_table(self) -> Dict[str, int]:
        return self.p2idx

# --- 使用示例 ---
if __name__ == "__main__":
    # 假设 symbol_table_path 指向你之前生成的 units.txt
    # 模拟一个 units.txt 文件用于测试
    with open("temp_units.txt", "w") as f:
        f.write("<blank> 0\n<unk> 1\n<sil> 2\nkou3 100\nyin1 101\nyue4 102\n")

    tokenizer = PinyinTokenizer(symbol_table_path="temp_units.txt")

    # 模拟数据中的 txt 字段
    data_txt = "kou3 kou3 yin1 yue4 beyond <unk> <sil>"
    
    # 1. 解析
    tokens = tokenizer.text2tokens(data_txt)
    print(f"Tokens: {tokens}")
    # Output: ['kou3', 'kou3', 'yin1', 'yue4']

    # 2. 转 ID
    ids = tokenizer.tokens2ids(tokens)
    print(f"IDs: {ids}")
    # Output: [100, 100, 101, 102]

    # 3. 还原
    restored = tokenizer.ids2tokens(ids)
    print(f"Restored: {restored}")
    
    import os
    os.remove("temp_units.txt")