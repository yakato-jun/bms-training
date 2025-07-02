#!/usr/bin/env python3
"""
階段練習用BMSON生成
- 階段のみバージョン
- 階段＋4分皿バージョン
- 階段＋4分ゴミバージョン（過去3世代除外）
"""
import json
import random
from stair_patterns import StairPatternGenerator

def create_stair_bmson(bpm, difficulty, level, include_scratch=False, include_trash=False):
    """階段練習用BMSONを生成"""
    
    # 基本情報
    if include_trash:
        title_base = "階段＋ゴミ練習"
    elif include_scratch:
        title_base = "階段＋皿練習"
    else:
        title_base = "階段練習"
    
    bmson = {
        "version": "1.0.0",
        "info": {
            "title": f"{title_base} {difficulty.upper()} BPM{bpm}",
            "artist": "jun",
            "genre": "Practice",
            "mode_hint": "beat-7k",
            "chart_name": difficulty,
            "level": level,
            "judge_rank": 100,
            "total": 100.0,
            "init_bpm": float(bpm),
            "base_bpm": float(bpm)
        },
        "lines": [],
        "bpm_events": [],
        "stop_events": [],
        "sound_channels": [
            {
                "name": "handclap.wav",
                "notes": []
            },
            {
                "name": "scratch.wav", 
                "notes": []
            },
            {
                "name": "metronome.wav",
                "notes": []
            }
        ]
    }
    
    # 階段パターン生成
    generator = StairPatternGenerator()
    pattern_gen = generator.pattern_generator()
    
    resolution = 240
    beats_per_measure = 4
    duration_minutes = 5
    
    # 総小節数（5分を超えるまで2小節単位）
    total_beats = int(bpm * duration_minutes)
    total_measures = total_beats // beats_per_measure
    if total_measures % 2 != 0:
        total_measures += 1
    
    # パス1: 階段ノートを生成
    current_y = 0
    current_pattern = None
    pattern_position = 0
    stair_notes = []  # 階段ノートの位置を記録
    
    for measure in range(total_measures):
        # パターンが終了したら次のパターンを取得
        if current_pattern is None or pattern_position >= len(current_pattern['notes']):
            current_pattern = next(pattern_gen)
            pattern_position = 0
        
        # 1小節分のノートを配置
        for i in range(16):  # 16分音符16個
            note_y = current_y + (i * resolution // 4)
            
            # 階段ノート
            if pattern_position < len(current_pattern['notes']):
                lane = current_pattern['notes'][pattern_position]
                bmson["sound_channels"][0]["notes"].append({
                    "x": lane,
                    "y": note_y,
                    "l": 0,
                    "c": False
                })
                stair_notes.append((note_y, lane))
                pattern_position += 1
            
            # メトロノーム（4分音符）
            if i % 4 == 0:
                bmson["sound_channels"][2]["notes"].append({
                    "x": 0,
                    "y": note_y,
                    "l": 0,
                    "c": False
                })
                
                # スクラッチ（4分音符）
                if include_scratch:
                    bmson["sound_channels"][1]["notes"].append({
                        "x": 8,
                        "y": note_y,
                        "l": 0,
                        "c": False
                    })
        
        current_y += beats_per_measure * resolution
    
    # パス2: ゴミノートを追加
    if include_trash:
        for i, (y, lane) in enumerate(stair_notes):
            # 4分音符の位置（16分音符の2つおき）でゴミを配置
            if (y % resolution) == (resolution // 2):  # 2拍目と4拍目
                # 過去3つと未来2つのノートを確認
                excluded_lanes = set()
                
                # 過去3つ
                for j in range(max(0, i-3), i):
                    excluded_lanes.add(stair_notes[j][1])
                
                # 現在
                excluded_lanes.add(lane)
                
                # 未来2つ
                for j in range(i+1, min(i+3, len(stair_notes))):
                    excluded_lanes.add(stair_notes[j][1])
                
                # 利用可能なレーンから選択
                available_lanes = [x for x in range(1, 8) if x not in excluded_lanes]
                if available_lanes:
                    trash_lane = random.choice(available_lanes)
                    bmson["sound_channels"][0]["notes"].append({
                        "x": trash_lane,
                        "y": y,
                        "l": 0,
                        "c": False
                    })
    
    return bmson

def generate_stair_difficulties():
    """全難易度の階段譜面を生成"""
    difficulties = [
        (120, "beginner", 1),
        (140, "normal", 3),
        (160, "hyper", 5),
        (180, "another", 7),
        (200, "insane", 9)
    ]
    
    # 階段のみ
    print("=== 階段のみバージョン ===")
    for bpm, difficulty, level in difficulties:
        bmson = create_stair_bmson(bpm, difficulty, level, include_scratch=False, include_trash=False)
        filename = f"stair_practice_{difficulty}_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")
    
    # 階段＋4分皿
    print("\n=== 階段＋4分皿バージョン ===")
    for bpm, difficulty, level in difficulties:
        bmson = create_stair_bmson(bpm, difficulty, level, include_scratch=True, include_trash=False)
        filename = f"stair_scratch_practice_{difficulty}_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")
    
    # 階段＋4分ゴミ
    print("\n=== 階段＋4分ゴミバージョン ===")
    for bpm, difficulty, level in difficulties:
        bmson = create_stair_bmson(bpm, difficulty, level, include_scratch=False, include_trash=True)
        filename = f"stair_trash_practice_{difficulty}_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_stair_difficulties()