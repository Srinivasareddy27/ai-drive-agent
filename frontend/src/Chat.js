import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMsg = { type: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        query: query,
      });

      const botMsg = {
        type: "bot",
        text: res.data.answer,
        sources: res.data.sources,
      };

      setMessages((prev) => [...prev, botMsg]);
      setQuery("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      
      {/* Sidebar */}
      <div style={styles.sidebar}>
        <h2>AI Drive</h2>
        <p>Chat with your Google Drive files</p>
      </div>

      {/* Chat Area */}
      <div style={styles.chatArea}>
        
        {/* Messages */}
        <div style={styles.messages}>
          {messages.map((msg, index) => (
            <div
              key={index}
              style={
                msg.type === "user"
                  ? styles.userMessage
                  : styles.botMessage
              }
            >
              <p>{msg.text}</p>
              {msg.sources && (
                <small style={styles.source}>
                  📄 {msg.sources.join(", ")}
                </small>
              )}
            </div>
          ))}
        </div>

        {/* Input */}
        <div style={styles.inputArea}>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask something about your files..."
            style={styles.input}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage} style={styles.button}>
            Send
          </button>
        </div>

      </div>
    </div>
  );
}

export default Chat;

const styles = {
  container: {
    display: "flex",
    height: "100vh",
    fontFamily: "Arial, sans-serif",
  },

  sidebar: {
    width: "250px",
    background: "#202123",
    color: "white",
    padding: "20px",
  },

  chatArea: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    background: "#343541",
  },

  messages: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
  },

  userMessage: {
    background: "#0b93f6",
    color: "white",
    padding: "12px",
    borderRadius: "12px",
    marginBottom: "10px",
    maxWidth: "60%",
    alignSelf: "flex-end",
  },

  botMessage: {
    background: "#444654",
    color: "white",
    padding: "12px",
    borderRadius: "12px",
    marginBottom: "10px",
    maxWidth: "60%",
    alignSelf: "flex-start",
  },

  source: {
    fontSize: "12px",
    opacity: 0.7,
  },

  inputArea: {
    display: "flex",
    padding: "10px",
    background: "#40414f",
  },

  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    outline: "none",
    marginRight: "10px",
  },

  button: {
    padding: "12px 20px",
    background: "#19c37d",
    border: "none",
    borderRadius: "8px",
    color: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },
};