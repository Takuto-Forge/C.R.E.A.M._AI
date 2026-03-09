from datetime import datetime
from typing import Any


def ensure_generation_logs_table(db_conn: Any, table_name: str = "generation_logs"):
    try:
        if table_name not in db_conn.table_names():
            db_conn.create_table(
                table_name,
                data=[
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "session_id": "",
                        "instruction": "",
                        "recent_notes": "",
                        "knowledge_context": "",
                        "interpretation": "",
                        "energy": 0.0,
                        "complexity": 0.0,
                        "color_mood": "",
                        "sequence_json": "[]",
                    }
                ],
                mode="overwrite",
            )
            print(f"'{table_name}' テーブルを新規作成しました。")
    except Exception as e:
        print(f"generation_logs テーブル初期化エラー: {e}")


def save_generation_log(
    db_conn: Any,
    session_id: str,
    instruction: str,
    recent_notes: str,
    knowledge_context: str,
    interpretation: str,
    energy: float,
    complexity: float,
    color_mood: str,
    sequence_json: str,
    table_name: str = "generation_logs",
) -> bool:
    try:
        ensure_generation_logs_table(db_conn, table_name=table_name)
        table = db_conn.open_table(table_name)

        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "instruction": instruction,
            "recent_notes": recent_notes,
            "knowledge_context": knowledge_context,
            "interpretation": interpretation,
            "energy": energy,
            "complexity": complexity,
            "color_mood": color_mood,
            "sequence_json": sequence_json,
        }

        table.add([row])
        print("生成ログ保存完了")
        return True

    except Exception as e:
        print(f"生成ログ保存エラー: {e}")
        return False