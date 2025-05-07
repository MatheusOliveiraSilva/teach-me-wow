'use client';

import React, { useState, useEffect, useRef, FormEvent } from 'react';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  meta?: any; // Para armazenar metadados do agente se necessário
}

interface LLMConfig {
  model: string;
  provider: string;
  // Adicione outros campos conforme definido em seus schemas FastAPI
}

interface ChatInterfaceProps {
  specIconUrl?: string; // Tornar a prop opcional
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ specIconUrl }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [currentAssistantMessageId, setCurrentAssistantMessageId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const chatContainerRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Efeito para simular uma mensagem inicial do assistente (opcional)
  useEffect(() => {
    setMessages([
      {
        id: 'initial-assistant-msg',
        sender: 'assistant',
        content: `Olá! Como posso te ajudar a dominar esta especialização hoje?`,
      }
    ]);
  }, []);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!userInput.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString() + '-user',
      sender: 'user',
      content: userInput,
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setUserInput('');
    setIsLoading(true);
    const assistantMsgId = Date.now().toString() + '-assistant';
    setCurrentAssistantMessageId(assistantMsgId);

    try {
      const llmConfig: LLMConfig = {
        model: 'gpt-4o', 
        provider: 'azure',
      };
      const requestBody = {
        message: { content: userMessage.content },
        llm_config: llmConfig,
      };

      const response = await fetch('http://localhost:8000/api/v1/agent/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      const reader = response.body?.getReader();
      if (!reader) throw new Error('Failed to get response reader');
      const decoder = new TextDecoder();
      let buffer = '';
      let firstChunkReceived = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        let eventEndIndex;
        while ((eventEndIndex = buffer.indexOf('\n\n')) !== -1) {
          const eventStr = buffer.substring(0, eventEndIndex);
          buffer = buffer.substring(eventEndIndex + 2);
          if (eventStr.startsWith('data: ')) {
            const jsonData = eventStr.substring(6);
            try {
              const parsedData = JSON.parse(jsonData);
              if (parsedData.content === null || parsedData.content === undefined) continue;

              setMessages((prevMessages) => {
                const assistantMsgIndex = prevMessages.findIndex(msg => msg.id === assistantMsgId);
                
                if (assistantMsgIndex !== -1) {
                  const updatedMessages = [...prevMessages];
                  updatedMessages[assistantMsgIndex] = {
                    ...updatedMessages[assistantMsgIndex],
                    content: updatedMessages[assistantMsgIndex].content + parsedData.content,
                    meta: parsedData.meta
                  };
                  return updatedMessages;
                } else {
                  return [
                    ...prevMessages,
                    {
                      id: assistantMsgId,
                      sender: 'assistant',
                      content: parsedData.content,
                      meta: parsedData.meta
                    }
                  ];
                }
              });

            } catch (error) {
              console.error('Failed to parse SSE data chunk:', jsonData, error);
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat stream error:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          id: assistantMsgId,
          sender: 'assistant',
          content: 'Error: Não foi possível conectar ao assistente. ' + (error instanceof Error ? error.message : String(error))
        }
      ]);
    } finally {
      setIsLoading(false);
      setCurrentAssistantMessageId(null);
    }
  };

  // Estilos adaptados para layout tela cheia tipo GPT
  return (
    <div 
      ref={chatContainerRef} 
      className="flex flex-col h-full w-full bg-gray-800 text-white overflow-hidden relative"
      // O bg-gray-800 aqui é o fundo da área de chat. O bg-gray-900 da página pai será o fundo geral.
    >
      {/* Header Opcional (se você quiser um no topo do chat) */}
      {/* <header className="p-4 border-b border-gray-700 text-center">
        <h1 className="text-xl font-semibold">
          {currentSpecialization ? `${currentSpecialization.name} ${currentSpecialization.class}` : 'Chat com Agente'}
        </h1>
      </header> */}

      {/* Área de Mensagens: O container de scroll ocupa a largura toda,
          mas o container interno com as mensagens é centralizado e tem max-width */}
      <div className="flex-grow overflow-y-auto w-full scroll-smooth">
        <div className="max-w-3xl mx-auto px-4 md:px-6 py-4 md:py-6 space-y-4">
          {messages.map((msg) => (
            <div 
              key={msg.id} 
              className={`flex items-start space-x-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {/* Avatar do Assistente */} 
              {msg.sender === 'assistant' && (
                <div className="flex-shrink-0 w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center border border-gray-500">
                  {specIconUrl ? (
                    <Image src={specIconUrl} alt="Spec Icon" width={24} height={24} className="rounded-full object-cover" />
                  ) : (
                    <span className="text-sm">AI</span> // Fallback se não houver ícone
                  )}
                </div>
              )}
              {/* Bolha da Mensagem */} 
              <div 
                className={`max-w-[85%] p-3 rounded-lg shadow-md prose prose-sm prose-invert prose-headings:text-yellow-400 prose-strong:text-white ${ // Adiciona classes prose para Markdown
                  msg.sender === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none order-last' // order-last para usuário
                    : 'bg-gray-700 text-gray-200 rounded-bl-none'
                }`}
              >
                 {/* Renderiza Markdown para assistente, texto normal para usuário */}
                 {msg.sender === 'assistant' ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                 ) : (
                    msg.content.split('\n').map((line, index) => (
                      <React.Fragment key={index}>
                        {line}
                        {index < msg.content.split('\n').length - 1 && <br />}
                      </React.Fragment>
                    ))
                 )}
              </div>
            </div>
          ))}
          {/* Indicador de Loading: Renderizado apenas quando isLoading é true */}
          {isLoading && (
              <div className="flex items-start space-x-3 justify-start">
                  {/* Avatar do Assistente para o Loading */} 
                  <div className="flex-shrink-0 w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center border border-gray-500">
                     {specIconUrl ? (
                      <Image src={specIconUrl} alt="Spec Icon" width={24} height={24} className="rounded-full object-cover" />
                    ) : (
                      <span className="text-sm">AI</span>
                    )}
                  </div>
                  {/* Bolha de Loading */} 
                  <div className="max-w-[85%] p-3 rounded-lg shadow-md bg-gray-700 text-gray-200 rounded-bl-none">
                      <div className="loading-dots" style={{display: 'inline-block'}}>
                          <span style={{animation: 'blink 1.4s infinite both', animationDelay:'0s'}}>.</span>
                          <span style={{animation: 'blink 1.4s infinite both', animationDelay:'0.2s'}}>.</span>
                          <span style={{animation: 'blink 1.4s infinite both', animationDelay:'0.4s'}}>.</span>
                      </div>
                  </div>
              </div>
          )}
          <div ref={messagesEndRef} />
        </div> { /* Fim do container interno centralizado */}
      </div> { /* Fim da área de scroll */}

      {/* Formulário de Input Fixo no Fundo: O container externo tem a borda,
          mas o formulário interno é centralizado e tem max-width */}
      <div className="w-full px-4 md:px-6 py-3 border-t border-gray-700 bg-gray-800 flex-shrink-0">
        <div className="max-w-3xl mx-auto"> { /* Container interno centralizado */}
          <form onSubmit={handleSubmit} className="flex items-center space-x-2">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Converse com o Mestre do Conhecimento..."
              className="flex-grow p-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-200 placeholder-gray-500"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className={`p-3 rounded-lg text-white transition-colors ${isLoading ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
              disabled={isLoading}
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path d="M3.105 3.105a1.5 1.5 0 012.122-.001l1.06 1.061a.5.5 0 00.707 0l1.06-1.06a.5.5 0 00-.707-.708L5.122 3.105a.5.5 0 00-.707.707l1.06 1.06a.5.5 0 00.707 0l1.061-1.06a1.5 1.5 0 012.121.001l1.061 1.06a.5.5 0 00.708 0l1.06-1.06a.5.5 0 00-.707-.707l-1.06 1.06a.5.5 0 00-.707 0l-1.061-1.06a1.5 1.5 0 01-2.121-.001L9.121 4.875a.5.5 0 00-.707 0L7.354 3.815a.5.5 0 00-.707.707l1.06 1.06a.5.5 0 00.708 0l1.06-1.06a1.5 1.5 0 012.122.001l1.06 1.061a.5.5 0 00.707 0l1.06-1.06a.5.5 0 00-.707-.708L13.122 3.105a.5.5 0 00-.707.707l1.06 1.06a.5.5 0 00.707 0L15.242 2.81a1.5 1.5 0 012.122-.001l.217.217a1.5 1.5 0 010 2.121l-6.828 6.828a1.5 1.5 0 01-2.121 0l-6.828-6.828a1.5 1.5 0 010-2.121L3.105 3.105zM2.44 15.88a.75.75 0 001.06 0l1.06-1.061a.5.5 0 01.707 0l1.061 1.06a.5.5 0 010 .708l-1.06 1.06a.5.5 0 01-.707 0l-1.061-1.06a.75.75 0 00-1.06 0z" />
              </svg>
            </button>
          </form>
        </div> { /* Fim do container interno centralizado */}
      </div> { /* Fim da área de input */}
    </div>
  );
};

export default ChatInterface; 