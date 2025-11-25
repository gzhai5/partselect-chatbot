export interface AiInvokeRequest {
    message: string;
    sessionId: string;
}

export interface AiInvokeResponse {
    query: string;
    answer: string;
    token_usage: TokenUsage;
    total_price: number;
    response_time: string;
    tools_used: McpTool[];
}

interface McpTool {
    name: string;
    args: {
        query: string;
    };
    id: string;
    type: string;
}

interface TokenUsage {
    completion_tokens: number;
    prompt_tokens: number;
    total_tokens: number;
}

export interface McpToolsResponse {
    name: string;
    description: string;
}

export interface VerifyUserQueryResponse {
    is_in_scope: boolean;
    reason: string;
}

export interface VerifyAIResponseResponse {
    is_appropriate: boolean;
    is_in_scope: boolean;
    hallucination: boolean;
    reason: string;
}