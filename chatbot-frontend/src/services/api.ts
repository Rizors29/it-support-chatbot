import type { ChatResponse, LoginRequest, LoginResponse } from "../types/chat";

const API_BASE_URL = "http://localhost:8000";

export async function askQuestion(query: string, model: string): Promise<ChatResponse> {
  const token = localStorage.getItem("token");

  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ query, model }),
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

export async function uploadKnowledgeBase(
  file: File,
  folderName: string
) {
  const token = localStorage.getItem("token");

  const formData = new FormData();

  formData.append("folder_name", folderName);
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/admin/upload-document`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.text();
    console.error(error);

    throw new Error("Gagal upload knowledge base.");
  }

  return response.json();
}

export async function getDocuments(token: string) {
  const response = await fetch(
    `${API_BASE_URL}/admin/documents`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Gagal mengambil daftar dokumen.");
  }

  return response.json();
}

export async function deleteDocument(
  folderName: string,
  filename: string
) {
  const token = localStorage.getItem("token");

  const response = await fetch(
    `${API_BASE_URL}/admin/documents/${encodeURIComponent(
      folderName
    )}/${encodeURIComponent(filename)}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Gagal menghapus dokumen.");
  }

  return response.json();
}