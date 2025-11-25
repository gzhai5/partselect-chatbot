/* eslint-disable @typescript-eslint/no-explicit-any */
export interface Message {
    id: string;
    sessionId: string;
    sender: 'user' | 'bot' | 'system';
    content: string;
    timestamp: Date;
    action: any;
};

export interface beginConversationRequest {
    startTime: Date;
    userId: string;
}

export interface Conversation {
    sessionId: string;
    startTime: Date;
    endTime: Date;
    userId: string;
    messages: Message[];
}

