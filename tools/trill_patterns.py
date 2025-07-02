#!/usr/bin/env python3
"""
16分トリルパターン設計
2小節毎に異なる組み合わせで配置
"""

def generate_trill_patterns():
    """16分トリルの基本パターンを生成"""
    patterns = [
        # パターン1: 1-2トリル
        [(1, 2), (2, 1), (1, 2), (2, 1)],
        # パターン2: 2-3トリル  
        [(2, 3), (3, 2), (2, 3), (3, 2)],
        # パターン3: 3-4トリル
        [(3, 4), (4, 3), (3, 4), (4, 3)],
        # パターン4: 4-5トリル
        [(4, 5), (5, 4), (4, 5), (5, 4)],
        # パターン5: 5-6トリル
        [(5, 6), (6, 5), (5, 6), (6, 5)],
        # パターン6: 6-7トリル
        [(6, 7), (7, 6), (6, 7), (7, 6)],
        # パターン7: 1-3トリル (飛び)
        [(1, 3), (3, 1), (1, 3), (3, 1)],
        # パターン8: 2-4トリル (飛び)
        [(2, 4), (4, 2), (2, 4), (4, 2)],
        # パターン9: 3-5トリル (飛び)
        [(3, 5), (5, 3), (3, 5), (5, 3)],
        # パターン10: 4-6トリル (飛び)
        [(4, 6), (6, 4), (4, 6), (6, 4)],
    ]
    return patterns

def generate_bmson_notes(bpm, duration_minutes=2):
    """BMSONノート配列を生成"""
    resolution = 240  # 1拍の分解能
    beats_per_measure = 4
    measures_per_pattern = 2
    
    # 2分間の総拍数
    total_beats = bpm * duration_minutes * 2
    total_measures = total_beats // beats_per_measure
    
    patterns = generate_trill_patterns()
    notes = []
    scratch_notes = []
    metronome_notes = []
    
    current_y = 0
    pattern_index = 0
    
    for measure in range(total_measures):
        # 2小節毎にパターン変更
        if measure % measures_per_pattern == 0:
            current_pattern = patterns[pattern_index % len(patterns)]
            pattern_index += 1
        
        # 各小節の16分音符配置
        for beat in range(beats_per_measure):
            beat_y = current_y + (beat * resolution)
            
            # メトロノーム（4分音符毎）
            metronome_notes.append({
                "x": 0,  # BGMチャンネル
                "y": beat_y,
                "l": 0,
                "c": False
            })
            
            # 16分音符のトリル配置
            for sixteenth in range(4):
                note_y = beat_y + (sixteenth * resolution // 4)
                trill_index = sixteenth % len(current_pattern)
                lane1, lane2 = current_pattern[trill_index]
                
                # 交互にノート配置
                if sixteenth % 2 == 0:
                    notes.append({
                        "x": lane1,
                        "y": note_y,
                        "l": 0,
                        "c": False
                    })
                else:
                    notes.append({
                        "x": lane2,
                        "y": note_y,
                        "l": 0,
                        "c": False
                    })
        
        # 4分音符毎にスクラッチ
        for beat in range(beats_per_measure):
            scratch_y = current_y + (beat * resolution)
            scratch_notes.append({
                "x": 8,  # スクラッチレーン
                "y": scratch_y,
                "l": 0,
                "c": False
            })
        
        current_y += beats_per_measure * resolution
    
    return notes, scratch_notes, metronome_notes

if __name__ == "__main__":
    # テスト実行
    patterns = generate_trill_patterns()
    print(f"Generated {len(patterns)} trill patterns")
    for i, pattern in enumerate(patterns):
        print(f"Pattern {i+1}: {pattern}")