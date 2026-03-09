import pandas as pd
from langchain_community.vectorstores import LanceDB
from langchain_ollama import OllamaEmbeddings
import lancedb

# プロジェクトディレクトリの設定
DB_PATH = "./data/music_knowledge_db"
CSV_PATH = "musiccaps-public.csv"  # ダウンロードしたCSV

def ingest_data():
    # CSV読み込み (caption列が音楽の説明文)
    df = pd.read_csv(CSV_PATH)
    texts = df['caption'].tolist()
    
    # Ollamaを使って文章をベクトル（数値）に変換
    embeddings = OllamaEmbeddings(model="gemma:2b")
    
    # ローカルDB (LanceDB) に保存
    db = lancedb.connect(DB_PATH)
    # 知識ベース作成（gemma:2bのベクトルを生成して保存）
    table = db.create_table("music_caps", 
                            data=[{"text": t, "vector": embeddings.embed_query(t)} for t in texts[:500]], 
                            mode="overwrite")
    print(f"Ingested {len(texts[:500])} rows with gemma:2b embeddings.")

def setup_eval_table():
    db = lancedb.connect(DB_PATH)
    # 評価ログ用のテーブル作成（次元数を2048に変更！）
    if "eval_logs" not in db.table_names():
        db.create_table("eval_logs", 
                        data=[{"text": "init", "error_type": "none", "vector": [0.0]*2048}])
        print("Created evaluation log table (2048 dim).")

if __name__ == "__main__":
    ingest_data()
    setup_eval_table()