export interface ChatMessage {
  role: "user" | "bot";
  content: string;
  sources?: string[];
  category?: string;
  similarity_score?: number;
  is_fallback?: boolean;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
  category: string;
  similarity_score: number;
  is_fallback: boolean;
}