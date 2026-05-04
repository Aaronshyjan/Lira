import os
import pandas as pd
import json
import requests
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", 5000))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
JSON_FILE = os.getenv("JSON_FILE", "logs_10k.csv")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "lira")
FORCE_RECREATE = os.getenv("FORCE_RECREATE", "True").lower() == "true"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "bge-m3")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embeddings")
DIMENSIONS = int(os.getenv("DIMENSIONS", 1024))

# Credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase Client Initialized")
    except Exception as e:
        print(f"❌ Supabase init error: {e}")

def get_ollama_embeddings(texts):
    vectors = []
    for text in texts:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text})
        vectors.append(response.json()["embedding"])
    return vectors

def run_ingestion():
    print(f"🚀 Starting Dual Ingestion (Ollama/BGE-M3: {DIMENSIONS} dims)")
    
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: {JSON_FILE} not found.")
        return

    df = pd.read_csv(JSON_FILE)
    if FORCE_RECREATE:
        print("🔄 Resetting ingestion flags...")
        df['ingested'] = False
        
    pending_df = df[df['ingested'] == False].head(DAILY_LIMIT)
    if pending_df.empty:
        print("✅ No records to ingest!")
        return

    # 2. Setup Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if PINECONE_INDEX_NAME in pc.list_indexes().names():
        desc = pc.describe_index(PINECONE_INDEX_NAME)
        if FORCE_RECREATE or desc.dimension != DIMENSIONS:
            print(f"🗑️ Deleting index {PINECONE_INDEX_NAME} (Ollama Switch)...")
            pc.delete_index(PINECONE_INDEX_NAME)
            time.sleep(12)

    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"🛠️ Creating Index: {PINECONE_INDEX_NAME} ({DIMENSIONS} dims)...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=DIMENSIONS, 
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status.ready:
            time.sleep(2)

    index = pc.Index(PINECONE_INDEX_NAME)

    # 3. Dual Processing
    processed_count = 0
    for i in tqdm(range(0, len(pending_df), BATCH_SIZE)):
        batch = pending_df.iloc[i:i+BATCH_SIZE]
        texts = batch['description'].astype(str).tolist()
        
        try:
            # Generate Vectors via Ollama
            vectors = get_ollama_embeddings(texts)
            
            # --- 1. Push to Pinecone ---
            upserts = []
            for j, (idx, row) in enumerate(batch.iterrows()):
                upserts.append({
                    "id": f"log-{idx}",
                    "values": vectors[j],
                    "metadata": {
                        "text": f"LOG: {row['description']} | CAUSE: {row['root_cause']} | FIX: {row['solution']}",
                        "category": str(row['category']).lower(),
                        "severity": str(row['level']).upper(),
                        "service": str(row['service']).lower()
                    }
                })
            index.upsert(vectors=upserts)
            
            # --- 2. Push to Supabase (New Schema) ---
            if supabase:
                sb_data = []
                for _, row in batch.iterrows():
                    sb_data.append({
                        "timestamp": row['timestamp'],
                        "level": str(row['level']).upper(),
                        "raw_log": row['description'],
                        "message": row['description'][:200],
                        "cause": row['root_cause'],
                        "fix": row['solution'],
                        "severity": str(row['level']).upper(),
                        "confidence": float(row['confidence']),
                        "container": row['service'],
                        "log_type": row['category']
                    })
                supabase.table("incidents").insert(sb_data).execute()
            
            # Save Progress
            df.loc[batch.index, 'ingested'] = True
            processed_count += len(batch)
            df.to_csv(JSON_FILE, index=False)
            
        except Exception as e:
            print(f"\n❌ Batch Error: {e}")
            time.sleep(2)

    print(f"\n✨ Ingestion Complete! {processed_count} logs pushed via Ollama/BGE-M3.")

if __name__ == "__main__":
    run_ingestion()
