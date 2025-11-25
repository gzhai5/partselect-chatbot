/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";
import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send as SendIcon } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from "remark-breaks";
import { generateUUID, generateInitialMessages, fallbackBotMessages } from './utils';
import { beginConversation, sendMessage } from '@/app/apis/chat/apis';
import { Message } from '@/app/apis/chat/interfaces';
import { useWebSocket } from '@/app/apis/hooks/useWebsocket';
import { invokeAi, verifyAIResponse, verifyUserQuery } from '@/app/apis/ai/apis';


export const ChatWidget = () => {
    const bottomRef = useRef<HTMLDivElement | null>(null);
    const [sessionId, setSessionId] = useState<string>('');
    const [query, setQuery] = useState<string>('');
    const [conversationHistory, setConversationHistory] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    useWebSocket(sessionId); // handle conversation start/end


    // Initialize conversation on component mounting, get session ID, and set up WS connection
    useEffect(() => {
        beginConversation({ startTime: new Date(), userId: `${'mockuser_' + generateUUID()}`, }).then(resp => { 
            setSessionId(resp.sessionId);
            setConversationHistory(generateInitialMessages(resp.sessionId));      
        })
    }, []);


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim() === '') return;

        const botReply: Message = {
            id: generateUUID(),
            sessionId: sessionId,
            sender: 'bot',
            content: "",
            timestamp: new Date(),
            action: null,
        }

        // add the user input into the FE/BE, and reset the input box
        setIsLoading(true);
        const userMsgId = generateUUID();
        appendOneMessage(query, userMsgId, 'user');
        setQuery('');

        try {
            // store user-query message in the DB
            await sendMessage({
                id: userMsgId,
                sessionId: sessionId,
                sender: 'user',
                content: query,
                timestamp: new Date(),
                action: null,
            });

            // validate the user's query
            const userQueryValidation = await verifyUserQuery(query);
            // If query is invalid → reply with fallback and persist
            if (!userQueryValidation.is_in_scope) {
                botReply.content = fallbackBotMessages["out_of_scope"];
                botReply.timestamp = new Date();
                appendOneMessage(botReply.content, botReply.id, 'bot');
                await sendMessage(botReply);
                return;
            }

            // send the user query to the mcp-server and get the bot response
            const botResponse = await invokeAi({ message: query, sessionId: sessionId });

            // validate the bot response
            const aiResponseValidation = await verifyAIResponse(query, botResponse.answer);
            if (!aiResponseValidation.is_appropriate || aiResponseValidation.hallucination) {
                botReply.content = fallbackBotMessages["answer_wrong"];
            } else if (!aiResponseValidation.is_in_scope) {
                botReply.content = fallbackBotMessages["out_of_scope"];
            } else {
                botReply.content = botResponse.answer;
            }
            botReply.timestamp = new Date();
            // append bot reply to the FE/BE
            appendOneMessage(botReply.content, botReply.id, 'bot');
            await sendMessage(botReply);
        } catch (error) {
            console.error("Error during message handling:", error);
            botReply.content = fallbackBotMessages["default"];
            botReply.timestamp = new Date();
            appendOneMessage(botReply.content, botReply.id, 'bot');
        } finally {
            setIsLoading(false);
        }
    }

    // helper func to append one message to the conversation history
    const appendOneMessage = (message: string, msg_id: string, sender: string) => {
        setConversationHistory(prevHistory => [
            ...prevHistory,
            {
                id: msg_id,
                sessionId: sessionId,
                sender: sender,
                content: message,
                timestamp: new Date(),
            } as Message,
        ]);
    }

    // Scroll to the bottom of the chat when new messages are added or loading state changes
    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [conversationHistory, isLoading]);


    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto p-4">

                {/* Normal chat between user and bot */}
                <div className={`w-full h-5/6 min-h-[30rem] min-w-[25rem] min-h-[20rem] items-center justify-center rounded-lg z-10 bg-transport}`}>

                    {/* chat area */}
                    <div className='h-full w-full overflow-y-auto flex flex-col gap-4 px-2 relative'>
                        {conversationHistory.map((chat, _index) => (
                            <div key={chat.id} className={`chat ${chat.sender !== 'user' ? 'chat-start' : 'chat-end'}`}>
                                
                                {/* avatar */}
                                <div className="chat-image avatar">
                                    <div className="w-10 h-10 rounded-full bg-zinc-100 flex text-[#337778] items-center justify-center">
                                        {chat.sender === 'user' && <p className='text-2xl font-sans font-normal'>?</p>}
                                        {chat.sender !== 'user' && <Bot size={30} color="#337778" />}
                                    </div>
                                </div>

                                {/* chat bubble */}
                                <div
                                    className={`chat-bubble max-w-[43rem] text-base font-semibold ${
                                        chat.sender === "bot"
                                        ? "bg-[#EFE8D4] text-[#337778] pb-8"
                                        : "bg-[#337778] text-[#EFE8D4]"
                                    }`}
                                    >
                                    <div className={`markdown-body ${
                                        chat.sender === "bot" ? "text-[#337778]" : "text-[#EFE8D4]"
                                        }`}>
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm, remarkBreaks]}
                                            components={{
                                                a: ({node, ...props}) => (
                                                <a
                                                    {...props}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="text-blue-600 underline hover:text-blue-800"
                                                />
                                                )
                                            }}
                                        >
                                            {chat.content}
                                        </ReactMarkdown>
                                    </div>
                                </div>                             
                            </div>
                        ))}
                        {/* When user's query is pending, show the loading indicator */}
                        {isLoading && (
                            <div className="flex items-center justify-start pl-10">
                                <span className="loading loading-ring loading-xl text-purple-700"></span>
                                <span className="ml-2 text-lg text-purple-700">Thinking...</span>
                            </div>
                        )}
                    </div>

                    {/* chat input box */}
                    <form onSubmit={handleSubmit} className={`w-full bg-[#939C62] h-[3.5rem] min-w-[25rem] mt-[5rem] p-2 flex flex-row items-center justify-center gap-2 rounded-md z-10 `}>

                        <input 
                            type="text" 
                            placeholder="Ask about our products..." 
                            className="input input-warning bg-transparent w-full h-full text-lg text-[#5A3E00] placeholder-black font-semibold rounded-l-md px-3"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && query.trim() !== '') {
                                    handleSubmit(e);
                                }
                            }}
                        />
                        <button type="submit" className="btn btn-ghost btn-square rounded-r-md hover:bg-[#E0D3B8]" disabled={query.trim() === ''}>
                            <SendIcon className="text-black" />
                        </button>
                    </form>

                    {/* Anchor to scroll to */}
                    <div ref={bottomRef} />
                </div>
            </div>
        </div>
    )
};