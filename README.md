# Music Recommendation System

以使用者聆聽紀錄建立個人化音樂推薦系統，
透過協同過濾與向量搜尋尋找相似使用者，
並根據相似使用者的聆聽行為產生推薦歌曲。

## Tech Stack
- Python
- PostgreSQL
- Qdrant
- FastAPI
- Streamlit
- Docker
- TruncatedSVD

## Recommendation Workflow
User-Song Play Count Matrix
→ TruncatedSVD
→ User Embedding
→ Qdrant Vector Search
→ Similar Users
→ Candidate Songs
→ Filter Listened Songs
→ Recommendations

## System Architecture
- PostgreSQL：儲存歌曲與使用者聆聽紀錄
- Qdrant：儲存使用者向量並進行相似度搜尋
- FastAPI：提供推薦系統 API
- Streamlit：建立推薦結果互動介面
- Docker：建立 PostgreSQL 與 Qdrant 執行環境

## Recommendation Method
將 User-Song Interaction Matrix 經由 TruncatedSVD 降維，
建立 256 維使用者向量，並使用 Cosine Similarity 尋找相似使用者。
再根據相似使用者的聆聽紀錄產生候選歌曲，
排除目標使用者已聽過的歌曲後產生推薦結果。

## Dataset
Million Song Dataset (1% subset)  
Echo Nest Taste Profile

## Project Structure
- `data_collection/`：資料處理與推薦模型相關程式
- `backend/`：FastAPI 後端服務
- `frontend/`：Streamlit 使用者介面

## Note
Large datasets, database files, virtual environments, and sensitive configuration files are not included in this repository.
