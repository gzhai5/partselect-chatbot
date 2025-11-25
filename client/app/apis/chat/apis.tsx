import { instance } from '../base/instance';
import { beginConversationRequest, Conversation, Message } from './interfaces';


export const sendMessage = async (body: Message): Promise<Message> => {
    const response = await instance.post('/message/send', body);
    return response.data as Message;
};

export const beginConversation = async (body: beginConversationRequest): Promise<Conversation> => {
    const response = await instance.post('/conversation/begin', body);
    return response.data as Conversation;
}

export const endConversation = async (sessionId: string): Promise<void> => {
    await instance.post(`/conversation/end?sessionId=${sessionId}`);
};