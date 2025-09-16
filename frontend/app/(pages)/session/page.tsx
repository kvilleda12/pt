'use client';
import React, { useState, useEffect, useRef } from 'react';
import Webcam from 'react-webcam';

interface Message {
  text: string;
  isUser: boolean;
}

const ChatMessage: React.FC<{ message: string; isUser: boolean; }> = ({ message, isUser }) => {
  const messageClass = isUser 
    ? 'bg-purple-200 text-purple-900 self-end' 
    : 'bg-gray-200 text-gray-800 self-start';
  
  return (
    <div className={`w-fit max-w-lg rounded-xl px-4 py-3 shadow-sm ${messageClass}`}>
      <p className="text-sm">{message}</p>
    </div>
  );
};


export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I'm your AI Physical Therapy assistant. When you're ready, turn on your camera and type 'begin' to load your profile.", isUser: false }
  ]);

  //we check to see if these things are running for the user. Has camera loaded
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);
  
  //is the user signed in adn do we have access to there profile?
  const [userProfileContext, setUserProfileContext] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const webcamRef = useRef<Webcam>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const enableWebcam = () => setIsCameraOn(true);

  const handleSendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (userInput.trim() === '' || isLoading) return;

    const userMessage: Message = { text: userInput, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setUserInput('');
    setIsLoading(true);

    try {
      let currentContext = userProfileContext;

      // getting the users profile if its first time then storing it to use again and again
      if (userInput.trim().toLowerCase() === 'begin' && !currentContext) {
        const currentUserId = 1; // Replace with the user_id
        const contextResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/llm/get_context`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: currentUserId }),
        });
        const contextData = await contextResponse.json();
        currentContext = contextData.context;
        setUserProfileContext(currentContext); // store context
        
        // Confirm with the user
        const botMessage: Message = { text: "Great! I've loaded your profile. How can I help you today?", isUser: false };
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
        return; // End the function here for this special case
      }

      // fallback and let user know to start. Might not be necessary because its a waste of tokens. For testing purposes
      //leave it commented out until its ready
      //if (!currentContext) {
     //   const botMessage: Message = { text: "Please type 'lets begin' so we can start the session", isUser: false };
     //   setMessages(prev => [...prev, botMessage]);
     //   setIsLoading(false);
     //   return;
    //  }

      // use the user_profile on every message. bascially now we query through excersices taking the user profile into account
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/llm/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userInput,
          user_profile_context: currentContext 
        }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      const botResponse: Message = { text: data.response, isUser: false };
      setMessages(prev => [...prev, botResponse]);

    } catch (error) {
      console.error("Failed to get response from bot:", error);
      const errorResponse: Message = { text: "Sorry, I'm having trouble connecting right now.", isUser: false };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  //page layout
  return (
    <div style={{
      background: '#1E1B4B',
      minHeight: '100svh',
      display: 'flex',
      flexDirection: 'column',
      color: 'var(--foreground, #fff)',
      fontFamily: 'var(--font-geist-sans, sans-serif)',
      padding: '2rem 1rem',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <main style={{
        display: 'grid',
        gridTemplateColumns: '1.5fr 1fr',
        width: '100%',
        maxWidth: '95vw',
        gap: '2rem',
        alignItems: 'center',
      }}>
        {/* Camera Section */}
        <div style={{ textAlign: 'center' }}>
          {isCameraOn ? (
            <div style={{ background: '#000', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.2)' }}>
              <Webcam
                ref={webcamRef}
                audio={false}
                mirrored={true}
                style={{ width: '100%', display: 'block' }}
                screenshotFormat="image/jpeg"
              />
            </div>
          ) : (
            <div style={{
              height: '70vh',
              maxHeight: '700px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: '12px',
              border: '1px dashed rgba(255,255,255,0.2)'
            }}>
              <h1 style={{ fontSize: '2.5rem', fontWeight: 600, marginBottom: '0.5rem' }}>Camera Access</h1>
              <p style={{ fontSize: '1.1rem', color: '#A5B4FC', marginBottom: '1.5rem' }}>Please enable your camera for movement analysis.</p>
              <button style={{
                background: 'rgba(255, 255, 255, 0.1)',
                color: '#fff',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                padding: '10px 20px',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 500,
                cursor: 'pointer',
                transition: 'background 0.2s',
              }}
              onClick={enableWebcam}
              >
                Enable Camera
              </button>
            </div>
          )}
        </div>

        {/* Chat Interface */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          background: '#fff',
          color: '#000',
          borderRadius: '12px',
          boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          overflow: 'hidden',
          height: '70vh',
          maxHeight: '700px',
        }}>
          <div style={{ flexGrow: 1, overflowY: 'auto', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
            ))}
            {isLoading && (
              <div className="self-start">
                <div className="bg-gray-200 rounded-xl px-4 py-3 shadow-sm">
                  <span className="animate-pulse">...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
          <form onSubmit={handleSendMessage} style={{
            display: 'flex',
            padding: '1rem',
            borderTop: '1px solid #E5E7EB',
            background: '#F9FAFB',
          }}>
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your message..."
              style={{
                flexGrow: 1,
                background: '#fff',
                border: '1px solid #D1D5DB',
                borderRadius: '8px',
                padding: '10px',
                color: '#1F2937',
                fontSize: '1rem',
                outline: 'none',
              }}
            />
            <button type="submit" style={{
              background: '#4338CA',
              color: '#fff',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '8px',
              marginLeft: '0.75rem',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: 'pointer',
              opacity: isLoading ? 0.5 : 1,
            }}
            disabled={isLoading}
            >
              Send
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}