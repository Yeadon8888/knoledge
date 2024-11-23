import sqlite3
import json
from typing import List, Dict, Any
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()
        
    def init_db(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        
        # 创建网页信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建知识表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                vector BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (page_id) REFERENCES pages (id)
            )
        """)
        
        # 创建知识表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                page_id INTEGER PRIMARY KEY,
                knowledge_json TEXT,
                vectors_json TEXT,
                FOREIGN KEY (page_id) REFERENCES pages (id)
            )
        """)
        
        self.conn.commit()
    
    def store_page(self, url: str, title: str, content: str) -> int:
        """存储网页信息"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO pages (url, title, content) VALUES (?, ?, ?)",
            (url, title, content)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def store_knowledge(self, page_id: int, knowledge_dict: Dict[str, List[str]], vectors: Dict[str, List[List[float]]]):
        """存储知识项及其向量"""
        cursor = self.conn.cursor()
        
        for category, items in knowledge_dict.items():
            for idx, content in enumerate(items):
                vector = vectors.get(category, [])[idx] if vectors.get(category) else None
                vector_blob = np.array(vector).tobytes() if vector else None
                
                cursor.execute(
                    "INSERT INTO knowledge_items (page_id, category, content, vector) VALUES (?, ?, ?, ?)",
                    (page_id, category, content, vector_blob)
                )
        
        self.conn.commit()
    
    def search_similar_knowledge(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """搜索相似的知识项"""
        query_vector_np = np.array(query_vector)
        results = []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category, content, vector FROM knowledge_items WHERE vector IS NOT NULL")
        
        for row in cursor.fetchall():
            id_, category, content, vector_blob = row
            if vector_blob:
                vector = np.frombuffer(vector_blob).reshape(-1)
                similarity = np.dot(query_vector_np, vector) / (np.linalg.norm(query_vector_np) * np.linalg.norm(vector))
                results.append({
                    'id': id_,
                    'category': category,
                    'content': content,
                    'similarity': float(similarity)
                })
        
        # 按相似度降序排序并返回前N个结果
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]

    def get_all_knowledge(self) -> List[Dict[str, Any]]:
        """获取所有知识项"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT k.id, k.category, k.content, p.url, p.title
            FROM knowledge_items k
            JOIN pages p ON k.page_id = p.id
            ORDER BY k.created_at DESC
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'category': row[1],
                'content': row[2],
                'url': row[3],
                'page_title': row[4]
            })
        
        return results

    def get_page(self, page_id: int) -> dict:
        """获取页面信息"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT url, title, content FROM pages WHERE id = ?",
                (page_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "url": row[0],
                    "title": row[1],
                    "content": row[2]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting page: {str(e)}")
            raise

    def store_knowledge_only(self, page_id: int, knowledge: dict):
        """只存储知识，不包含向量"""
        try:
            cursor = self.conn.cursor()
            # 存储知识
            knowledge_json = json.dumps(knowledge)
            cursor.execute(
                """
                INSERT OR REPLACE INTO knowledge (page_id, knowledge_json)
                VALUES (?, ?)
                """,
                (page_id, knowledge_json)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error storing knowledge: {str(e)}")
            raise

    def get_knowledge(self, page_id: int) -> dict:
        """获取页面的知识"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT knowledge_json FROM knowledge WHERE page_id = ?",
                (page_id,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Error getting knowledge: {str(e)}")
            raise

    def store_vectors(self, page_id: int, vectors: dict):
        """存储知识向量"""
        try:
            cursor = self.conn.cursor()
            vectors_json = json.dumps(vectors)
            cursor.execute(
                """
                UPDATE knowledge
                SET vectors_json = ?
                WHERE page_id = ?
                """,
                (vectors_json, page_id)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error storing vectors: {str(e)}")
            raise
