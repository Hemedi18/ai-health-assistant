document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const chatInterface = document.querySelector('.chat-interface');
    const sendBtn = document.getElementById('send-btn');

    // Initial scroll to bottom
    scrollToBottom();

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Disable input state
        setInputState(false);

        // Add user message immediately
        addMessage(message, 'user');
        userInput.value = '';

        // Add loading indicator
        const loadingId = addLoadingIndicator();

        try {
            // Send request to the chat API endpoint
            const response = await fetch('/chat/api/send/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    'message': message
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Remove loading indicator
            removeMessage(loadingId);

            // Handle response
            if (data.error) {
                addMessage('Error: ' + data.error, 'ai');
            } else {
                // Use 'response' or 'message' depending on your Django view's JSON structure
                const aiResponse = data.response || data.message || "I didn't get a response.";
                addMessage(aiResponse, 'ai');
            }

        } catch (error) {
            removeMessage(loadingId);
            addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            console.error('Chat error:', error);
        } finally {
            setInputState(true);
            userInput.focus();
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        // Avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = `avatar ${sender}-avatar`;
        avatarDiv.innerHTML = sender === 'ai' 
            ? '<i class="fa-solid fa-robot"></i>' 
            : '<i class="fa-solid fa-user"></i>';
        
        // Bubble
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'bubble';
        
        // Render Markdown for AI, plain text for user
        if (sender === 'ai' && typeof marked !== 'undefined') {
            bubbleDiv.innerHTML = marked.parse(text);
        } else {
            bubbleDiv.textContent = text;
        }

        // Append order: Avatar then Bubble (CSS handles visual reversal for user)
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);

        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function addLoadingIndicator() {
        const id = 'thinking-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ai-message';
        messageDiv.id = id;
        
        messageDiv.innerHTML = `
            <div class="avatar ai-avatar">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="bubble">
                <i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...
            </div>
        `;
        
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatInterface.scrollTop = chatInterface.scrollHeight;
    }

    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendBtn.disabled = !enabled;
        if (enabled) {
            sendBtn.innerHTML = '<span>Send</span><i class="fa-solid fa-paper-plane"></i>';
            sendBtn.style.cursor = 'pointer';
        } else {
            sendBtn.innerHTML = '<span>Sending...</span><i class="fa-solid fa-spinner fa-spin"></i>';
            sendBtn.style.cursor = 'not-allowed';
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
