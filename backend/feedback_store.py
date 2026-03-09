from datetime import datetime
from typing import Any


def ensure_eval_logs_table(db_conn: Any, table_name: str = "eval_logs"):
    try:
        if table_name not in db_conn.table_names():
            db_conn.create_table(
                table_name,
                data=[
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "instruction": "",
                        "interpretation": "",
                        "feedback_type": "",
                        "feedback_text": "",
                        "recent_midi_count": 0,
                    }
                ],
                mode="overwrite",
            )
            print(f"'{table_name}' テーブルを新規作成しました。")
    except Exception as e:
        print(f"eval_logs テーブル初期化エラー: {e}")


def save_feedback(
    db_conn: Any,
    instruction: str,
    interpretation: str,
    feedback_type: str,
    feedback_text: str,
    recent_midi_count: int,
    table_name: str = "eval_logs",
) -> bool:
    try:
        ensure_eval_logs_table(db_conn, table_name=table_name)
        table = db_conn.open_table(table_name)

        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "instruction": instruction,
            "interpretation": interpretation,
            "feedback_type": feedback_type,
            "feedback_text": feedback_text,
            "recent_midi_count": recent_midi_count,
        }

        table.add([row])
        print(f"フィードバック保存完了: {feedback_type}")
        return True

    except Exception as e:
        print(f"フィードバック保存エラー: {e}")
        return False