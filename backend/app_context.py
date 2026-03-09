import lancedb
from openai import OpenAI
from pythonosc import udp_client
from langchain_ollama import OllamaEmbeddings

from config import (
    LM_STUDIO_BASE_URL,
    LM_STUDIO_API_KEY,
    OSC_HOST,
    OSC_PORT,
    VECTOR_DB_PATH,
    EMBEDDING_MODEL_NAME,
    MIDI_OUT_BUS_KEYWORD,
    MIDI_IN_BUS_KEYWORD,
    HISTORY_TIMEOUT,
)
from state import SessionState
from midi_io import open_midi_port, start_midi_monitor_thread
from feedback_store import ensure_eval_logs_table
from generation_store import ensure_generation_logs_table


class AppContext:
    def __init__(self):
        self.client = OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key=LM_STUDIO_API_KEY,
        )
        self.osc_client = udp_client.SimpleUDPClient(OSC_HOST, OSC_PORT)
        self.db_conn = lancedb.connect(VECTOR_DB_PATH)
        ensure_eval_logs_table(self.db_conn)
        ensure_generation_logs_table(self.db_conn)

        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
        self.state = SessionState()

        self.midi_out = open_midi_port(MIDI_OUT_BUS_KEYWORD, is_input=False)
        self.midi_in = open_midi_port(MIDI_IN_BUS_KEYWORD, is_input=True)

        start_midi_monitor_thread(self.midi_in, self.state, HISTORY_TIMEOUT)