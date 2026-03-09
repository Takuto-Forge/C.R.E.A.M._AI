import json
import re
import threading


def extract_json_from_response(content: str) -> dict | None:
    try:
        json_match = re.search(r"(\{[\s\S]*\})", content)
        if not json_match:
            print("JSON抽出失敗: レスポンス内にJSONが見つかりません。")
            return None
        return json.loads(json_match.group(1))
    except Exception as e:
        print(f"JSON解析エラー: {e}")
        return None


def normalize_sequence(raw_sequence: list) -> list[dict]:
    valid_notes = []

    for item in raw_sequence:
        if isinstance(item, dict) and "note" in item:
            valid_notes.append(item)
        elif isinstance(item, str):
            valid_notes.append(
                {
                    "note": item,
                    "time": len(valid_notes) * 0.2,
                    "duration": "0.5s",
                }
            )

    return valid_notes


def process_and_dispatch_generation(
    content: str,
    osc_client,
    midi_out,
    state,
    play_midi_note_func,
):
    try:
        data = extract_json_from_response(content)
        if not data:
            return None

        interp_text = data.get("interpretation", "思考中...")
        print(f"AIの意図: {interp_text}")

        v_params = data.get("visual_params", {})
        energy = float(v_params.get("energy", 0.5))
        complexity = float(v_params.get("complexity", 0.5))
        color_mood = str(v_params.get("color_mood", "neutral"))

        osc_client.send_message("/music/energy", energy)
        osc_client.send_message("/music/complexity", complexity)
        osc_client.send_message("/music/mood", color_mood)
        osc_client.send_message("/music/interpretation", interp_text)

        raw_sequence = data.get("sequence", [])
        valid_notes = normalize_sequence(raw_sequence)

        state.update_last_generation(
            interpretation=interp_text,
            visual_params={
                "energy": energy,
                "complexity": complexity,
                "color_mood": color_mood,
            },
            sequence=valid_notes,
        )

        print(f">>> 救済抽出成功: {len(valid_notes)}音を処理")

        if midi_out:
            for note_data in valid_notes:
                threading.Thread(
                    target=play_midi_note_func,
                    args=(midi_out, note_data),
                    daemon=True,
                ).start()

        return {
            "interpretation": interp_text,
            "energy": energy,
            "complexity": complexity,
            "color_mood": color_mood,
            "sequence": valid_notes,
        }

    except Exception as e:
        print(f"解析エラー: {e}")
        return None