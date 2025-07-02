#!/usr/bin/env python3
"""
階段パターン生成
最低2小節単位で様々な階段パターンを生成
"""
import random

class StairPatternGenerator:
    def __init__(self, use_rest=False):
        self.use_rest = use_rest
        self.used_patterns = []
        self.last_note = None  # 最後のノートを記録
        
    def pattern_generator(self):
        """階段パターンを無限に生成するジェネレータ"""
        pattern_types = [
            "4_stairs_repeat",
            "5_stairs_repeat", 
            "6_stairs_repeat",
            "large_stair",
            "spiral_4",
            "spiral_5",
            "spiral_6",
            "spiral_large",
            "slide_4_stairs",
            "slide_5_stairs",
        ]
        
        while True:
            # 使用済みでないパターンから選択
            available = [p for p in pattern_types if p not in self.used_patterns]
            if not available:
                self.used_patterns = []
                available = pattern_types.copy()
            
            pattern_type = random.choice(available)
            self.used_patterns.append(pattern_type)
            
            # パターンを生成
            pattern = None
            if pattern_type == "4_stairs_repeat":
                pattern = self._generate_repeat_stairs(4)
            elif pattern_type == "5_stairs_repeat":
                pattern = self._generate_repeat_stairs(5)
            elif pattern_type == "6_stairs_repeat":
                pattern = self._generate_repeat_stairs(6)
            elif pattern_type == "large_stair":
                pattern = self._generate_large_stair()
            elif pattern_type == "spiral_4":
                pattern = self._generate_spiral_stairs(4)
            elif pattern_type == "spiral_5":
                pattern = self._generate_spiral_stairs(5)
            elif pattern_type == "spiral_6":
                pattern = self._generate_spiral_stairs(6)
            elif pattern_type == "spiral_large":
                pattern = self._generate_spiral_large()
            elif pattern_type == "slide_4_stairs":
                pattern = self._generate_slide_stairs(4)
            elif pattern_type == "slide_5_stairs":
                pattern = self._generate_slide_stairs(5)
            
            # 縦連チェック：最初の音が前のパターンの最後の音と同じ場合は調整
            if pattern and self.last_note is not None:
                if pattern['notes'][0] == self.last_note:
                    # 最初の音を削除
                    pattern['notes'].pop(0)
            
            # 最後の音を記録
            if pattern and pattern['notes']:
                self.last_note = pattern['notes'][-1]
            
            yield pattern
    
    def _generate_repeat_stairs(self, width):
        """同じ位置で繰り返す階段"""
        start = random.randint(1, 8 - width)
        direction = random.choice(['up', 'down'])
        
        if direction == 'up':
            sequence = list(range(start, start + width))
        else:
            sequence = list(range(start + width - 1, start - 1, -1))
        
        # 2小節分（32音）を埋める
        pattern = []
        for _ in range(32 // width):
            pattern.extend(sequence)
        # 余りを埋める
        remaining = 32 - len(pattern)
        if remaining > 0:
            pattern.extend(sequence[:remaining])
        
        return {
            "type": f"{width}_stairs_repeat_{direction}",
            "notes": pattern,
            "measures": 2
        }
    
    def _generate_large_stair(self):
        """大階段（7鍵）"""
        direction = random.choice(['up', 'down'])
        
        if direction == 'up':
            sequence = list(range(1, 8))  # 1-7
        else:
            sequence = list(range(7, 0, -1))  # 7-1
        
        # 2小節分（32音）を埋める
        pattern = []
        for _ in range(32 // 7):
            pattern.extend(sequence)
        # 余り（4音）
        pattern.extend(sequence[:4])
        
        return {
            "type": f"large_stair_{direction}",
            "notes": pattern,
            "measures": 2
        }
    
    def _generate_spiral_stairs(self, width):
        """螺旋階段（往復）"""
        start = random.randint(1, 8 - width)
        direction = random.choice(['up', 'down'])
        
        # 繰り返し用：折り返し地点の音を1つだけにする
        if direction == 'up':
            first = list(range(start, start + width))
            second = list(range(start + width - 2, start, -1))  # 最初の音まで戻らない
        else:
            first = list(range(start + width - 1, start - 1, -1))
            second = list(range(start + 1, start + width - 1))  # 最後の音まで行かない
        
        sequence = first + second  # 例：[4,3,2,1,2,3] = 6音（width=4の場合）
        
        # 4小節分（64音）を埋める
        pattern = []
        cycle_length = len(sequence)
        for _ in range(64 // cycle_length):
            pattern.extend(sequence)
        # 余りを埋める
        remaining = 64 - len(pattern)
        if remaining > 0:
            pattern.extend(sequence[:remaining])
        
        return {
            "type": f"spiral_{width}_{direction}",
            "notes": pattern,
            "measures": 4
        }
    
    def _generate_spiral_large(self):
        """螺旋大階段（7鍵往復）"""
        direction = random.choice(['up', 'down'])
        
        # 繰り返し用：12音サイクル
        if direction == 'up':
            sequence = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2]
        else:
            sequence = [7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6]
        
        # 4小節分（64音）を埋める
        pattern = []
        for _ in range(64 // 12):
            pattern.extend(sequence)
        # 余り（4音）
        pattern.extend(sequence[:4])
        
        return {
            "type": f"spiral_large_{direction}",
            "notes": pattern,
            "measures": 4
        }
    
    def _generate_slide_stairs(self, width):
        """スライド階段（移動階段）"""
        pattern = []
        stair_direction = random.choice(['up', 'down'])
        
        # 2小節分（32音）を埋める
        position = 1
        slide_direction = 1  # 1:右移動, -1:左移動
        
        while len(pattern) < 32:
            # 現在位置から階段
            if stair_direction == 'up':
                stairs = list(range(position, position + width))
            else:
                stairs = list(range(position + width - 1, position - 1, -1))
            pattern.extend(stairs)
            
            # 次の位置を決定
            position += slide_direction
            # 境界チェック
            if position + width > 8:
                position = 8 - width
                slide_direction = -1
            elif position < 1:
                position = 1
                slide_direction = 1
        
        # 32音に調整
        pattern = pattern[:32]
        
        return {
            "type": f"slide_{width}_stairs_{stair_direction}",
            "notes": pattern,
            "measures": 2
        }


def test_patterns():
    """パターンのテスト表示"""
    gen = StairPatternGenerator()
    pattern_gen = gen.pattern_generator()
    
    print("階段パターンテスト（4小節分を表示）\n")
    
    # 5種類のパターンを生成
    for i in range(5):
        pattern1 = next(pattern_gen)
        pattern2 = next(pattern_gen)
        
        print(f"=== パターン {i+1} ===")
        print(f"タイプ: {pattern1['type']} → {pattern2['type']}")
        
        # 最初のパターン
        print(f"\n{pattern1['type']} ({pattern1['measures']}小節):")
        for measure in range(pattern1['measures']):
            start = measure * 16
            end = start + 16
            notes = pattern1['notes'][start:end]
            print(f"  小節{measure+1}: {notes}")
        
        # 2つ目のパターン（4小節まで表示）
        remaining_measures = 4 - pattern1['measures']
        if remaining_measures > 0:
            print(f"\n{pattern2['type']} ({min(pattern2['measures'], remaining_measures)}小節):")
            for measure in range(min(pattern2['measures'], remaining_measures)):
                start = measure * 16
                end = start + 16
                notes = pattern2['notes'][start:end]
                print(f"  小節{pattern1['measures']+measure+1}: {notes}")
        
        print()


if __name__ == "__main__":
    test_patterns()