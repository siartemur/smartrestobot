(function () {
  const style = document.createElement('style');
  style.innerHTML = `
    #smartresto-chatbot {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 300px;
      max-height: 400px;
      background: white;
      border: 1px solid #ccc;
      border-radius: 8px;
      box-shadow: 0 0 12px rgba(0,0,0,0.15);
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      z-index: 9999;
    }
    #smartresto-chat-header {
      background: #444;
      color: white;
      padding: 8px;
      font-weight: bold;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
    }
    #smartresto-chat-messages {
      flex: 1;
      padding: 8px;
      overflow-y: auto;
      font-size: 14px;
    }
    #smartresto-chat-input {
      display: flex;
      border-top: 1px solid #ccc;
    }
    #smartresto-chat-input input {
      flex: 1;
      padding: 8px;
      border: none;
      outline: none;
    }
    #smartresto-chat-input button {
      background: #1e90ff;
      color: white;
      border: none;
      padding: 8px 12px;
      cursor: pointer;
    }
  `;
  document.head.appendChild(style);

  const chatbot = document.createElement('div');
  chatbot.id = 'smartresto-chatbot';
  chatbot.innerHTML = `
    <div id="smartresto-chat-header">SmartRestoBot</div>
    <div id="smartresto-chat-messages"></div>
    <div id="smartresto-chat-input">
      <input type="text" placeholder="Mesajınızı yazın..." />
      <button>Gönder</button>
    </div>
  `;
  document.body.appendChild(chatbot);

  const messages = document.getElementById('smartresto-chat-messages');
  const input = chatbot.querySelector('input');
  const button = chatbot.querySelector('button');

  function addMessage(role, text) {
    const div = document.createElement('div');
    div.textContent = `${role === 'user' ? '🧑‍🍳' : '🤖'} ${text}`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  button.onclick = async () => {
    const text = input.value.trim();
    if (!text) return;
    addMessage('user', text);
    input.value = '';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      addMessage('bot', data.response);
    } catch (err) {
      addMessage('bot', 'Bir hata oluştu.');
    }
  };
})();
