from dataclasses import dataclass, field
from threading import Lock
from typing import Any
from uuid import uuid4


@dataclass
class SessionState:
    current_instruction: str = "自由に演奏してください。"
    user_midi_history: list[dict[str, Any]] = field(default_factory=list)
    is_autonomous_mode: bool = True

    last_interpretation: str = ""
    last_visual_params: dict[str, Any] = field(default_factory=dict)
    last_sequence: list[dict[str, Any]] = field(default_factory=list)

    session_id: str = field(default_factory=lambda: str(uuid4()))
    lock: Lock = field(default_factory=Lock)

    def add_midi_event(self, event: dict[str, Any], window_sec: float = 10.0) -> None:
        with self.lock:
            self.user_midi_history.append(event)
            current_time = event["time"]
            self.user_midi_history = [
                e for e in self.user_midi_history
                if current_time - e["time"] < window_sec
            ]

    def get_recent_midi_history(self) -> list[dict[str, Any]]:
        with self.lock:
            return list(self.user_midi_history)

    def set_instruction(self, instruction: str) -> None:
        with self.lock:
            self.current_instruction = instruction

    def get_instruction(self) -> str:
        with self.lock:
            return self.current_instruction

    def new_session(self) -> str:
        with self.lock:
            self.session_id = str(uuid4())
            self.user_midi_history = []
            self.last_interpretation = ""
            self.last_visual_params = {}
            self.last_sequence = []
            return self.session_id

    def get_session_id(self) -> str:
        with self.lock:
            return self.session_id

    def update_last_generation(
        self,
        interpretation: str = "",
        visual_params: dict[str, Any] | None = None,
        sequence: list[dict[str, Any]] | None = None,
    ) -> None:
        with self.lock:
            self.last_interpretation = interpretation
            self.last_visual_params = visual_params or {}
            self.last_sequence = sequence or []

    def get_status(self) -> dict[str, Any]:
        with self.lock:
            return {
                "session_id": self.session_id,
                "current_instruction": self.current_instruction,
                "is_autonomous_mode": self.is_autonomous_mode,
                "last_interpretation": self.last_interpretation,
                "last_visual_params": dict(self.last_visual_params),
                "last_sequence": list(self.last_sequence),
                "recent_midi_count": len(self.user_midi_history),
            }