from typing import Dict, List
from wenet.text.base_tokenizer import BaseTokenizer


class EnglishTokenizer(BaseTokenizer):
    def __init__(
        self,
        unk='<unk>',
    ) -> None:
        self.phonemes = ['<blank>','AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0',
                                                             'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'B', 'CH', 'D', 'DH',
                                                             'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1',
                                                             'EY2', 'F', 'G', 'HH',
                                                             'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'JH', 'K', 'L',
                                                             'M', 'N', 'NG', 'OW0', 'OW1',
                                                             'OW2', 'OY0', 'OY1', 'OY2', 'P', 'R', 'S', 'SH', 'T', 'TH',
                                                             'UH0', 'UH1', 'UH2', 'UW',
                                                             'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', 'Z', 'ZH']
        
        self.p2idx = {p: idx for idx, p in enumerate(self.phonemes)}
        self.idx2p = {idx: p for idx, p in enumerate(self.phonemes)}
        self.connect_symbol = " "
        self.unk = unk

    def text2tokens(self, line: str) -> List[str]:
        line = line.strip()
        splits = line.split(" ")

        tokens = []
        for part in splits:
            tokens.append(part)
        return tokens

    def tokens2text(self, tokens: List[str]) -> str:
        return self.connect_symbol.join(tokens)

    def tokens2ids(self, tokens: List[str]) -> List[int]:
        ids = []
        for ch in tokens:
            if ch in self.phonemes:
                ids.append(self.p2idx[ch])
            else:
                ids.append(0)
        return ids

    def ids2tokens(self, ids: List[int]) -> List[str]:
        content = [self.idx2p[w] for w in ids]
        return content

    def vocab_size(self) -> int:
        return len(self.phonemes)

    @property
    def symbol_table(self) -> Dict[str, int]:
        return self.p2idx
