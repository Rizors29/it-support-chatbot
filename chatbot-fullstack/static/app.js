const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");
const queryInput = document.getElementById("query");
const providerSelect = document.getElementById("provider");
const sendButton = document.getElementById("sendButton");
const clearChat = document.getElementById("clearChat");
const healthText = document.getElementById("healthText");
const healthDot = document.getElementById("healthDot");
const uploadForm = document.getElementById("uploadForm");
const uploadFile = document.getElementById("uploadFile");
const folderName = document.getElementById("folderName");
const uploadButton = document.getElementById("uploadButton");
const uploadStatus = document.getElementById("uploadStatus");
const folderList = document.getElementById("folderList");
const docList = document.getElementById("docList");
const folderSuggestions = document.getElementById("folderSuggestions");
const refreshDocs = document.getElementById("refreshDocs");

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderMarkdown(text) {
  const escaped = escapeHtml(text);
  return escaped
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
}

function appendMessage(role, text, meta = null) {
  const message = document.createElement("div");
  message.className = `message ${role}`;

  if (role === "bot") {
    message.innerHTML = renderMarkdown(text);
  } else {
    message.textContent = text;
  }

  if (meta) {
    const badgeRow = document.createElement("div");
    badgeRow.className = "meta-badges";

    meta.forEach((item) => {
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = item;
      badgeRow.appendChild(badge);
    });

    message.appendChild(badgeRow);
  }

  chatWindow.appendChild(message);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return message;
}

function appendMetaLine(text) {
  const meta = document.createElement("div");
  meta.className = "message meta";
  meta.textContent = text;
  chatWindow.appendChild(meta);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    healthText.textContent = `Index siap, ${data.indexed_chunks} chunk terindeks`;
    healthDot.classList.add("ok");
  } catch (error) {
    healthText.textContent = "Status indeks belum tersedia";
  }
}

async function refreshKnowledgeBase() {
  try {
    const response = await fetch("/api/documents");
    const data = await response.json();

    folderList.innerHTML = "";
    docList.innerHTML = "";
    folderSuggestions.innerHTML = "";

    if (!data.folders || data.folders.length === 0) {
      folderList.innerHTML = '<span class="pill">Belum ada folder</span>';
      docList.innerHTML = '<div class="doc-card">Belum ada dokumen di knowledge base.</div>';
      return;
    }

    data.folders.forEach((folder) => {
      const pill = document.createElement("span");
      pill.className = "pill";
      pill.textContent = folder.folder_name;
      folderList.appendChild(pill);

      const option = document.createElement("option");
      option.value = folder.folder_name;
      folderSuggestions.appendChild(option);

      const card = document.createElement("div");
      card.className = "doc-card";

      const header = document.createElement("div");
      header.className = "doc-card-header";
      header.innerHTML = `<span>${escapeHtml(folder.folder_name)}</span><span>${folder.files.length} file</span>`;

      const meta = document.createElement("div");
      meta.className = "doc-card-meta";
      meta.textContent =
        folder.files.length > 0
          ? folder.files
              .map((file) => `${file.filename} (${file.size_kb} KB)`)
              .join(" · ")
          : "Folder ini masih kosong.";

      card.appendChild(header);
      card.appendChild(meta);
      docList.appendChild(card);
    });
  } catch (error) {
    folderList.innerHTML = '<span class="pill">Gagal memuat folder</span>';
    docList.innerHTML = '<div class="doc-card">Gagal memuat daftar dokumen.</div>';
  }
}

async function sendQuery(query) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      model: providerSelect.value,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Request gagal");
  }

  return response.json();
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = queryInput.value.trim();
  if (!query) {
    return;
  }

  appendMessage("user", query);
  queryInput.value = "";
  queryInput.focus();

  const loading = appendMessage("bot", "Memproses jawaban...");
  sendButton.disabled = true;

  try {
    const data = await sendQuery(query);
    loading.remove();

    const badges = [
      `Kategori: ${data.category}`,
      `Skor: ${data.similarity_score.toFixed(2)}`,
      data.is_fallback ? "Fallback aktif" : "RAG aktif",
    ];

    appendMessage("bot", data.answer, badges);

    if (data.sources && data.sources.length > 0) {
      appendMetaLine(`Sumber: ${data.sources.join(", ")}`);
    }
  } catch (error) {
    loading.remove();
    appendMessage("bot", `Terjadi error: ${error.message}`);
  } finally {
    sendButton.disabled = false;
  }
});

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = uploadFile.files[0];
  const folder = folderName.value.trim();

  if (!folder) {
    uploadStatus.textContent = "Isi nama folder knowledge base terlebih dahulu.";
    return;
  }

  if (!file) {
    uploadStatus.textContent = "Pilih file PDF, TXT, atau DOCX.";
    return;
  }

  const formData = new FormData();
  formData.append("folder_name", folder);
  formData.append("file", file);

  uploadButton.disabled = true;
  uploadStatus.textContent = "Mengupload dan membangun ulang index...";

  try {
    const response = await fetch("/api/upload-document", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || payload.message || "Upload gagal");
    }

    uploadStatus.textContent = `${payload.filename} berhasil diupload ke ${payload.folder}.`;
    uploadFile.value = "";
    await refreshKnowledgeBase();
    await checkHealth();
  } catch (error) {
    uploadStatus.textContent = `Upload gagal: ${error.message}`;
  } finally {
    uploadButton.disabled = false;
  }
});

document.querySelectorAll("[data-suggest]").forEach((button) => {
  button.addEventListener("click", () => {
    queryInput.value = button.dataset.suggest;
    queryInput.focus();
  });
});

clearChat.addEventListener("click", () => {
  chatWindow.innerHTML = "";
  appendMessage(
    "bot",
    "Tanya masalah IT Anda di sini. Contoh: 'VPN sering putus saat WFH' atau 'Printer tidak terdeteksi di laptop Windows'."
  );
});

refreshDocs.addEventListener("click", async () => {
  refreshDocs.disabled = true;
  await refreshKnowledgeBase();
  await checkHealth();
  refreshDocs.disabled = false;
});

appendMessage(
  "bot",
  "Tanya masalah IT Anda di sini. Contoh: 'VPN sering putus saat WFH' atau 'Printer tidak terdeteksi di laptop Windows'."
);
refreshKnowledgeBase();
checkHealth();

