import type { ChatResponse, LoginRequest, LoginResponse } from "../types/chat";

const API_BASE_URL = "http://localhost:8000";

export async function askQuestion(query: string): Promise<ChatResponse> {
  const token = localStorage.getItem("token");

  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Gagal menghubungi server chatbot.");
  }

  return response.json();
}

export async function loginUser(data: LoginRequest): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Email atau password salah.");
  }

  return response.json();
}

export async function rebuildIndex() {
  const token = localStorage.getItem("token");

  const response = await fetch(`${API_BASE_URL}/admin/rebuild-index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Gagal rebuild index.");
  }

  return response.json();
}

export async function uploadKnowledgeBase(file: File) {
  const token = localStorage.getItem("token");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/admin/upload-document`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Gagal upload knowledge base.");
  }

  return response.json();
}