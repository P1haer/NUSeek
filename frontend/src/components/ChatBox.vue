  <!-- <template>
    <div class="chat-container">
      <div class="chat-header">
        <h1>🦁 NUSeek</h1>
        <button @click="newSession" class="new-chat-btn">
          <span>✨</span> 新对话
        </button>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-icon">🦁</div>
          <h2>你好，我是 NUSeek</h2>
          <p>有什么可以帮助你的吗？</p>
        </div>
        
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="avatar">{{ msg.role === 'user' ? '👤' : '🦁' }}</div>
          <div class="content">{{ msg.content }}</div>
        </div>
        
        <div v-if="isLoading" class="message assistant">
          <div class="avatar">🦁</div>
          <div class="content loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
      
      <div class="chat-input-wrapper">
        <div class="chat-input">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            placeholder="输入你的问题..."
            :disabled="isLoading"
          />
          <button @click="sendMessage" :disabled="isLoading || !inputMessage.trim()">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
        <p class="input-hint">按 Enter 发送消息</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, nextTick, onMounted } from 'vue'
  import axios from 'axios'
  
  const messages = ref([])
  const inputMessage = ref('')
  const isLoading = ref(false)
  const sessionId = ref('')
  const messagesContainer = ref(null)
  
  onMounted(() => {
    newSession()
  })
  
  const newSession = async () => {
    try {
      const response = await axios.post('/api/new-session')
      sessionId.value = response.data.session_id
      messages.value = []
    } catch (error) {
      console.error('创建会话失败:', error)
    }
  }
  
  const scrollToBottom = () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }
  
  const sendMessage = async () => {
    const message = inputMessage.value.trim()
    if (!message || isLoading.value) return
    
    messages.value.push({ role: 'user', content: message })
    inputMessage.value = ''
    isLoading.value = true
    scrollToBottom()
    
    try {
      const response = await axios.post('/api/chat', {
        message: message,
        session_id: sessionId.value
      })
      
      messages.value.push({ 
        role: 'assistant', 
        content: response.data.reply 
      })
      
    } catch (error) {
      messages.value.push({ 
        role: 'assistant', 
        content: '抱歉，发生了错误，请稍后重试。' 
      })
      console.error('发送消息失败:', error)
    } finally {
      isLoading.value = false
      scrollToBottom()
    }
  }
  </script>
  
  <style scoped>
  /* 容器 */
  .chat-container {
    width: 100%;
    max-width: 900px;
    height: 92vh;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 
      0 4px 24px rgba(0, 0, 0, 0.06),
      0 1px 2px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.06);
  }
  
  /* 头部 */
  .chat-header {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 20px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .chat-header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2d3748;
    margin: 0;
  }
  
  .new-chat-btn {
    background: rgba(255, 255, 255, 0.8);
    color: #4a5568;
    border: none;
    padding: 10px 20px;
    border-radius: 50px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    backdrop-filter: blur(10px);
  }
  
  .new-chat-btn:hover {
    background: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  /* 消息区域 */
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    background: linear-gradient(180deg, #fafbfc 0%, #ffffff 100%);
  }
  
  /* 滚动条美化 */
  .chat-messages::-webkit-scrollbar {
    width: 6px;
  }
  
  .chat-messages::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .chat-messages::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 3px;
  }
  
  .chat-messages::-webkit-scrollbar-thumb:hover {
    background: #cbd5e0;
  }
  
  /* 欢迎消息 */
  .welcome-message {
    text-align: center;
    padding: 60px 20px;
    color: #718096;
  }
  
  .welcome-icon {
    font-size: 4rem;
    margin-bottom: 16px;
    animation: bounce 2s infinite;
  }
  
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  
  .welcome-message h2 {
    font-size: 1.5rem;
    color: #2d3748;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .welcome-message p {
    font-size: 1rem;
    color: #a0aec0;
  }
  
  /* 消息样式 */
  .message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: slideIn 0.3s ease;
  }
  
  @keyframes slideIn {
    from { 
      opacity: 0; 
      transform: translateY(10px); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0); 
    }
  }
  
  .message.user {
    flex-direction: row-reverse;
  }
  
  .avatar {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
  }
  
  .message.user .avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .message.assistant .avatar {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  }
  
  .content {
    max-width: 70%;
    padding: 14px 18px;
    border-radius: 18px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 0.95rem;
  }
  
  .message.user .content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 6px;
  }
  
  .message.assistant .content {
    background: #f7fafc;
    color: #2d3748;
    border-bottom-left-radius: 6px;
    border: 1px solid #e2e8f0;
  }
  
  /* 加载动画 */
  .loading {
    display: flex;
    gap: 6px;
    padding: 18px 22px;
  }
  
  .dot {
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 50%;
    animation: pulse 1.4s infinite ease-in-out;
  }
  
  .dot:nth-child(1) { animation-delay: -0.32s; }
  .dot:nth-child(2) { animation-delay: -0.16s; }
  
  @keyframes pulse {
    0%, 80%, 100% { 
      transform: scale(0.6); 
      opacity: 0.5;
    }
    40% { 
      transform: scale(1); 
      opacity: 1;
    }
  }
  
  /* 输入区域 */
  .chat-input-wrapper {
    padding: 20px 24px;
    background: #ffffff;
    border-top: 1px solid #edf2f7;
  }
  
  .chat-input {
    display: flex;
    gap: 12px;
    background: #f7fafc;
    border-radius: 16px;
    padding: 6px;
    border: 2px solid #edf2f7;
    transition: all 0.3s ease;
  }
  
  .chat-input:focus-within {
    border-color: #a8edea;
    background: #ffffff;
    box-shadow: 0 0 0 4px rgba(168, 237, 234, 0.2);
  }
  
  .chat-input input {
    flex: 1;
    padding: 14px 16px;
    border: none;
    background: transparent;
    font-size: 1rem;
    color: #2d3748;
    outline: none;
  }
  
  .chat-input input::placeholder {
    color: #a0aec0;
  }
  
  .chat-input button {
    padding: 14px 24px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    color: #4a5568;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .chat-input button:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(168, 237, 234, 0.4);
  }
  
  .chat-input button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .input-hint {
    text-align: center;
    font-size: 0.8rem;
    color: #a0aec0;
    margin-top: 10px;
  }
  </style> -->
  <template>
    <div class="chat-container">
      <!-- 头部 -->
      <div class="chat-header">
        <div class="header-left">
          <h1>🦁 NUS Assistant</h1>
          <p class="subtitle">National University of Singapore</p>
        </div>
        <button @click="newSession" class="new-chat-btn">
          <span>✨</span> 新对话
        </button>
      </div>
      
      <!-- 消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-logo">🦁</div>
          <h2>欢迎来到 NUS</h2>
          <p class="welcome-subtitle">National University of Singapore - 新加坡国立大学</p>
          
          <!-- 快速问题按钮 -->
          <div class="quick-links">
            <button @click="quickQuestion('计算机科学专业包括哪些课程?')" class="quick-btn">
              📚 计算机科学
            </button>
            <button @click="quickQuestion('国际学生申请研究生需要什么条件?')" class="quick-btn">
              🎓 研究生申请
            </button>
            <button @click="quickQuestion('NUS有哪些奖学金?')" class="quick-btn">
              💰 奖学金
            </button>
            <button @click="quickQuestion('学生宿舍费用多少?')" class="quick-btn">
              🏠 学生生活
            </button>
          </div>
        </div>
        
        <!-- 消息列表 -->
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="avatar">{{ msg.role === 'user' ? '👤' : '🦁' }}</div>
          <div class="message-content">
            <!-- AI 消息使用 Markdown -->
            <div 
              v-if="msg.role === 'assistant'"
              class="content markdown-content"
              v-html="markdownToHtml(msg.content)"
            ></div>
            <!-- 用户消息纯文本 -->
            <div v-else class="content">{{ msg.content }}</div>
            
            <!-- 来源信息 -->
            <div v-if="msg.sources && msg.sources.length > 0" class="sources">
              <div class="sources-title">📚 参考来源</div>
              <div 
                v-for="(source, idx) in msg.sources"
                :key="idx"
                class="source-item"
                @click="toggleSource(msg, idx)"
              >
                <span class="source-category">{{ source.category }}</span>
                <span class="source-score">{{ source.score }}%</span>
                <span class="source-file">{{ source.source_file }}</span>
                <div v-if="expandedSources[getKey(msg)] === idx" class="source-detail">
                  {{ source.content }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载动画 -->
        <div v-if="isLoading" class="message assistant">
          <div class="avatar">🦁</div>
          <div class="content loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="chat-input-wrapper">
        <div class="chat-input">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            placeholder="输入你的问题..."
            :disabled="isLoading"
            class="input-field"
          />
          <button @click="sendMessage" :disabled="isLoading || !inputMessage.trim()" class="send-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
        <p class="input-hint">按 Enter 发送</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, nextTick, onMounted } from 'vue'
  import axios from 'axios'
  import { marked } from 'marked'
  import hljs from 'highlight.js'
  import 'highlight.js/styles/github.css'
  
  // ========== 配置 ==========
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
  
  // ========== 状态 ==========
  const messages = ref([])
  const inputMessage = ref('')
  const isLoading = ref(false)
  const sessionId = ref('')
  const messagesContainer = ref(null)
  const expandedSources = ref({})
  
  // ========== Markdown 配置 ==========
  marked.setOptions({
    breaks: true,
    gfm: true,
    highlight: (code, lang) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).highlighted
      }
      return hljs.highlightAuto(code).highlighted
    }
  })
  
  const markdownToHtml = (markdown) => marked(markdown)
  
  // ========== 方法 ==========
  const getKey = (msg) => JSON.stringify(msg).substring(0, 50)
  
  const quickQuestion = (question) => {
    inputMessage.value = question
    nextTick(() => {
      sendMessage()
    })
  }
  
  const toggleSource = (msg, idx) => {
    const key = getKey(msg)
    expandedSources.value[key] = expandedSources.value[key] === idx ? null : idx
  }
  
  onMounted(() => {
    newSession()
  })
  
  const newSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/new-session`)
      sessionId.value = response.data.session_id
      messages.value = []
    } catch (error) {
      console.error('创建会话失败:', error)
      alert('创建会话失败，请刷新页面重试')
    }
  }
  
  const scrollToBottom = () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }
  
  const sendMessage = async () => {
    const message = inputMessage.value.trim()
    if (!message || isLoading.value) return
    
    // 添加用户消息
    messages.value.push({ role: 'user', content: message })
    inputMessage.value = ''
    isLoading.value = true
    scrollToBottom()
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message: message,
        session_id: sessionId.value
      })
      
      // 添加 AI 回复
      messages.value.push({ 
        role: 'assistant', 
        content: response.data.reply,
        sources: response.data.sources || []
      })
      
    } catch (error) {
      console.error('发送消息失败:', error)
      messages.value.push({ 
        role: 'assistant', 
        content: '抱歉，发生了错误。请检查网络连接或稍后重试。'
      })
    } finally {
      isLoading.value = false
      scrollToBottom()
    }
  }
  </script>
  
  <style scoped>
  /* ========== 容器 ========== */
  .chat-container {
    width: 100%;
    max-width: 900px;
    height: 92vh;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.06);
  }
  
  /* ========== 头部 ========== */
  .chat-header {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 20px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .header-left {
    flex: 1;
  }
  
  .chat-header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2d3748;
    margin: 0;
  }
  
  .subtitle {
    font-size: 0.9rem;
    color: rgba(45, 55, 72, 0.8);
    margin: 4px 0 0 0;
  }
  
  .new-chat-btn {
    background: rgba(255, 255, 255, 0.8);
    color: #4a5568;
    border: none;
    padding: 10px 20px;
    border-radius: 50px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .new-chat-btn:hover {
    background: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  /* ========== 消息区域 ========== */
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    background: linear-gradient(180deg, #fafbfc 0%, #ffffff 100%);
  }
  
  .chat-messages::-webkit-scrollbar {
    width: 6px;
  }
  
  .chat-messages::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .chat-messages::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 3px;
  }
  
  .chat-messages::-webkit-scrollbar-thumb:hover {
    background: #cbd5e0;
  }
  
  /* ========== 欢迎消息 ========== */
  .welcome-message {
    text-align: center;
    padding: 40px 20px;
    color: #718096;
  }
  
  .welcome-logo {
    font-size: 4rem;
    margin-bottom: 16px;
    animation: bounce 2s infinite;
  }
  
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  
  .welcome-message h2 {
    font-size: 1.5rem;
    color: #2d3748;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
    color: #a0aec0;
    margin-bottom: 24px;
  }
  
  .quick-links {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    max-width: 500px;
    margin: 0 auto;
  }
  
  .quick-btn {
    padding: 12px 16px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.3s;
  }
  
  .quick-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(168, 237, 234, 0.4);
  }
  
  /* ========== 消息 ========== */
  .message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: slideIn 0.3s ease;
  }
  
  @keyframes slideIn {
    from { 
      opacity: 0; 
      transform: translateY(10px); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0); 
    }
  }
  
  .message.user {
    flex-direction: row-reverse;
  }
  
  .avatar {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
  }
  
  .message.user .avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .message.assistant .avatar {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  }
  
  .message-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .content {
    max-width: 70%;
    padding: 14px 18px;
    border-radius: 18px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 0.95rem;
  }
  
  .message.user .content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 6px;
  }
  
  .message.assistant .content {
    background: #f7fafc;
    color: #2d3748;
    border-bottom-left-radius: 6px;
    border: 1px solid #e2e8f0;
  }
  
  /* ========== Markdown 样式 ========== */
  .markdown-content h1,
  .markdown-content h2,
  .markdown-content h3 {
    margin: 16px 0 8px 0;
    font-weight: 600;
    color: #2d3748;
  }
  
  .markdown-content h1 {
    font-size: 1.4rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
  }
  
  .markdown-content h2 {
    font-size: 1.2rem;
  }
  
  .markdown-content h3 {
    font-size: 1.1rem;
  }
  
  .markdown-content p {
    margin: 8px 0;
  }
  
  .markdown-content code {
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.9em;
    color: #d63384;
  }
  
  .markdown-content pre {
    background: #1e293b;
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
    margin: 12px 0;
  }
  
  .markdown-content pre code {
    background: none;
    color: #e2e8f0;
    padding: 0;
  }
  
  .markdown-content ul,
  .markdown-content ol {
    margin: 8px 0;
    padding-left: 24px;
  }
  
  .markdown-content li {
    margin: 4px 0;
  }
  
  .markdown-content table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
  }
  
  .markdown-content th,
  .markdown-content td {
    border: 1px solid #e2e8f0;
    padding: 8px 12px;
    text-align: left;
  }
  
  .markdown-content th {
    background: #f7fafc;
  }
  
  /* ========== 加载动画 ========== */
  .loading {
    display: flex;
    gap: 6px;
    padding: 18px 22px;
  }
  
  .dot {
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 50%;
    animation: pulse 1.4s infinite ease-in-out;
  }
  
  .dot:nth-child(1) { animation-delay: -0.32s; }
  .dot:nth-child(2) { animation-delay: -0.16s; }
  
  @keyframes pulse {
    0%, 80%, 100% { 
      transform: scale(0.6); 
      opacity: 0.5;
    }
    40% { 
      transform: scale(1); 
      opacity: 1;
    }
  }
  
  /* ========== 来源信息 ========== */
  .sources {
    margin-top: 12px;
    padding: 12px;
    background: #f0f9ff;
    border-left: 3px solid #0284c7;
    border-radius: 6px;
    font-size: 0.85rem;
  }
  
  .sources-title {
    font-weight: 600;
    color: #0284c7;
    margin-bottom: 8px;
  }
  
  .source-item {
    cursor: pointer;
    padding: 8px;
    margin: 4px 0;
    background: white;
    border-radius: 4px;
    border: 1px solid #bfdbfe;
    transition: all 0.2s;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  
  .source-item:hover {
    background: #dbeafe;
    border-color: #0284c7;
  }
  
  .source-category {
    background: #0284c7;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    white-space: nowrap;
  }
  
  .source-score,
  .source-file {
    color: #666;
    font-size: 0.8rem;
  }
  
  .source-detail {
    width: 100%;
    margin-top: 8px;
    padding: 8px;
    background: #ecf0f1;
    border-radius: 4px;
    color: #333;
    line-height: 1.5;
  }
  
  /* ========== 输入区域 ========== */
  .chat-input-wrapper {
    padding: 20px 24px;
    background: #ffffff;
    border-top: 1px solid #edf2f7;
  }
  
  .chat-input {
    display: flex;
    gap: 12px;
    background: #f7fafc;
    border-radius: 16px;
    padding: 6px;
    border: 2px solid #edf2f7;
    transition: all 0.3s;
  }
  
  .chat-input:focus-within {
    border-color: #a8edea;
    background: #ffffff;
    box-shadow: 0 0 0 4px rgba(168, 237, 234, 0.2);
  }
  
  .input-field {
    flex: 1;
    padding: 14px 16px;
    border: none;
    background: transparent;
    font-size: 1rem;
    color: #2d3748;
    outline: none;
  }
  
  .input-field::placeholder {
    color: #a0aec0;
  }
  
  .send-btn {
    padding: 14px 24px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .send-btn:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(168, 237, 234, 0.4);
  }
  
  .send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .input-hint {
    text-align: center;
    font-size: 0.8rem;
    color: #a0aec0;
    margin-top: 10px;
  }
  
  /* ========== 响应式 ========== */
  @media (max-width: 768px) {
    .chat-container {
      max-width: 100%;
      height: 100vh;
      border-radius: 0;
    }
    
    .content {
      max-width: 90% !important;
    }
    
    .quick-links {
      grid-template-columns: 1fr;
    }
    
    .welcome-logo {
      font-size: 3rem;
    }
  }
  </style>