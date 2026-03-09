import json
import threading
import time

from config import GENERATION_INTERVAL, MODEL_NAME, MODEL_TEMPERATURE
from llm_generator import generate_music_response
from knowledge_base import search_music_knowledge, format_knowledge_for_prompt
from osc_output import process_and_dispatch_generation
from generation_store import save_generation_log
from midi_io import play_midi_note


def autonomous_session_loop(ctx):
    print("自律セッション・ループを開始しました。")

    while True:
        try:
            status = ctx.state.get_status()
            if status["is_autonomous_mode"]:
                print("--- 自律生成プロセス開始 ---")

                active_history = ctx.state.get_recent_midi_history()
                recent_notes = ", ".join([m["note"] for m in active_history]) if active_history else "なし"
                current_instruction = ctx.state.get_instruction()

                knowledge_texts = search_music_knowledge(
                    db_conn=ctx.db_conn,
                    embeddings=ctx.embeddings,
                    current_instruction=current_instruction,
                    recent_notes=recent_notes,
                    table_name="music_caps",
                    top_k=3,
                )
                knowledge_context = format_knowledge_for_prompt(knowledge_texts)

                print("LM Studioにリクエスト送信中...")
                res_content = generate_music_response(
                    client=ctx.client,
                    recent_notes=recent_notes,
                    current_instruction=current_instruction,
                    knowledge_context=knowledge_context,
                    model_name=MODEL_NAME,
                    temperature=MODEL_TEMPERATURE,
                )
                print(f"AIからのレスポンスを受信: {res_content[:80]}...")

                generation_result = process_and_dispatch_generation(
                    content=res_content,
                    osc_client=ctx.osc_client,
                    midi_out=ctx.midi_out,
                    state=ctx.state,
                    play_midi_note_func=play_midi_note,
                )

                if generation_result:
                    save_generation_log(
                        db_conn=ctx.db_conn,
                        session_id=ctx.state.get_session_id(),
                        instruction=current_instruction,
                        recent_notes=recent_notes,
                        knowledge_context=knowledge_context,
                        interpretation=generation_result["interpretation"],
                        energy=generation_result["energy"],
                        complexity=generation_result["complexity"],
                        color_mood=generation_result["color_mood"],
                        sequence_json=json.dumps(generation_result["sequence"], ensure_ascii=False),
                    )

                print("OSC/MIDI送信プロセス完了")

        except Exception as e:
            print(f"自律生成エラー: {e}")

        time.sleep(GENERATION_INTERVAL)


def start_autonomous_session_thread(ctx):
    threading.Thread(
        target=autonomous_session_loop,
        args=(ctx,),
        daemon=True,
    ).start()