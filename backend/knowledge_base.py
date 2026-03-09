from typing import Any


def build_knowledge_query(current_instruction: str, recent_notes: str) -> str:
    instruction = current_instruction.strip() if current_instruction else ""
    notes = recent_notes.strip() if recent_notes else "なし"
    return f"演奏指示: {instruction} / 直近演奏: {notes}"


def search_music_knowledge(
    db_conn: Any,
    embeddings: Any,
    current_instruction: str,
    recent_notes: str,
    table_name: str = "music_caps",
    top_k: int = 3,
) -> list[str]:
    try:
        if table_name not in db_conn.table_names():
            print(f"知識検索スキップ: テーブル '{table_name}' が見つかりません。")
            return []

        query_text = build_knowledge_query(current_instruction, recent_notes)
        query_vector = embeddings.embed_query(query_text)

        table = db_conn.open_table(table_name)
        results = table.search(query_vector).limit(top_k).to_list()

        knowledge_texts = []
        for row in results:
            text = row.get("text")
            if text:
                knowledge_texts.append(text)

        print(f"Knowledge hit: {len(knowledge_texts)}件")
        return knowledge_texts

    except Exception as e:
        print(f"知識検索エラー: {e}")
        return []


def format_knowledge_for_prompt(knowledge_texts: list[str]) -> str:
    if not knowledge_texts:
        return "参考音楽知識: なし"

    lines = ["参考音楽知識:"]
    for i, text in enumerate(knowledge_texts, start=1):
        lines.append(f"{i}. {text}")
    return "\n".join(lines)