// Live Chat System with Admin Reply
(function() {
    // Create chat widget
    const chatHTML = `
    <div id="live-chat-widget" style="position: fixed; z-index: 99998; font-family: 'Segoe UI', Arial, sans-serif;">
        <!-- Chat Button (bottom left) -->
        <div id="live-chat-button" style="position: fixed; bottom: 220px; left: 20px; width: 55px; height: 55px; background: linear-gradient(135deg, #10B981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <i class="fas fa-headset" style="font-size: 26px; color: white;"></i>
            <span id="chat-notification" style="position: absolute; top: -5px; right: -5px; width: 12px; height: 12px; background: #EF4444; border-radius: 50%; border: 2px solid white; display: none;"></span>
        </div>
        
        <!-- Chat Window (centered, small) -->
        <div id="live-chat-window" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; height: 400px; max-width: 80vw; max-height: 70vh; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); overflow: hidden; flex-direction: column; z-index: 99999;">
            <div style="background: linear-gradient(135deg, #10B981, #059669); padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-headset" style="font-size: 20px; color: white;"></i>
                    <div>
                        <div style="font-weight: 600; color: white; font-size: 14px;">Live Support</div>
                        <div style="font-size: 10px; color: rgba(255,255,255,0.8);">Reply within minutes</div>
                    </div>
                </div>
                <button id="close-live-chat" style="background: none; border: none; color: white; font-size: 18px; cursor: pointer;">✕</button>
            </div>
            
            <div id="live-chat-messages" style="flex: 1; overflow-y: auto; padding: 15px; background: #F8FAFC; font-size: 13px;"></div>
            
            <div style="padding: 12px; background: white; border-top: 1px solid #E2E8F0;">
                <div style="display: flex; gap: 8px;">
                    <input type="text" id="live-chat-input" placeholder="Type your message..." style="flex: 1; padding: 10px 12px; border: 1px solid #E2E8F0; border-radius: 25px; outline: none; font-size: 13px;">
                    <button id="send-live-chat" style="width: 38px; height: 38px; background: #10B981; border: none; border-radius: 50%; cursor: pointer;">
                        <i class="fas fa-paper-plane" style="color: white; font-size: 14px;"></i>
                    </button>
                </div>
                <div style="text-align: center; margin-top: 8px;">
                    <span style="font-size: 10px; color: #888;">Powered by KHARY GLOBAL EDU</span>
                </div>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);
    
    let isOpen = false;
    let currentUserId = localStorage.getItem('chatUserId') || 'user_' + Math.random().toString(36).substr(2, 8);
    localStorage.setItem('chatUserId', currentUserId);
    
    const button = document.getElementById('live-chat-button');
    const chatWindow = document.getElementById('live-chat-window');
    const closeBtn = document.getElementById('close-live-chat');
    const input = document.getElementById('live-chat-input');
    const sendBtn = document.getElementById('send-live-chat');
    const messagesDiv = document.getElementById('live-chat-messages');
    const notification = document.getElementById('chat-notification');
    
    function loadMessages() {
        let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
        let userMessages = allMessages.filter(m => m.userId === currentUserId);
        
        messagesDiv.innerHTML = '';
        
        if(userMessages.length === 0) {
            messagesDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #888; font-size: 12px;">👋 Welcome! Ask us anything about studying in Asia.</div>';
        }
        
        userMessages.forEach(msg => {
            const msgDiv = document.createElement('div');
            msgDiv.style.display = 'flex';
            msgDiv.style.marginBottom = '10px';
            msgDiv.style.justifyContent = msg.isAdmin ? 'flex-start' : 'flex-end';
            
            const bubble = document.createElement('div');
            bubble.style.maxWidth = '75%';
            bubble.style.padding = '8px 12px';
            bubble.style.borderRadius = '15px';
            bubble.style.fontSize = '12px';
            bubble.style.lineHeight = '1.4';
            
            if(msg.isAdmin) {
                bubble.style.background = '#10B981';
                bubble.style.color = 'white';
                bubble.style.borderBottomLeftRadius = '3px';
                bubble.innerHTML = '<i class="fas fa-headset" style="font-size: 10px; margin-right: 4px;"></i> ' + msg.message;
            } else {
                bubble.style.background = '#D4AF37';
                bubble.style.color = '#1E3A8A';
                bubble.style.borderBottomRightRadius = '3px';
                bubble.innerHTML = msg.message;
            }
            
            msgDiv.appendChild(bubble);
            messagesDiv.appendChild(msgDiv);
        });
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function saveMessage(message, isAdmin) {
        let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
        allMessages.push({
            userId: currentUserId,
            message: message,
            isAdmin: isAdmin,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('liveChatMessages', JSON.stringify(allMessages));
        loadMessages();
        
        if(!isAdmin) {
            let adminChats = JSON.parse(localStorage.getItem('adminChats') || '[]');
            adminChats.push({ userId: currentUserId, message: message, timestamp: new Date().toISOString(), read: false });
            localStorage.setItem('adminChats', JSON.stringify(adminChats));
        }
    }
    
    function sendMessage() {
        const text = input.value.trim();
        if(!text) return;
        
        saveMessage(text, false);
        input.value = '';
        
        setTimeout(() => {
            saveMessage("✅ Thanks! We'll respond within 24 hours. Urgent? WhatsApp: +86 135 2246 4910", true);
        }, 500);
    }
    
    if(sendBtn) sendBtn.addEventListener('click', sendMessage);
    if(input) input.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });
    
    if(button) {
        button.addEventListener('click', () => {
            if(isOpen) {
                chatWindow.style.display = 'none';
                isOpen = false;
            } else {
                chatWindow.style.display = 'flex';
                isOpen = true;
                loadMessages();
                if(notification) notification.style.display = 'none';
            }
        });
    }
    
    if(closeBtn) {
        closeBtn.addEventListener('click', () => {
            chatWindow.style.display = 'none';
            isOpen = false;
        });
    }
    
    function checkNewMessages() {
        let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
        let userMessages = allMessages.filter(m => m.userId === currentUserId);
        let lastRead = localStorage.getItem('lastRead_' + currentUserId) || '0';
        
        let newMessages = userMessages.filter(m => new Date(m.timestamp) > new Date(lastRead) && m.isAdmin);
        
        if(newMessages.length > 0 && !isOpen && notification) {
            notification.style.display = 'block';
        }
        
        if(isOpen) loadMessages();
        
        localStorage.setItem('lastRead_' + currentUserId, new Date().toISOString());
    }
    
    setInterval(checkNewMessages, 5000);
    loadMessages();
})();