import { Message } from '@/app/apis/chat/interfaces';


// Description: Utility function to generate a UUID.
export function generateUUID(): string {
    const hexChars = '0123456789abcdef';
    let result = '';
    for (let i = 0; i < 24; i++) {
    result += hexChars[Math.floor(Math.random() * 16)];
    }
    return result;
}

export const generateInitialMessages = (sessionId: string): Message[] => [
    {
        id: generateUUID(),
        sessionId: sessionId,
        sender: 'system',
        content: "👋 Hello! I'm your PartSelect assistant. How can I help you today?",
        timestamp: new Date(),
        action: null,
    }
];

export const fallbackBotMessages: Record<string, string> = {
    "default": "I'm sorry, but I can't assist with that request. Please ask me about PartSelect products or services.",
    "out_of_scope": "I'm sorry, but I can't assist with that request. Please ask me about PartSelect products or services, and I am only able to help you with the dishwasher and refrigerator part categories for now.",
    "answer_wrong": "I'm sorry, could you please clarify your question or provide more details? I'll do my best to assist you with PartSelect products or services.",
}