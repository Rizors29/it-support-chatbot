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

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}

export interface LoginResponse {
  message: string;
  access_token: string;
  token_type: string;
  user: AuthUser;
}