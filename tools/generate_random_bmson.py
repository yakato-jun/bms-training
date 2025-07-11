#!/usr/bin/env python3
"""
乱打練習用BMSON生成
"""
import json
from random_patterns import RandomPatternGenerator

def create_random_bmson(bpm, chord_sizes, pattern_name, scratch_interval=None, scratch_probability=1.0):
    """乱打練習用BMSONを生成"""
    
    # パターンジェネレータを作成
    generator = RandomPatternGenerator(chord_sizes)
    notes, scratch_notes, metronome_notes = generator.generate_notes(bpm, 2, scratch_interval, scratch_probability)
    
    # タイトル設定
    if scratch_interval == 4:
        title = f"{pattern_name}＋4分皿 BPM{bpm}"
    elif scratch_interval == 8:
        title = f"{pattern_name}＋8分皿{int(scratch_probability*100)}% BPM{bpm}"
    elif scratch_interval == 16:
        title = f"{pattern_name}＋16分皿{int(scratch_probability*100)}% BPM{bpm}"
    else:
        title = f"{pattern_name} BPM{bpm}"
    
    bmson = {
        "version": "1.0.0",
        "info": {
            "title": title,
            "subtitle": "",
            "artist": "jun",
            "genre": "Practice",
            "mode_hint": "beat-7k",
            "chart_name": "HYPER",
            "level": 10,
            "judge_rank": 100,
            "total": 100.0,
            "init_bpm": float(bpm),
            "base_bpm": float(bpm)
        },
        "lines": [
            {"name": "", "kx": 1, "ky": 0},
            {"name": "", "kx": 2, "ky": 0},
            {"name": "", "kx": 3, "ky": 0},
            {"name": "", "kx": 4, "ky": 0},
            {"name": "", "kx": 5, "ky": 0},
            {"name": "", "kx": 6, "ky": 0},
            {"name": "", "kx": 7, "ky": 0},
            {"name": "", "kx": 8, "ky": -0.2}
        ],
        "bpm_events": [],
        "stop_events": [],
        "sound_channels": [
            {
                "name": "handclap.wav",
                "notes": notes
            },
            {
                "name": "scratch.wav",
                "notes": scratch_notes
            },
            {
                "name": "metronome.wav",
                "notes": metronome_notes
            }
        ]
    }
    
    return bmson

def generate_all_patterns():
    """全パターンのBMSONファイルを生成"""
    bpms = range(100, 260, 20)  # 100-240を20刻み
    
    pattern_configs = [
        ([1], "01_[1]乱打", "1_random"),
        ([1, 2], "02_[1, 2]乱打", "1_2_random"),
        ([1, 2, 2], "03_[1, 2, 2]乱打", "1_2_2_random"),
        ([1, 1, 2, 2, 3], "04_[1, 1, 2, 2, 3]乱打", "1_1_2_2_3_random"),
        ([1, 2, 3], "05_[1, 2, 3]乱打", "1_2_3_random"),
        ([1, 1, 1, 2, 2, 2, 3, 4], "06_[1, 1, 1, 2, 2, 2, 3, 4]乱打", "1_1_1_2_2_2_3_4_random"),
        ([1, 1, 1, 1, 2, 2, 2, 3, 3, 4], "07_[1, 1, 1, 2, 2, 2, 3, 3, 4]乱打", "1_1_1_2_2_2_3_3_4_random"),
        ([1, 2, 3, 4], "08_[1, 2, 3, 4]乱打", "1_2_3_4_random")
    ]
    
    scratch_configs = [
        (None, 1.0, ""),
        (4, 1.0, "_4th_scratch"),
        (8, 0.25, "_8th_scratch_25"),
        (8, 0.5, "_8th_scratch_50"),
        (16, 0.25, "_16th_scratch_25")
    ]
    
    for chord_sizes, pattern_name, filename_suffix in pattern_configs:
        for scratch_interval, scratch_probability, scratch_suffix in scratch_configs:
            # 8分皿と16分皿は[1]と[1,2]のみ
            if scratch_interval in [8, 16] and chord_sizes not in [[1], [1, 2], [1, 2, 2], [1, 1, 2, 2, 3]]:
                continue
                
            if scratch_interval:
                interval_name = f"{scratch_interval}分" if scratch_interval == 4 else f"{scratch_interval}分"
                prob_text = f"{int(scratch_probability*100)}%" if scratch_probability < 1.0 else ""
                print(f"=== {pattern_name}＋{interval_name}皿{prob_text} ===")
            else:
                print(f"=== {pattern_name} ===")
                
            for bpm in bpms:
                bmson = create_random_bmson(bpm, chord_sizes, pattern_name, scratch_interval, scratch_probability)
                filename = f"random_{filename_suffix}{scratch_suffix}_practice_bpm{bpm}.bmson"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(bmson, f, indent=2, ensure_ascii=False)
                
                print(f"Generated: {filename}")
            print()

if __name__ == "__main__":
    generate_all_patterns()