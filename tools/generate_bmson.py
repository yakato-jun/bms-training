#!/usr/bin/env python3
"""
BMSON生成スクリプト
"""
import json
import random
from trill_patterns import generate_bmson_notes

def create_bmson(bpm, include_scratch=False, include_trash=False, trash_type="4th"):
    """BMSON形式のデータを生成"""
    notes, scratch_notes, metronome_notes = generate_bmson_notes(bpm, 2)
    
    # タイトル設定
    if include_trash and trash_type == "8th":
        title = f"16分トリル＋8分ゴミ練習 BPM{bpm}"
    elif include_trash and trash_type == "4th":
        title = f"16分トリル＋4分ゴミ練習 BPM{bpm}"
    elif include_scratch:
        title = f"16分トリル＋皿練習 BPM{bpm}"
    else:
        title = f"16分トリル練習 BPM{bpm}"
    
    bmson = {
        "version": "1.0.0",
        "info": {
            "title": title,
            "subtitle": "",
            "artist": "jun",
            "subartists": [],
            "genre": "Practice",
            "mode_hint": "beat-7k",
            "chart_name": "HYPER",
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
                "notes": []  # 後で追加
            },
            {
                "name": "scratch.wav",
                "notes": []  # 後で追加
            }
        ]
    }
    
    # ノートを配置
    bmson["sound_channels"][1]["notes"] = notes
    
    # スクラッチを追加（4分音符）
    if include_scratch:
        bmson["sound_channels"][2]["notes"] = scratch_notes
    
    # ゴミノートを追加
    if include_trash:
        trash_notes = []
        trill_notes_dict = {}  # y座標でトリルノートを管理
        
        # トリルノートをy座標でインデックス化
        for note in notes:
            trill_notes_dict[note["y"]] = note["x"]
        
        # ゴミノートのタイミングを決定
        resolution = 240
        for note in notes:
            y = note["y"]
            place_trash = False
            
            if trash_type == "4th":
                # 4分音符の位置（2拍目と4拍目）
                if (y % resolution) == (resolution // 2):
                    place_trash = True
            elif trash_type == "8th":
                # 8分音符の位置（裏拍）
                if (y % (resolution // 2)) == (resolution // 4):
                    place_trash = True
            
            if place_trash:
                # 過去3つと未来2つのトリルレーンを確認
                excluded_lanes = set()
                
                # 現在のレーン
                excluded_lanes.add(note["x"])
                
                # 過去3つのレーンを確認
                for i in range(1, 4):
                    check_y = y - (i * resolution // 4)
                    if check_y in trill_notes_dict:
                        excluded_lanes.add(trill_notes_dict[check_y])
                
                # 未来2つのレーンを確認
                for i in range(1, 3):
                    check_y = y + (i * resolution // 4)
                    if check_y in trill_notes_dict:
                        excluded_lanes.add(trill_notes_dict[check_y])
                
                # 利用可能なレーンから選択
                available_lanes = [x for x in range(1, 8) if x not in excluded_lanes]
                if available_lanes:
                    trash_lane = random.choice(available_lanes)
                    trash_notes.append({
                        "x": trash_lane,
                        "y": y,
                        "l": 0,
                        "c": False
                    })
        
        # ゴミノートを追加
        bmson["sound_channels"][1]["notes"].extend(trash_notes)
    
    return bmson

def generate_all_difficulties():
    """全BPMのBMSONファイルを生成"""
    bpms = range(100, 240, 20)  # 100-220を20刻み
    
    # トリルのみ
    print("=== トリルのみバージョン ===")
    for bpm in bpms:
        bmson = create_bmson(bpm, include_scratch=False, include_trash=False)
        filename = f"trill_practice_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")
    
    # トリル＋4分皿
    print("\n=== トリル＋4分皿バージョン ===")
    for bpm in bpms:
        bmson = create_bmson(bpm, include_scratch=True, include_trash=False)
        filename = f"trill_scratch_practice_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")
    
    # トリル＋4分ゴミ
    print("\n=== トリル＋4分ゴミバージョン ===")
    for bpm in bpms:
        bmson = create_bmson(bpm, include_scratch=False, include_trash=True, trash_type="4th")
        filename = f"trill_trash_4th_practice_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")
    
    # トリル＋8分ゴミ
    print("\n=== トリル＋8分ゴミバージョン ===")
    for bpm in bpms:
        bmson = create_bmson(bpm, include_scratch=False, include_trash=True, trash_type="8th")
        filename = f"trill_trash_8th_practice_bpm{bpm}.bmson"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(bmson, f, indent=2, ensure_ascii=False)
        
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_all_difficulties()