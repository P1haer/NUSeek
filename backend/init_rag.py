#!/usr/bin/env python3
"""
NUS RAG 知识库初始化脚本
"""

import os
import sys
from rag_system import RAGSystem
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_knowledge_base():
    """初始化 NUS 知识库"""
    
    print("\n" + "="*70)
    print(" 🦁 NUS AI Chatbot - RAG 知识库初始化")
    print("="*70)
    
    rag = RAGSystem()
    
    # 检查知识库目录
    kb_path = 'knowledge_base'
    if not os.path.exists(kb_path):
        print(f"\n❌ {kb_path} 目录不存在！")
        print("\n✅ 已创建目录结构，请按以下步骤操作:\n")
        
        # 创建目录结构
        os.makedirs(f'{kb_path}/schools', exist_ok=True)
        os.makedirs(f'{kb_path}/admissions', exist_ok=True)
        os.makedirs(f'{kb_path}/student_life', exist_ok=True)
        os.makedirs(f'{kb_path}/fees_funding', exist_ok=True)
        os.makedirs(f'{kb_path}/research', exist_ok=True)
        os.makedirs(f'{kb_path}/academics', exist_ok=True)
        os.makedirs(f'{kb_path}/campus', exist_ok=True)
        
        print("已创建目录:")
        print(f"  ✅ {kb_path}/schools/")
        print(f"  ✅ {kb_path}/admissions/")
        print(f"  ✅ {kb_path}/student_life/")
        print(f"  ✅ {kb_path}/fees_funding/")
        print(f"  ✅ {kb_path}/research/")
        print(f"  ✅ {kb_path}/academics/")
        print(f"  ✅ {kb_path}/campus/")
        
        print("\n📝 推荐的文档:")
        print("\nschools/ (⭐⭐⭐⭐⭐ 重要)")
        print("  - school_of_computing.md")
        print("  - engineering.md")
        print("  - business.md")
        
        print("\nadmissions/ (⭐⭐⭐⭐⭐ 重要)")
        print("  - undergraduate.md")
        print("  - graduate.md")
        print("  - international_students.md")
        
        print("\nstudent_life/ (⭐⭐⭐⭐)")
        print("  - housing.md")
        print("  - dining.md")
        print("  - transportation.md")
        
        print("\nfees_funding/ (⭐⭐⭐⭐⭐ 重要)")
        print("  - tuition_fees.md")
        print("  - scholarships.md")
        
        print("\n请将 Markdown 文件添加到相应目录，然后再次运行此脚本")
        print("="*70 + "\n")
        return False
    
    # 加载知识库
    print("\n📚 加载知识库文件...\n")
    rag.load_knowledge_base(kb_path)
    
    if len(rag.documents) == 0:
        print("❌ 未找到任何文档!")
        print(f"请确保已在 {kb_path} 中添加 .md 文件")
        return False
    
    print(f"\n✅ 成功加载 {len(rag.documents)} 个文档块\n")
    
    # 构建索引
    print("🔄 构建向量索引...\n")
    rag.build_index()
    
    # 保存索引
    print("\n💾 保存索引...\n")
    rag.save_index()
    
    # 显示状态
    status = rag.get_status()
    print("\n" + "="*70)
    print("✅ 初始化完成!")
    print("="*70)
    print(f"\n📊 系统状态:")
    print(f"  文档数: {status['documents_count']}")
    print(f"  索引大小: {status['index_size']}")
    print(f"  模型: {status['model']}")
    print(f"  状态: {status['status']}")
    
    print("\n🚀 后续步骤:")
    print("  1. 启动后端: python app.py")
    print("  2. 启动前端: npm run dev")
    print("  3. 访问应用: http://localhost:3000")
    print("\n祝你使用愉快! 🎓\n")
    
    return True

if __name__ == '__main__':
    success = init_knowledge_base()
    sys.exit(0 if success else 1)