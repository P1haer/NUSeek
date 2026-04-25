# import os
# from dotenv import load_dotenv

# load_dotenv()


# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# MYSQL_CONFIG = {
#     "host": os.getenv("MYSQL_HOST", "localhost"),
#     "user": os.getenv("MYSQL_USER", "root"),
#     "password": os.getenv("MYSQL_PASSWORD", ""),
#     "database": os.getenv("MYSQL_DATABASE", "chatbot_db")
# }
import os
from dotenv import load_dotenv

load_dotenv()

# ========== 环境检测 ==========
ENV = os.getenv('FLASK_ENV', 'development')

# ========== DeepSeek 配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ========== MySQL 数据库配置 ==========
if ENV == 'production':
    # 生产环境：使用云数据库（支持 Railway）
    MYSQL_CONFIG = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "autocommit": True,
        "pool_name": "mypool",
        "pool_size": 5
    }
else:
    # 开发环境：使用本地数据库
    MYSQL_CONFIG = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "chatbot_db"),
        "port": 3306
    }

# ========== NUS 配置 ==========
NUS_CONFIG = {
    "university": "National University of Singapore",
    "location": "Singapore",
    "website": "nus.edu.sg",
    "main_campus": "Kent Ridge Campus",
    "contact_email": "admissions@nus.edu.sg",
    "phone": "+65 6874 2966"
}

# ========== RAG 配置 ==========
RAG_CONFIG = {
    "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "kb_path": "knowledge_base",
    "index_path": "rag_index",
    "chunk_size": 500,
    "chunk_overlap": 100,
    "top_k": 5  # 检索前 5 个相关文档
}

# ========== 日志配置 ==========
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')