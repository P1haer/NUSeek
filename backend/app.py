# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI
# import uuid
# from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
# from database import init_database, save_message, get_history

# app = Flask(__name__)
# CORS(app)

# # 初始化 DeepSeek 客户端
# client = OpenAI(
#     api_key=DEEPSEEK_API_KEY,
#     base_url=DEEPSEEK_BASE_URL
# )

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     """处理聊天请求"""
#     data = request.json
#     user_message = data.get("message", "")
#     session_id = data.get("session_id", str(uuid.uuid4()))
    
#     if not user_message:
#         return jsonify({"error": "消息不能为空"}), 400
    
#     # 保存用户消息
#     save_message(session_id, "user", user_message)
    
#     # 获取历史对话
#     history = get_history(session_id)
    
#     # 构建消息列表
#     messages = [{"role": "system", "content": "你是一个友好的AI助手"}]
#     messages.extend(history)
    
#     try:
#         # 调用 DeepSeek API
#         response = client.chat.completions.create(
#             model="deepseek-chat",
#             messages=messages,
#             temperature=0.7,
#             max_tokens=2000
#         )
        
#         assistant_message = response.choices[0].message.content
        
#         # 保存助手回复
#         save_message(session_id, "assistant", assistant_message)
        
#         return jsonify({
#             "reply": assistant_message,
#             "session_id": session_id
#         })
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/api/history/<session_id>", methods=["GET"])
# def history(session_id):
#     """获取对话历史"""
#     messages = get_history(session_id)
#     return jsonify({"messages": messages})

# @app.route("/api/new-session", methods=["POST"])
# def new_session():
#     """创建新会话"""
#     return jsonify({"session_id": str(uuid.uuid4())})

# if __name__ == "__main__":
#     init_database()
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import uuid
import logging
import os
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, RAG_CONFIG, ENV
from database import init_database, save_message, get_history
from rag_system import RAGSystem

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)

# 初始化 RAG 系统
logger.info("🚀 初始化 RAG 系统...")
rag = RAGSystem(model_name=RAG_CONFIG['model_name'])

if not rag.load_index(RAG_CONFIG['index_path']):
    logger.warning("⚠️  RAG 索引不存在，正在构建...")
    rag.load_knowledge_base(RAG_CONFIG['kb_path'])
    if len(rag.documents) > 0:
        rag.build_index()
        rag.save_index(RAG_CONFIG['index_path'])
        logger.info("✅ RAG 索引构建完成")
    else:
        logger.warning("⚠️  知识库为空")
else:
    logger.info("✅ RAG 系统初始化完成")

# NUS 系统提示词
SYSTEM_PROMPT = """你是 NUS Assistant，新加坡国立大学（National University of Singapore）的官方 AI 助手。

【关于你的角色】
- 你对 NUS 的学位项目、招生要求、奖学金计划有深入了解
- 你熟悉 NUS 的学生生活、宿舍、费用、学术政策
- 你能用中文、英文流畅地回答问题
- 你友好、专业、准确

【重要指引】
- 始终基于提供的知识库信息回答
- 对于超出知识库的问题，建议访问 nus.edu.sg
- 如果不确定，请坦诚说明

【语气】
- 专业但友好
- 清晰且有条理"""

def extract_category(content):
    """从内容中提取分类标签"""
    content_lower = content.lower()
    
    categories = {
        'computing': '📚 计算机科学',
        'computer science': '📚 计算机科学',
        '申请': '🎓 招生信息',
        'admission': '🎓 招生信息',
        'requirement': '🎓 招生信息',
        '宿舍': '🏠 学生生活',
        'housing': '🏠 学生生活',
        'residence': '🏠 学生生活',
        '奖学金': '💰 奖学金',
        'scholarship': '💰 奖学金',
        '研究': '🔬 研究',
        'research': '🔬 研究',
        '学费': '💵 费用',
        'tuition': '💵 费用',
        'fee': '💵 费用',
        '学术': '📖 学术政策',
        'academic': '📖 学术政策',
    }
    
    for key, category in categories.items():
        if key in content_lower:
            return category
    
    return '📋 学校信息'

@app.route("/api/health", methods=["GET"])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "ok",
        "service": "NUS AI Chatbot",
        "environment": ENV,
        "rag_status": rag.get_status()
    }), 200

@app.route("/api/chat", methods=["POST"])
def chat():
    """处理聊天请求（带 RAG）"""
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400
        
        logger.info(f"📨 新消息: {user_message[:50]}...")
        
        # 保存用户消息
        save_message(session_id, "user", user_message)
        
        # ========== RAG 检索 ==========
        logger.info(f"🔍 从知识库检索相关信息...")
        retrieved_docs = rag.retrieve(user_message, top_k=RAG_CONFIG['top_k'])
        
        # 构建 RAG 上下文
        rag_context = ""
        if retrieved_docs:
            rag_context = "【参考信息】\n"
            for i, doc in enumerate(retrieved_docs, 1):
                rag_context += f"\n📌 来源 {i}:\n{doc['content'][:500]}...\n"
            rag_context += "\n---\n"
            logger.info(f"✅ 检索到 {len(retrieved_docs)} 个文档")
        else:
            logger.warning("⚠️  没有检索到相关文档")
        
        # 获取对话历史
        history = get_history(session_id, limit=50)
        
        # 构建消息列表
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + "\n\n" + rag_context
            }
        ]
        messages.extend(history)
        
        # ========== 调用 DeepSeek API ==========
        logger.info(f"🤖 调用 DeepSeek API...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=8192,
            top_p=0.95
        )
        
        assistant_message = response.choices[0].message.content
        
        # 保存助手回复
        save_message(session_id, "assistant", assistant_message)
        logger.info(f"✅ 回复已保存")
        
        # 返回响应
        return jsonify({
            "reply": assistant_message,
            "session_id": session_id,
            "sources": [
                {
                    "content": doc['content'][:300],
                    "score": round(doc['score'] * 100, 1),
                    "category": extract_category(doc['content']),
                    "source_file": doc.get('source', 'unknown')
                }
                for doc in retrieved_docs
            ]
        }), 200
        
    except Exception as e:
        logger.error(f"❌ 处理请求失败: {e}", exc_info=True)
        return jsonify({"error": f"处理请求失败: {str(e)}"}), 500

@app.route("/api/history/<session_id>", methods=["GET"])
def history(session_id):
    """获取对话历史"""
    try:
        messages = get_history(session_id, limit=50)
        return jsonify({"messages": messages}), 200
    except Exception as e:
        logger.error(f"❌ 获取历史失败: {e}")
        return jsonify({"error": "获取历史失败"}), 500

@app.route("/api/new-session", methods=["POST"])
def new_session():
    """创建新会话"""
    session_id = str(uuid.uuid4())
    logger.info(f"✅ 创建新会话: {session_id[:8]}...")
    return jsonify({"session_id": session_id}), 200

@app.route("/api/rag-status", methods=["GET"])
def rag_status():
    """获取 RAG 系统状态"""
    try:
        status = rag.get_status()
        return jsonify({
            "status": "ready",
            "rag_info": status
        }), 200
    except Exception as e:
        logger.error(f"❌ 获取 RAG 状态失败: {e}")
        return jsonify({"error": "获取状态失败"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "端点不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("🚀 NUS AI Chatbot 启动中...")
    logger.info(f"环境: {ENV}")
    logger.info(f"RAG 状态: {rag.get_status()}")
    logger.info("="*70)
    
    init_database()
    
    debug_mode = ENV == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode,
        use_reloader=debug_mode
    )