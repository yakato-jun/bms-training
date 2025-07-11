# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a BMS (Beat Mania Style) practice song generation project for beatoraja. The project generates BMSON (BMS Object Notation) format practice songs with different difficulty levels and BPM settings.

## Architecture

### Core Components

- **Pattern Generation**: `tools/trill_patterns.py` contains the core algorithm for generating 16th note trill patterns that change every 2 measures
- **BMSON Generation**: `tools/generate_bmson.py` creates complete BMSON files with proper metadata, timing, and note placement
- **Practice Songs**: Generated songs are placed in `practice_songs/` folders ready for beatoraja registration

### BMSON Format Structure

- **Resolution**: 240 ticks per beat (standard for BMS)
- **Lane Mapping**: 7-key mode (lanes 1-7) + scratch (lane 8)
- **Sound Channels**: Separate channels for handclap, scratch, and metronome sounds
- **Timing**: Uses y-coordinate system where each beat = 240 ticks

### Pattern System

The trill pattern generator creates 10 different patterns:
- Adjacent key trills (1-2, 2-3, 3-4, 4-5, 5-6, 6-7)
- Skip key trills (1-3, 2-4, 3-5, 4-6)
- Patterns rotate every 2 measures to provide variety

## Key Development Commands

### Generate New Practice Songs
```bash
cd /home/lexxauto/bms-training/tools
python3 generate_bmson.py
python3 generate_random_bmson.py
python3 generate_stair_bmson.py
```

**重要**: 生成後は必ず正しいディレクトリに移動してください：
- トリル練習: `mv trill_*.bmson ../practice_songs/01_trill_practice/`
- 階段練習: `mv stair_*.bmson ../practice_songs/02_stair_practice/`
- 乱打練習: `mv random_*.bmson ../practice_songs/03_random_practice/`

### Test Pattern Generation
```bash
cd /home/lexxauto/bms-training/tools
python3 trill_patterns.py
python3 random_patterns.py
python3 stair_patterns.py
```

### Create New Practice Song
1. Create folder: `practice_songs/XX_new_practice/`
2. Copy sounds from `shared_sounds/`
3. Generate BMSON files using tools
4. Register folder in beatoraja

## File Organization

- `practice_songs/`: Completed songs ready for beatoraja (each subfolder is a complete song set)
- `shared_sounds/`: Common audio files used across multiple songs
- `tools/`: Python scripts for generating BMSON files
- `soundset/`: Original source audio files

## Audio Requirements

Each practice song requires:
- `handclap.wav`: Key press sound
- `scratch.wav`: Turntable scratch sound  
- `metronome.wav`: Quiet metronome click for timing reference

## Difficulty Progression

Standard 5-difficulty setup:
- beginner: BPM 120, Level 1
- normal: BPM 140, Level 3
- hyper: BPM 160, Level 5
- another: BPM 180, Level 7
- insane: BPM 200, Level 9

## Adding New Practice Types

When creating new practice song types:
1. Create pattern generation function in `tools/`
2. Modify `generate_bmson.py` or create new generator
3. Follow the established folder structure in `practice_songs/`
4. Ensure proper BMSON metadata (title, artist, genre, mode_hint)
5. Test with beatoraja before finalizing

## Development Guidelines

- Always use TodoWrite tool to track multi-step tasks
- Keep responses concise (fewer than 4 lines unless detail requested)
- Only create files when explicitly necessary
- Prefer editing existing files over creating new ones
- Never create documentation files unless explicitly requested
- BMSON files should follow the established 240-resolution standard