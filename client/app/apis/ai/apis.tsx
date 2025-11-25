import { instance } from "../base/instance";
import { mcpInstance } from "../base/mcp.instance";
import { AiInvokeRequest, AiInvokeResponse, McpToolsResponse, VerifyAIResponseResponse, VerifyUserQueryResponse } from "./interfaces";

export const invokeAi = async (body: AiInvokeRequest): Promise<AiInvokeResponse> => {
    const response = await mcpInstance.post('/query', body);
    return response.data as AiInvokeResponse;
}

export const getAllMcpTools = async (): Promise<McpToolsResponse[]> => {
    const response = await mcpInstance.get('/tools');
    return response.data as McpToolsResponse[];
}

export const verifyUserQuery = async (query: string): Promise<VerifyUserQueryResponse> => {
    const response = await instance.post('/ai/verify-user-query', { query });
    return response.data as VerifyUserQueryResponse;
}

export const verifyAIResponse = async (query: string, responseText: string): Promise<VerifyAIResponseResponse> => {
    const response = await instance.post('/ai/verify-ai-response', { query, response: responseText });
    return response.data as VerifyAIResponseResponse;
}