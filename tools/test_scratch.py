#!/usr/bin/env python3
from random_patterns import RandomPatternGenerator

# 各皿パターンでテスト（2分間）
configs = [
    (4, 1.0, "4分皿100%"),
    (8, 0.25, "8分皿25%"),
    (16, 0.125, "16分皿12.5%")
]

for interval, prob, name in configs:
    gen = RandomPatternGenerator([1])  # 単一鍵盤で単純化
    notes, scratch_notes, metronome_notes = gen.generate_notes(120, 2, interval, prob)
    
    # 理論値を計算
    total_beats = 120 * 2  # BPM120で2分間
    if interval == 4:
        expected = total_beats  # 4分音符の数
        expected_actual = expected * prob
    elif interval == 8:
        expected = total_beats * 2  # 8分音符の数
        expected_actual = expected * prob
    elif interval == 16:
        expected = total_beats * 4  # 16分音符の数
        expected_actual = expected * prob
    
    actual = len(scratch_notes)
    print(f"\n{name}:")
    print(f"  期待値: {expected_actual:.1f}")
    print(f"  実際: {actual}")
    print(f"  割合: {actual/expected*100:.1f}%")