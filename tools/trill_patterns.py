#!/usr/bin/env python3
"""
16分トリルパターン設計
2小節毎に異なる組み合わせで配置
"""
import random
import itertools

def trill_pattern_generator():
    """トリルパターンを無限に生成するジェネレータ"""
    # 利用可能なレーン（1-7）
    available_lanes = list(range(1, 8))
    used_patterns = []
    
    # 可能な全ての2つのレーンの組み合わせを生成
    all_combinations = list(itertools.combinations(available_lanes, 2))
    
    while True:
        # 使用済みパターンを除外した候補を作成
        candidates = [combo for combo in all_combinations if combo not in used_patterns]
        
        # 候補がない場合は使用済みパターンをリセット
        if not candidates:
            used_patterns = []
            candidates = all_combinations.copy()
        
        # ランダムに選択
        selected = random.choice(candidates)
        used_patterns.append(selected)
        
        yield selected

def generate_bmson_notes(bpm, duration_minutes=2):
    """BMSONノート配列を生成"""
    resolution = 240  # 1拍の分解能
    beats_per_measure = 4
    measures_per_pattern = 2
    
    # 2分を超えるまで2小節単位で生成
    # 2分間の総拍数を計算し、2小節単位に切り上げ
    total_beats = bpm * duration_minutes * 2
    total_measures = total_beats // beats_per_measure
    # 2小節単位に切り上げ
    if total_measures % measures_per_pattern != 0:
        total_measures = ((total_measures // measures_per_pattern) + 1) * measures_per_pattern
    
    pattern_gen = trill_pattern_generator()
    notes = []
    scratch_notes = []
    metronome_notes = []
    
    current_y = 0
    current_pattern = None
    
    for measure in range(total_measures):
        # 2小節毎にパターン変更
        if measure % measures_per_pattern == 0:
            current_pattern = next(pattern_gen)
        
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
                # トリルの2つのレーンを交互に配置
                lane1, lane2 = current_pattern
                
                # 16分音符ごとに交互配置
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
    gen = trill_pattern_generator()
    print("Generating trill patterns:")
    for i in range(10):
        pattern = next(gen)
        print(f"Pattern {i+1}: {pattern[0]}-{pattern[1]}")