def build_system_prompt(
    recent_notes: str,
    current_instruction: str,
    knowledge_context: str = "参考音楽知識: なし",
) -> str:
    return (
        "あなたは自律演奏AI『CREAM』です。今すぐセッションを開始してください。\n"
        f"【ユーザー演奏】: {recent_notes}\n"
        f"【指揮者指示】: {current_instruction}\n"
        f"【音楽知識】: \n{knowledge_context}\n\n"
        "【出力命令（厳守）】\n"
        "1. JSONの 'interpretation' に、今の演奏に対するあなたの解釈を日本語一言で記述せよ。\n"
        "2. 'visual_params' には energy, complexity, color_mood を必ず含めること。\n"
        "3. 'sequence' には、和音やフレーズを構成するため、必ず【4つから12つの音符データ】を含めること。\n"
        "4. ユーザー演奏・指示・参考音楽知識を統合して応答せよ。\n"
        "5. 音符の 'time' をずらしてメロディにしたり、同じにして和音にしたりして音楽的に表現せよ。\n\n"
        "【出力形式例】\n"
        "```json\n"
        "{\n"
        '  "interpretation": "（ここに解釈を書く）",\n'
        '  "visual_params": {\n'
        '    "energy": 0.8,\n'
        '    "complexity": 0.4,\n'
        '    "color_mood": "warm"\n'
        "  },\n"
        '  "sequence": [\n'
        '    {"time": 0.0, "note": "C4", "duration": "0.5s"},\n'
        '    {"time": 0.0, "note": "E4", "duration": "0.5s"},\n'
        '    {"time": 0.5, "note": "G4", "duration": "1.0s"},\n'
        '    {"time": 1.0, "note": "C5", "duration": "0.5s"}\n'
        "  ]\n"
        "}\n"
        "```\n"
        "解説は不要。JSONのみを出力せよ。"
    )


def request_generation(client, model_name: str, system_prompt: str, temperature: float = 0.8) -> str:
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": system_prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content


def generate_music_response(
    client,
    recent_notes: str,
    current_instruction: str,
    knowledge_context: str = "参考音楽知識: なし",
    model_name: str = "liquid-lfm-1.2b",
    temperature: float = 0.8,
) -> str:
    system_prompt = build_system_prompt(
        recent_notes=recent_notes,
        current_instruction=current_instruction,
        knowledge_context=knowledge_context,
    )
    return request_generation(
        client=client,
        model_name=model_name,
        system_prompt=system_prompt,
        temperature=temperature,
    )