# import mysql.connector
# from config import MYSQL_CONFIG

# def get_connection():
#     return mysql.connector.connect(**MYSQL_CONFIG)

# def init_database():
#     """初始化数据库表（你已手动创建，此函数可跳过）"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS messages (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             session_id VARCHAR(64) NOT NULL,
#             role ENUM('user', 'assistant') NOT NULL,
#             content TEXT NOT NULL,
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
    
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("数据库初始化完成")

# def save_message(session_id: str, role: str, content: str):
#     """保存消息到数据库"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
#         (session_id, role, content)
#     )
    
#     conn.commit()
#     cursor.close()
#     conn.close()

# def get_history(session_id: str, limit: int = 20):
#     """获取对话历史"""
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
    
#     cursor.execute(
#         """SELECT role, content FROM messages 
#            WHERE session_id = %s 
#            ORDER BY created_at DESC LIMIT %s""",
#         (session_id, limit)
#     )
    
#     messages = cursor.fetchall()
#     cursor.close()
#     conn.close()
    
#     # 反转顺序，让最早的消息在前面
#     return list(reversed(messages))

# def clear_session(session_id: str):
#     """清除指定会话的所有消息"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "DELETE FROM messages WHERE session_id = %s",
#         (session_id,)
#     )
    
#     conn.commit()
#     cursor.close()
#     conn.close()
import mysql.connector
from config import MYSQL_CONFIG
import logging

logger = logging.getLogger(__name__)

def get_connection():
    """获取数据库连接"""
    try:
        return mysql.connector.connect(**MYSQL_CONFIG)
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        raise

def init_database():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(64) NOT NULL,
                role ENUM('user', 'assistant') NOT NULL,
                content LONGTEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_session (session_id),
                INDEX idx_created_at (created_at)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)
        
        conn.commit()
        logger.info("✅ 数据库初始化成功")
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")

def save_message(session_id: str, role: str, content: str):
    """保存消息到数据库"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content)
        )
        conn.commit()
        logger.info(f"✅ 消息已保存 ({role})")
    except Exception as e:
        logger.error(f"❌ 保存消息失败: {e}")
    finally:
        cursor.close()
        conn.close()

def get_history(session_id: str, limit: int = 50):  # ⬆️ 增加到 50
    """获取对话历史"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """SELECT role, content FROM messages 
               WHERE session_id = %s 
               ORDER BY created_at DESC LIMIT %s""",
            (session_id, limit)
        )
        
        messages = cursor.fetchall()
        return list(reversed(messages))
    except Exception as e:
        logger.error(f"❌ 获取历史失败: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def clear_session(session_id: str):
    """清除指定会话的所有消息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "DELETE FROM messages WHERE session_id = %s",
            (session_id,)
        )
        conn.commit()
        logger.info(f"✅ 会话已清除: {session_id}")
    except Exception as e:
        logger.error(f"❌ 清除会话失败: {e}")
    finally:
        cursor.close()
        conn.close()

def get_statistics():
    """获取统计信息"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_messages,
                COUNT(DISTINCT session_id) as total_sessions,
                SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as user_messages,
                SUM(CASE WHEN role = 'assistant' THEN 1 ELSE 0 END) as assistant_messages
            FROM messages
        """)
        
        return cursor.fetchone()
    except Exception as e:
        logger.error(f"❌ 获取统计信息失败: {e}")
        return None
    finally:
        cursor.close()
        conn.close()