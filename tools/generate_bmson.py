#!/usr/bin/env python3
"""
BMSON生成スクリプト
"""
import json
from trill_patterns import generate_bmson_notes

def create_bmson(bpm, difficulty_name):
    """BMSON形式のデータを生成"""
    notes, scratch_notes, metronome_notes = generate_bmson_notes(bpm, 2)
    
    bmson = {
        "version": "1.0.0",
        "info": {
            "title": "16分トリル練習",
            "subtitle": f"BPM{bpm}",
            "artist": "jun",
            "subartists": [],
            "genre": "Practice",
            "mode_hint": "beat-7k",
            "chart_name": difficulty_name,
            "level": 10,
            "init_bpm": float(bpm),
            "judge_rank": 100,
            "total": 200.0,
            "back_image": "",
            "eyecatch_image": "",
            "banner_image": "",
            "preview_music": "",
            "resolution": 240
        },
        "lines": [
            {"name": "", "kx": 1, "ky": 0},  # 1key
            {"name": "", "kx": 2, "ky": 0},  # 2key
            {"name": "", "kx": 3, "ky": 0},  # 3key
            {"name": "", "kx": 4, "ky": 0},  # 4key
            {"name": "", "kx": 5, "ky": 0},  # 5key
            {"name": "", "kx": 6, "ky": 0},  # 6key
            {"name": "", "kx": 7, "ky": 0},  # 7key
            {"name": "", "kx": 8, "ky": -0.2} # scratch
        ],
        "bpm_events": [
            {"y": 0, "bpm": float(bpm)}
        ],
        "stop_events": [],
        "sound_channels": [
            {
                "name": "metronome.wav",
                "notes": metronome_notes
            },
            {
                "name": "handclap.wav", 
                "notes": notes
            },
            {
                "name": "scratch.wav",
                "notes": scratch_notes
            }
        ]
    }
    
    return bmson

def generate_all_difficulties():
    """全難易度のBMSONファイルを生成"""
    difficulties = [
        (120, "P", "practice"),
        (140, "N", "normal"),
        (160, "H", "hyper"),
        (180, "A", "another"),
        (200, "I", "insane")
    ]
    
    for bpm, difficulty_name, filename_suffix in difficulties:
        bmson = create_bmson(bpm, difficulty_name)
        filename = f"trill_practice_{filename_suffix}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_all_difficulties()