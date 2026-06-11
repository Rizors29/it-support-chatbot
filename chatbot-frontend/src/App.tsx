import { useEffect, useState } from "react";
import { askQuestion, rebuildIndex, uploadKnowledgeBase } from "./services/api";
import type { ChatMessage } from "./types/chat";
import Login from "./pages/Login";
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import ChatWindow from "./components/chat/ChatWindow";
import QuickSuggestions from "./components/chat/QuickSuggestions";
import ChatInput from "./components/chat/ChatInput";
import { CgMicrosoft } from "react-icons/cg";
import { FiPrinter } from "react-icons/fi";
import { MdLaptopWindows } from "react-icons/md";
import { ImOnedrive } from "react-icons/im";
import type { AuthUser } from "./types/chat";

const quickSuggestions = [
  { text: "Registrasi Microsoft 365", icon: CgMicrosoft },
  { text: "Install printer C3371", icon: FiPrinter },
  { text: "Install Windows 11", icon: MdLaptopWindows },
  { text: "Drive tidak muncul saat install Windows", icon: ImOnedrive },
];

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isRebuilding, setIsRebuilding] = useState(false);
  const [adminMessage, setAdminMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem("user");

    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (loggedInUser: AuthUser) => {
    setUser(loggedInUser);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    setMessages([]);
  };

  const handleRebuildIndex = async () => {
    setIsRebuilding(true);
    setAdminMessage("");

    try {
      const response = await rebuildIndex();
      setAdminMessage(
        `${response.message} Total chunk: ${response.indexed_chunks}`
      );
    } catch {
      setAdminMessage("Gagal rebuild index. Pastikan akun memiliki role admin.");
    } finally {
      setIsRebuilding(false);
    }
  };

  const handleUploadKnowledgeBase = async () => {
    if (!selectedFile) {
      setAdminMessage("Pilih file terlebih dahulu.");
      return;
    }

    setIsUploading(true);
    setAdminMessage("");

    try {
      const response = await uploadKnowledgeBase(selectedFile);
      setAdminMessage(
        `${response.message} File: ${response.filename}. Total chunk: ${response.indexed_chunks}`
      );
      setSelectedFile(null);
    } catch {
      setAdminMessage("Gagal upload dokumen. Gunakan file PDF, TXT, atau DOCX.");
    } finally {
      setIsUploading(false);
    }
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  const sendMessage = async (queryText?: string) => {
    const query = (queryText ?? input).trim();
    if (!query || isLoading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await askQuestion(query);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: response.answer,
          sources: response.sources,
          category: response.category,
          similarity_score: response.similarity_score,
          is_fallback: response.is_fallback,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: "Maaf, terjadi kesalahan saat menghubungi server chatbot.",
          category: "Error",
          is_fallback: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-100 text-slate-800">
      <Sidebar
        user={user}
        adminMessage={adminMessage}
        isUploading={isUploading}
        isRebuilding={isRebuilding}
        setSelectedFile={setSelectedFile}
        onUpload={handleUploadKnowledgeBase}
        onRebuild={handleRebuildIndex}
      />

      <main className="flex flex-1 flex-col">
        <Header user={user} onLogout={handleLogout} />

        <section className="flex-1 overflow-y-auto px-6 py-6">
          <ChatWindow messages={messages} isLoading={isLoading} />
        </section>

        <div className="sticky bottom-0 z-10 border-t border-slate-200 bg-white px-6 py-4">
          <QuickSuggestions suggestions={quickSuggestions} onSelect={sendMessage} />

          <ChatInput
            input={input}
            setInput={setInput}
            onSend={() => sendMessage()}
            isLoading={isLoading}
          />
        </div>
      </main>
    </div>
  );
}

export default App;