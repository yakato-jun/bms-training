#!/usr/bin/env python3
from random_patterns import RandomPatternGenerator

# 各パターンでテスト
patterns = [
    ([1], '単一'),
    ([3], '3鍵'),
    ([3, 4], '3-4鍵')
]

for chord_sizes, name in patterns:
    gen = RandomPatternGenerator(chord_sizes)
    notes, _, _ = gen.generate_notes(120, 0.01)
    
    # 縦連チェック
    prev_lanes = None
    vertical_violations = 0
    max_vertical = 0
    
    print(f'\n=== {name} ===')
    
    # 最初の10個をサンプル表示
    prev_y = -1
    count = 0
    for i, note in enumerate(notes[:100]):
        if note['y'] != prev_y:
            prev_y = note['y']
            curr_lanes = sorted([n['x'] for n in notes if n['y'] == prev_y])
            
            # 縦連チェック
            if prev_lanes:
                vertical = len(set(prev_lanes) & set(curr_lanes))
                allowed = max(0, len(curr_lanes) - 2)
                if vertical > allowed:
                    vertical_violations += 1
                    max_vertical = max(max_vertical, vertical)
            
            print(f'16分{count+1}: レーン{curr_lanes} (N={len(curr_lanes)})')
            prev_lanes = curr_lanes
            count += 1
            if count >= 10:
                break
    
    print(f'縦連違反: {vertical_violations}回, 最大縦連数: {max_vertical}')