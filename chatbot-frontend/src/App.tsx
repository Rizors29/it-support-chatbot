import { useEffect, useState } from "react";
import { askQuestion, uploadKnowledgeBase } from "./services/api";
import ModelDropdown from "./components/chat/ModelDropdown";

import type { ChatMessage, ModelType } from "./types/chat";
import type { AuthUser } from "./types/chat";

import LoginModal from "./components/auth/LoginModal";
import KnowledgeBaseModal from "./components/auth/KnowledgeBaseModal";

import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import ChatWindow from "./components/chat/ChatWindow";
import QuickSuggestions from "./components/chat/QuickSuggestions";
import ChatInput from "./components/chat/ChatInput";

import { CgMicrosoft } from "react-icons/cg";
import { FiPrinter } from "react-icons/fi";
import { MdLaptopWindows } from "react-icons/md";
import { FaWifi } from "react-icons/fa";

const quickSuggestions = [
  { text: "Registrasi Microsoft 365", icon: CgMicrosoft },
  { text: "Install Printer C3371", icon: FiPrinter },
  { text: "Install Windows 11", icon: MdLaptopWindows },
  { text: "Wifi Bermasalah", icon: FaWifi },
];

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [adminMessage, setAdminMessage] = useState("");
  const [selectedModel, setSelectedModel] = useState<ModelType>("llama");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedFolder, setSelectedFolder] = useState("");

  const [isUploading, setIsUploading] = useState(false);
  const [refreshKb, setRefreshKb] = useState(0);
  const token = localStorage.getItem("token") || "";

  const [showLogin, setShowLogin] = useState(false);
  const [showKnowledgeBase, setShowKnowledgeBase] = useState(false);

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

  const handleUploadKnowledgeBase = async () => {
    if (!selectedFile) {
      setAdminMessage("Pilih file terlebih dahulu.");
      return;
    }

    setIsUploading(true);
    setAdminMessage("");

    try {
      const response = await uploadKnowledgeBase(selectedFile, selectedFolder);
      setAdminMessage(
        `${response.message} File: ${response.filename}. Total chunk: ${response.indexed_chunks}`
      );
      setSelectedFile(null);
      setRefreshKb((prev) => prev + 1);
    } catch {
      setAdminMessage("Gagal upload dokumen. Gunakan file PDF, TXT, atau DOCX.");
    } finally {
      setIsUploading(false);
    }
  };

  const sendMessage = async (queryText?: string) => {
    const query = (queryText ?? input).trim();
    if (!query || isLoading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await askQuestion(query, selectedModel);

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
        isUploading={isUploading}
        setSelectedFile={setSelectedFile}
        onUpload={handleUploadKnowledgeBase}
        onOpenKnowledgeBase={() => setShowKnowledgeBase(true)}
        selectedFolder={selectedFolder}
        setSelectedFolder={setSelectedFolder}
      />

      <main className="flex flex-1 flex-col min-w-0">
        <Header
          user={user}
          onLogout={handleLogout}
          onLogin={() => setShowLogin(true)}
        />

        <section className="flex-1 overflow-y-auto px-6 py-6">
          <ChatWindow messages={messages} isLoading={isLoading} />
        </section>


        <div className="sticky bottom-0 z-10 border-t border-slate-200 bg-white px-6 py-4">
          <div className="mb-4 flex items-center gap-3">
            <ModelDropdown />

            <div className="hidden flex-1 justify-center lg:flex">
              <QuickSuggestions
                suggestions={quickSuggestions}
                onSelect={sendMessage}
              />
            </div>
          </div>

          <ChatInput
            input={input}
            setInput={setInput}
            onSend={() => sendMessage()}
            isLoading={isLoading}
          />
        </div>
        {showLogin && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <div className="w-full max-w-md px-4">
              <LoginModal
                onLogin={(loggedInUser) => {
                  handleLogin(loggedInUser);
                  setShowLogin(false);
                }}
                onClose={() => setShowLogin(false)}
              />
            </div>
          </div>
        )}
        {showKnowledgeBase && user?.role === "admin" && (
          <KnowledgeBaseModal
            token={token}
            refreshTrigger={refreshKb}
            onClose={() => setShowKnowledgeBase(false)}
          />
        )}
      </main>
    </div>
  );
}

export default App;