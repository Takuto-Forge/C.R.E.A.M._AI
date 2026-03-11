# C.R.E.A.M.

**Compositional Real-time Engine for Augmented Musicality**

# Demo

https://www.youtube.com/watch?v=PbfORgyXfn0

C.R.E.A.M. は、人間とAIがリアルタイムに即興共作するための音楽システムです。

人間のMIDI演奏、自然言語による演奏指示、音楽知識データベースを統合し、AIが音楽フレーズ・解釈テキスト・映像制御パラメータを生成し演奏としてセッションの形で返してくれます。

本システムは、AIを単なる生成ツールではなく、即興演奏に参加する「共演者」として人間とAIを対等な立場で定義することを目的としています。

---

# 概要

C.R.E.A.M. は、人間の演奏とAIの解釈をリアルタイムに統合することで、音楽即興における人間とAIの共創を実現するシステムです。

本システムは以下の要素を統合しています。

* 人間のMIDI演奏
* Webインターフェースからの自然言語による演奏指示
* MusicCaps + LanceDB による音楽知識検索
* LLMによる解釈生成および音楽シーケンス生成

AIは以下の出力を生成します。

* MIDI（Ableton Live による音楽出力）
* OSC（TouchDesigner による映像制御）
* 解釈テキスト（共作の意味レイヤー）

---

# コンセプト

C.R.E.A.M. は、一般的な音楽生成AIのような

prompt → music

という一方向の生成システムではありません。

本システムでは

人間の演奏 + 人間の指示 + 音楽知識
↓
AIによる解釈
↓
音楽的応答

という構造を持ち、AIを「共演者」としてリアルタイムの即興演奏に参加させることを目指しています。

---

# システム構成

C.R.E.A.M. は以下の構造で動作します。

Human Performance (MIDI)
＋
Human Instruction (Web UI)
↓
C.R.E.A.M. Engine
（LLM + 音楽知識 + セッション状態）
↓
MIDI → Ableton Live
OSC → TouchDesigner
Text → 音楽的解釈

---

# プロジェクト構成

```
cream/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── state.py
│   ├── app_context.py
│   ├── session_engine.py
│   ├── midi_io.py
│   ├── osc_output.py
│   ├── llm_generator.py
│   ├── knowledge_base.py
│   ├── feedback_store.py
│   ├── generation_store.py
│   └── requirements.txt
│
├── frontend/
│   └── Next.js control interface
│
├── data/
│   └── music_knowledge_db/
│
├── scripts/
│   └── ingest_musiccaps.py
│
├── assets/
│   └── jssa2026/
│
└── README.md
```

---

# バックエンド機能

* FastAPIベースの制御API
* 自律セッションループ
* MIDI入力の監視
* MIDI出力生成
* TouchDesignerへのOSC送信
* LanceDBによる音楽知識検索
* フィードバックログ保存
* 生成ログ保存
* セッションID管理

---

# フロントエンド機能

* 演奏指示入力パネル
* セッション状態の監視
* 定期的なステータス取得
* フィードバック送信
* 新規セッション開始

---

# APIエンドポイント

## POST /chat

演奏指示を更新します。

```
{
  "message": "もっと静かに、アンビエント寄りに",
  "user_id": "local-user"
}
```

---

## GET /status

現在のC.R.E.A.M.セッション状態を取得します。

---

## POST /feedback

AIの応答に対するフィードバックを保存します。

```
{
  "feedback_type": "not_reflected",
  "feedback_text": "もっと静かな雰囲気にしてほしかった"
}
```

---

## POST /session/new

新しい即興セッションを開始します。

---

# バックエンドセットアップ

プロジェクトルートで実行

```
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

バックエンド起動

```
python backend/main.py
```

---

# フロントエンドセットアップ

```
cd frontend
npm install
npm run dev
```

---

# 知識データベース構築

MusicCaps データを使用して LanceDB を構築します。

テスト用のサンプルデータを使用する場合

```
data_sample/musiccaps_small.csv
```

を使用してください。

```
python scripts/ingest_musiccaps.py
```

---

# 研究背景

C.R.E.A.M. は以下のテーマを探求する研究プロジェクトです。

* 生成AIなどのアートにおけるAIを嫌う傾向に疑問視
* 大事なのは人間とAIを区別することではない
* 人間とAIの共生。対等な立場での共生である。
* AIを受け入れることでアートとして新たな境地に達することができるのではないか。

* 人間とAIの即興共作
* AIを人間と対等な立場の創造的パートナーとして扱うシステム
* 音楽パフォーマンスにおける意味的解釈生成
* 音楽と映像のリアルタイム生成

---

# 作者

大久保 拓太
東京電機大学大学院

---

# プロジェクト状態

Experimental / Active Development

---

# License

MIT License

---

# C.R.E.A.M.

**Compositional Real-time Engine for Augmented Musicality**

# Demo

https://www.youtube.com/watch?v=PbfORgyXfn0

C.R.E.A.M. is a music system designed for real-time improvisational co-creation between humans and AI.

The system integrates human MIDI performance, natural language instructions, and a music knowledge database.
The AI generates musical phrases, interpretation text, and visual control parameters, returning them as part of a live improvisational session.

This system aims to define AI not as a simple generative tool, but as a **co-performer** that participates in improvisation on an equal footing with humans.

---

# Overview

C.R.E.A.M. enables human–AI collaborative improvisation by integrating human performance and AI interpretation in real time.

The system combines the following elements:

* Human MIDI performance
* Natural language instructions from a web interface
* Music knowledge retrieval using MusicCaps + LanceDB
* LLM-based interpretation and music sequence generation

The AI produces the following outputs:

* MIDI (for musical performance via Ableton Live)
* OSC (for visual control via TouchDesigner)
* Interpretation text (a semantic layer of the co-creation process)

---

# Concept

C.R.E.A.M. is not a one-shot music generation system like many conventional AI music tools.

Instead of:

prompt → music

the system is structured as:

human performance + human instruction + music knowledge
↓
AI interpretation
↓
musical response

Through this structure, the AI participates in real-time improvisation as a **co-performer**.

---

# System Architecture

C.R.E.A.M. operates with the following architecture:

Human Performance (MIDI)
＋
Human Instruction (Web UI)
↓
C.R.E.A.M. Engine
(LLM + Music Knowledge + Session State)
↓
MIDI → Ableton Live
OSC → TouchDesigner
Text → Musical Interpretation

---

# Project Structure

```
cream/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── state.py
│   ├── app_context.py
│   ├── session_engine.py
│   ├── midi_io.py
│   ├── osc_output.py
│   ├── llm_generator.py
│   ├── knowledge_base.py
│   ├── feedback_store.py
│   ├── generation_store.py
│   └── requirements.txt
│
├── frontend/
│   └── Next.js control interface
│
├── data/
│   └── music_knowledge_db/
│
├── scripts/
│   └── ingest_musiccaps.py
│
├── assets/
│   └── jssa2026/
│
└── README.md
```

---

# Backend Features

* FastAPI-based control API
* Autonomous session loop
* MIDI input monitoring
* MIDI output generation
* OSC dispatch to TouchDesigner
* Music knowledge retrieval via LanceDB
* Feedback logging
* Generation logging
* Session ID management

---

# Frontend Features

* Instruction input panel
* Live session monitoring
* Status polling
* Feedback submission
* New session control

---

# API Endpoints

## POST /chat

Updates the current musical instruction.

```
{
  "message": "Play more quietly, with an ambient feeling",
  "user_id": "local-user"
}
```

---

## GET /status

Retrieves the current state of the C.R.E.A.M. session.

---

## POST /feedback

Stores feedback about the AI's response.

```
{
  "feedback_type": "not_reflected",
  "feedback_text": "I wanted a quieter atmosphere"
}
```

---

## POST /session/new

Starts a new improvisation session.

---

# Backend Setup

Run from the project root:

```
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Start the backend:

```
python backend/main.py
```

---

# Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

# Knowledge Base Setup

Build the LanceDB knowledge base using MusicCaps data.

For quick testing, you can use the included sample dataset:

```
data_sample/musiccaps_small.csv
```

Run ingestion:

```
python scripts/ingest_musiccaps.py
```

---

# Research Context

C.R.E.A.M. is developed as a research project exploring:

* The skepticism toward AI in artistic creation
* The idea that the key question is not separating humans and AI
* Human–AI coexistence and collaboration on equal terms
* The possibility that accepting AI may open new frontiers in art

The project investigates:

* Human–AI improvisational co-creation
* AI as an equal creative partner
* Semantic interpretation in musical performance
* Real-time generation of music and visuals

---

# Author

Takuto Okubo
Tokyo Denki University Graduate School

---

# Project Status

Experimental / Active Development

---

# License

MIT License
