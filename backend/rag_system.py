# import os
# import json
# from pathlib import Path
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import logging

# # 配置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class RAGSystem:
#     """RAG（检索增强生成）系统"""
    
#     def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
#         """初始化 RAG 系统
        
#         Args:
#             model_name: Sentence Transformers 模型名称
#         """
#         logger.info("🔄 加载向量模型...")
#         self.model = SentenceTransformer(model_name)
#         self.embeddings = None
#         self.documents = []
#         self.index = None
#         logger.info("✅ 向量模型加载完成")
        
#     def load_knowledge_base(self, kb_path='knowledge_base'):
#         """从文件加载知识库
        
#         Args:
#             kb_path: 知识库目录路径
#         """
#         logger.info(f"📚 从 {kb_path} 加载知识库...")
#         self.documents = []
        
#         kb_dir = Path(kb_path)
#         if not kb_dir.exists():
#             logger.warning(f"⚠️  {kb_path} 目录不存在")
#             return
        
#         # 递归遍历所有 Markdown 文件
#         md_files = list(kb_dir.rglob('*.md'))
#         logger.info(f"🔍 找到 {len(md_files)} 个 Markdown 文件")
        
#         for md_file in md_files:
#             try:
#                 with open(md_file, 'r', encoding='utf-8') as f:
#                     content = f.read()
#                     # 按标题分割文档
#                     chunks = self._chunk_text(content, md_file.name)
#                     self.documents.extend(chunks)
#                     logger.info(f"✅ 加载: {md_file.name} ({len(chunks)} 块)")
#             except Exception as e:
#                 logger.error(f"❌ 加载失败 {md_file}: {e}")
        
#         logger.info(f"✅ 已加载 {len(self.documents)} 个文档块")
        
#     def _chunk_text(self, text, source_name='', chunk_size=500, overlap=100):
#         """将长文本分割成块
        
#         Args:
#             text: 原始文本
#             source_name: 源文件名
#             chunk_size: 块大小
#             overlap: 重叠大小
            
#         Returns:
#             文档块列表
#         """
#         chunks = []
#         lines = text.split('\n')
#         current_chunk = []
#         current_length = 0
        
#         for line in lines:
#             current_chunk.append(line)
#             current_length += len(line)
            
#             if current_length > chunk_size:
#                 chunk_text = '\n'.join(current_chunk)
#                 if chunk_text.strip():
#                     # 添加元数据
#                     chunks.append({
#                         'content': chunk_text,
#                         'source': source_name,
#                         'length': len(chunk_text)
#                     })
                
#                 # 保留部分重叠
#                 current_chunk = current_chunk[-overlap//50:]
#                 current_length = sum(len(l) for l in current_chunk)
        
#         # 添加最后的块
#         if current_chunk:
#             chunk_text = '\n'.join(current_chunk)
#             if chunk_text.strip():
#                 chunks.append({
#                     'content': chunk_text,
#                     'source': source_name,
#                     'length': len(chunk_text)
#                 })
        
#         return chunks
    
#     def build_index(self):
#         """构建 FAISS 索引"""
#         if not self.documents:
#             logger.error("❌ 错误: 没有加载文档")
#             return
        
#         logger.info(f"🔄 向量化 {len(self.documents)} 个文档...")
        
#         # 提取文档内容
#         doc_contents = [doc['content'] if isinstance(doc, dict) else doc 
#                        for doc in self.documents]
        
#         # 向量化文档
#         self.embeddings = self.model.encode(
#             doc_contents,
#             convert_to_numpy=True,
#             show_progress_bar=True
#         )
        
#         logger.info(f"✅ 向量化完成，向量维度: {self.embeddings.shape}")
        
#         # 构建 FAISS 索引
#         logger.info("🔄 构建 FAISS 索引...")
#         dimension = self.embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)
#         self.index.add(self.embeddings.astype(np.float32))
        
#         logger.info(f"✅ 索引构建完成，包含 {self.index.ntotal} 个向量")
        
#     def retrieve(self, query, top_k=3):
#         """检索相关文档
        
#         Args:
#             query: 查询文本
#             top_k: 返回前 K 个相关文档
            
#         Returns:
#             相关文档列表
#         """
#         if self.index is None:
#             logger.warning("⚠️  索引未初始化")
#             return []
        
#         # 向量化查询
#         query_embedding = self.model.encode(query, convert_to_numpy=True)
        
#         # 搜索最相似的文档
#         distances, indices = self.index.search(
#             query_embedding.reshape(1, -1).astype(np.float32),
#             min(top_k, self.index.ntotal)
#         )
        
#         results = []
#         for idx, distance in zip(indices[0], distances[0]):
#             if idx < len(self.documents):
#                 doc = self.documents[idx]
#                 # 处理不同的文档格式
#                 if isinstance(doc, dict):
#                     content = doc['content']
#                     source = doc.get('source', 'unknown')
#                 else:
#                     content = doc
#                     source = 'unknown'
                
#                 results.append({
#                     'content': content,
#                     'source': source,
#                     'score': float(1 - distance / 100)  # 相似度分数 0-1
#                 })
        
#         logger.info(f"🔍 检索完成: 找到 {len(results)} 个相关文档")
#         return results
    
#     def save_index(self, index_path='rag_index'):
#         """保存索引
        
#         Args:
#             index_path: 索引保存路径
#         """
#         os.makedirs(index_path, exist_ok=True)
        
#         try:
#             # 保存 FAISS 索引
#             faiss.write_index(self.index, f'{index_path}/faiss.index')
            
#             # 保存文档列表
#             with open(f'{index_path}/documents.json', 'w', encoding='utf-8') as f:
#                 json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
#             logger.info(f"✅ 索引已保存到 {index_path}")
#         except Exception as e:
#             logger.error(f"❌ 保存索引失败: {e}")
    
#     def load_index(self, index_path='rag_index'):
#         """加载已保存的索引
        
#         Args:
#             index_path: 索引路径
            
#         Returns:
#             是否加载成功
#         """
#         try:
#             self.index = faiss.read_index(f'{index_path}/faiss.index')
#             with open(f'{index_path}/documents.json', 'r', encoding='utf-8') as f:
#                 self.documents = json.load(f)
            
#             logger.info(f"✅ 索引已加载，包含 {len(self.documents)} 个文档")
#             return True
#         except Exception as e:
#             logger.warning(f"⚠️  加载索引失败: {e}")
#             return False
    
#     def get_status(self):
#         """获取 RAG 系统状态"""
#         return {
#             'status': 'ready' if self.index else 'not_initialized',
#             'documents_count': len(self.documents),
#             'index_size': self.index.ntotal if self.index else 0,
#             'model': 'paraphrase-multilingual-MiniLM-L12-v2'
#         }
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    """RAG（检索增强生成）系统"""
    
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        """初始化 RAG 系统"""
        logger.info("🔄 加载向量模型...")
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.documents = []  # 只存储文档内容（字符串）
        self.metadata = []   # 分开存储元数据（字典）
        self.index = None
        logger.info("✅ 向量模型加载完成")
        
    def load_knowledge_base(self, kb_path='knowledge_base'):
        """从文件加载知识库"""
        logger.info(f"📚 从 {kb_path} 加载知识库...")
        self.documents = []
        self.metadata = []
        
        kb_dir = Path(kb_path)
        if not kb_dir.exists():
            logger.warning(f"⚠️  {kb_path} 目录不存在")
            return
        
        # 递归遍历所有 Markdown 文件
        md_files = list(kb_dir.rglob('*.md'))
        logger.info(f"🔍 找到 {len(md_files)} 个 Markdown 文件")
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 按标题分割文档
                    chunks = self._chunk_text(content)
                    
                    for chunk_content, chunk_meta in chunks:
                        self.documents.append(chunk_content)  # ✅ 只存储内容
                        self.metadata.append({  # ✅ 分开存储元数据
                            'source': md_file.name,
                            'source_path': str(md_file),
                            **chunk_meta
                        })
                    
                    logger.info(f"✅ 加载: {md_file.name} ({len(chunks)} 块)")
            except Exception as e:
                logger.error(f"❌ 加载失败 {md_file}: {e}")
        
        logger.info(f"✅ 已加载 {len(self.documents)} 个文档块")
        
    def _chunk_text(self, text, chunk_size=500, overlap=100):
        """将长文本分割成块
        
        Returns:
            列表，每个元素是 (文档内容, 元数据字典) 的元组
        """
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_length = 0
        
        for line in lines:
            current_chunk.append(line)
            current_length += len(line)
            
            if current_length > chunk_size:
                chunk_text = '\n'.join(current_chunk)
                if chunk_text.strip():
                    chunks.append((
                        chunk_text,  # 文档内容（字符串）
                        {'length': len(chunk_text)}  # 元数据
                    ))
                
                # 保留部分重叠
                current_chunk = current_chunk[-overlap//50:]
                current_length = sum(len(l) for l in current_chunk)
        
        # 添加最后的块
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            if chunk_text.strip():
                chunks.append((
                    chunk_text,
                    {'length': len(chunk_text)}
                ))
        
        return chunks
    
    def build_index(self):
        """构建 FAISS 索引"""
        if not self.documents:
            logger.error("❌ 错误: 没有加载文档")
            return
        
        logger.info(f"🔄 向量化 {len(self.documents)} 个文档...")
        
        # ✅ 直接向量化文档（全是字符串）
        self.embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        
        logger.info(f"✅ 向量化完成，向量维度: {self.embeddings.shape}")
        
        # 构建 FAISS 索引
        logger.info("🔄 构建 FAISS 索引...")
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype(np.float32))
        
        logger.info(f"✅ 索引构建完成，包含 {self.index.ntotal} 个向量")
        
    def retrieve(self, query, top_k=3):
        """检索相关文档"""
        if self.index is None:
            logger.warning("⚠️  索引未初始化")
            return []
        
        # 向量化查询
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        # 搜索最相似的文档
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype(np.float32),
            min(top_k, self.index.ntotal)
        )
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                # ✅ 直接从 documents 和 metadata 中获取
                content = self.documents[idx]
                metadata = self.metadata[idx]
                
                results.append({
                    'content': content,
                    'source': metadata.get('source', 'unknown'),
                    'score': float(1 - distance / 100)  # 相似度分数 0-1
                })
        
        logger.info(f"🔍 检索完成: 找到 {len(results)} 个相关文档")
        return results
    
    def save_index(self, index_path='rag_index'):
        """保存索引"""
        os.makedirs(index_path, exist_ok=True)
        
        try:
            # 保存 FAISS 索引
            faiss.write_index(self.index, f'{index_path}/faiss.index')
            
            # ✅ 分开保存文档和元数据
            with open(f'{index_path}/documents.json', 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            with open(f'{index_path}/metadata.json', 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 索引已保存到 {index_path}")
        except Exception as e:
            logger.error(f"❌ 保存索引失败: {e}")
    
    def load_index(self, index_path='rag_index'):
        """加载已保存的索引"""
        try:
            self.index = faiss.read_index(f'{index_path}/faiss.index')
            
            # ✅ 分开加载文档和元数据
            with open(f'{index_path}/documents.json', 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            
            with open(f'{index_path}/metadata.json', 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            
            logger.info(f"✅ 索引已加载，包含 {len(self.documents)} 个文档")
            return True
        except Exception as e:
            logger.warning(f"⚠️  加载索引失败: {e}")
            return False
    
    def get_status(self):
        """获取 RAG 系统状态"""
        return {
            'status': 'ready' if self.index else 'not_initialized',
            'documents_count': len(self.documents),
            'index_size': self.index.ntotal if self.index else 0,
            'model': 'paraphrase-multilingual-MiniLM-L12-v2'
        }