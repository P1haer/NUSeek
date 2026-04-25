<template>
    <div class="app">
      <ChatBox />
    </div>
  </template>
  
  <script setup>
  import ChatBox from './components/ChatBox.vue'
  </script>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    
    /* 方案3: 淡青色 */
    background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);  
    min-height: 100vh;
  }
  
  .app {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }
  </style>