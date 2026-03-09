import re
import threading
import time

import mido


def open_midi_port(search_str: str, is_input: bool = False):
    names = mido.get_input_names() if is_input else mido.get_output_names()
    for name in names:
        if search_str in name:
            return mido.open_input(name) if is_input else mido.open_output(name)
    return None


def monitor_midi_input(midi_in, state, history_timeout: float = 10.0):
    if not midi_in:
        print("MIDI入力ポートが見つかりませんでした。")
        return

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    for msg in midi_in:
        if msg.type == "note_on" and msg.velocity > 0:
            note_name = f"{notes[msg.note % 12]}{msg.note // 12 - 1}"
            now = time.time()

            state.add_midi_event(
                {
                    "note": note_name,
                    "velocity": msg.velocity,
                    "time": now,
                },
                window_sec=history_timeout,
            )
            print(f"★演奏検知: {note_name}")


def play_midi_note(midi_out, note_data: dict):
    if not midi_out:
        return

    try:
        note_names = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11,
        }

        match = re.match(r"([A-G]#?)(\d)", note_data["note"])
        if not match:
            return

        name, octave = match.groups()
        note_num = (int(octave) + 1) * 12 + note_names[name]

        start_time = float(note_data.get("time", 0.0))
        duration_raw = str(note_data.get("duration", "0.5s"))
        duration_sec = float(duration_raw.replace("s", ""))

        time.sleep(start_time)
        midi_out.send(mido.Message("note_on", note=note_num, velocity=80))
        time.sleep(duration_sec)
        midi_out.send(mido.Message("note_off", note=note_num, velocity=80))

    except Exception as e:
        print(f"MIDI再生エラー: {e}")


def start_midi_monitor_thread(midi_in, state, history_timeout: float = 10.0):
    threading.Thread(
        target=monitor_midi_input,
        args=(midi_in, state, history_timeout),
        daemon=True,
    ).start()