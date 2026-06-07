import type { ChatResponse } from "../types/chat";

const API_BASE_URL = "http://localhost:8000";

export async function askQuestion(query: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Gagal menghubungi server chatbot.");
  }

  return response.json();
}