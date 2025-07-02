#!/usr/bin/env python3
"""
乱打パターン生成
16分音符で様々な同時押しパターンを生成
"""
import random

class RandomPatternGenerator:
    def __init__(self, chord_sizes):
        """
        chord_sizes: 同時押し数の配列
        - [1]: 単一鍵盤乱打
        - [1, 2]: 単一〜2鍵同時押し乱打
        - [1, 2, 3]: 単一〜3鍵同時押し乱打
        - [1, 2, 3, 4]: 単一〜4鍵同時押し乱打
        """
        self.chord_sizes = chord_sizes
        self.recent_notes = []  # 最近のノート履歴
        
    def generate_notes(self, bpm, duration_minutes=2, scratch_interval=None, scratch_probability=1.0):
        """16分乱打ノートを生成
        scratch_interval: None, 4(4分), 8(8分), 16(16分)
        scratch_probability: スクラッチを配置する確率 (0.0-1.0)
        """
        resolution = 240
        beats_per_measure = 4
        
        # 総小節数
        total_beats = int(bpm * duration_minutes)
        total_measures = total_beats // beats_per_measure
        
        notes = []
        scratch_notes = []
        metronome_notes = []
        
        current_y = 0
        
        for measure in range(total_measures):
            for beat in range(beats_per_measure):
                beat_y = current_y + (beat * resolution)
                
                # メトロノーム（4分音符）
                metronome_notes.append({
                    "x": 0,
                    "y": beat_y,
                    "l": 0,
                    "c": False
                })
                
                # 16分音符の乱打配置
                for sixteenth in range(4):
                    note_y = beat_y + (sixteenth * resolution // 4)
                    
                    # スクラッチ配置
                    if scratch_interval is not None:
                        # タイミングチェック
                        timing_match = False
                        if scratch_interval == 4 and sixteenth == 0:
                            timing_match = True
                        elif scratch_interval == 8 and sixteenth % 2 == 0:
                            timing_match = True
                        elif scratch_interval == 16:
                            timing_match = True
                        
                        # 確率チェック
                        if timing_match and random.random() < scratch_probability:
                            scratch_notes.append({
                                "x": 8,
                                "y": note_y,
                                "l": 0,
                                "c": False
                            })
                    
                    # 同時押し数を決定
                    chord_size = random.choice(self.chord_sizes)
                    
                    # 縦連禁止の制約を適用
                    # N=1,2: 完全に縦連禁止
                    # N=3: 1つまで縦連OK
                    # N=4: 2つまで縦連OK
                    allowed_repeat = max(0, chord_size - 2)
                    
                    # 利用可能なレーンを決定
                    available_lanes = list(range(1, 8))
                    
                    # 最近のノートから縦連を避ける
                    if self.recent_notes:
                        last_chord = self.recent_notes[-1]
                        
                        # 縦連を避けるべきレーンを特定
                        if allowed_repeat == 0:
                            # 完全に縦連禁止（N=1,2の場合）
                            forbidden_lanes = last_chord
                        else:
                            # 一部縦連OK（N=3,4の場合）
                            # ランダムに縦連を許可するレーンを選択
                            if len(last_chord) > allowed_repeat:
                                allowed_lanes = random.sample(last_chord, allowed_repeat)
                                forbidden_lanes = [lane for lane in last_chord if lane not in allowed_lanes]
                            else:
                                forbidden_lanes = []
                        
                        # 禁止レーンを除外
                        available_lanes = [lane for lane in available_lanes if lane not in forbidden_lanes]
                    
                    # 同時押しのレーンを選択
                    if len(available_lanes) >= chord_size:
                        selected_lanes = random.sample(available_lanes, chord_size)
                    else:
                        # 利用可能なレーンが足りない場合は全レーンから選択
                        selected_lanes = random.sample(range(1, 8), chord_size)
                    
                    # ノートを配置
                    for lane in selected_lanes:
                        notes.append({
                            "x": lane,
                            "y": note_y,
                            "l": 0,
                            "c": False
                        })
                    
                    # 履歴を更新
                    self.recent_notes.append(selected_lanes)
                    if len(self.recent_notes) > 1:
                        self.recent_notes.pop(0)
            
            # scratch_typeがNoneの場合は何もしない（既に処理済み）
            
            current_y += beats_per_measure * resolution
        
        return notes, scratch_notes, metronome_notes


def test_patterns():
    """パターンのテスト表示"""
    pattern_configs = [
        ([1], "単一鍵盤乱打"),
        ([1, 2], "単一〜2鍵同時押し乱打"),
        ([1, 2, 3], "単一〜3鍵同時押し乱打"),
        ([1, 2, 3, 4], "単一〜4鍵同時押し乱打")
    ]
    
    print("乱打パターンテスト（1小節分を表示）\n")
    
    for chord_sizes, description in pattern_configs:
        gen = RandomPatternGenerator(chord_sizes)
        notes, _, _ = gen.generate_notes(120, 0.1)  # 短いテスト
        
        print(f"=== {description} {chord_sizes} ===")
        # 16分音符ごとに表示
        current_y = -1
        beat_count = 0
        for note in notes[:64]:  # 最初の1小節分
            if note["y"] != current_y:
                current_y = note["y"]
                beat_count += 1
                # 同じy座標のノートをグループ化
                chord = sorted([n["x"] for n in notes if n["y"] == current_y])
                print(f"  16分{(beat_count-1)//4+1}-{(beat_count-1)%4+1}: レーン{chord} ({len(chord)}鍵)")
                if beat_count >= 16:
                    break
        print()


if __name__ == "__main__":
    test_patterns()