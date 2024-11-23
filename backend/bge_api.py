import requests
import numpy as np
from typing import List, Union
import os
from dotenv import load_dotenv

load_dotenv()

class BGEM3API:
    def __init__(self):
        self.api_key = os.getenv("sk-ddnhvdrcuwfhdrdddpdlibogvqsrrgmsbebabyrgcdfemffr")
        self.api_base = "https://api.bgem3.com/v1"
        
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """获取文本的向量表示"""
        if isinstance(texts, str):
            texts = [texts]
            
        try:
            response = requests.post(
                f"{self.api_base}/embeddings",
                headers=self._get_headers(),
                json={
                    "input": texts,
                    "model": "bge-m3"
                }
            )
            response.raise_for_status()
            return [data["embedding"] for data in response.json()["data"]]
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return []

    def compute_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
