import { useState } from "react";
import { askQuestion } from "./services/api";
import type { ChatMessage } from "./types/chat";
import ReactMarkdown from "react-markdown";
import { RiSendPlaneFill } from "react-icons/ri";
import { AiFillFilePdf } from "react-icons/ai";
import { BiFile, BiSolidFileTxt } from "react-icons/bi";
import { FaFileWord } from "react-icons/fa";
import { CgMicrosoft } from "react-icons/cg";
import { FiImage, FiPrinter } from "react-icons/fi";
import { MdLaptopWindows } from "react-icons/md";
import { ImOnedrive } from "react-icons/im";

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
      <aside className="hidden w-80 border-r border-slate-200 bg-white p-6 lg:block">
        <div className="mb-8 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100">
            <img src="/chatbot-icon.svg" alt="Chatbot Icon" className="h-8 w-8 object-contain" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Knowledge Base</h2>
            <p className="text-sm text-slate-500">IT Support RAG</p>
          </div>
        </div>

        {[
          ["Microsoft 365", "Registrasi MFA, portal Office, Authenticator"],
          ["Printer", "Install driver C3371 dan pengaturan printer"],
          ["Windows 11", "Instalasi Windows, BIOS, drive tidak muncul"],
        ].map(([title, desc]) => (
          <div key={title} className="mb-4 rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <h3 className="font-semibold text-blue-900">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-500">{desc}</p>
          </div>
        ))}
      </aside>

      <main className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold">IT Support Chatbot</h1>
            <p className="text-sm text-slate-500">Berbasis RAG + Gemini API</p>
          </div>
          <span className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
            Online
          </span>
        </header>

        <section className="flex-1 overflow-y-auto px-6 py-6">
          {messages.length === 0 && (
            <div className="mt-28 text-center">
              <h2 className="text-2xl font-bold text-slate-800">Halo, ada kendala IT apa?</h2>
              <p className="mt-2 text-slate-500">Pilih pertanyaan cepat atau ketik masalah Anda.</p>
            </div>
          )}

          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-3xl rounded-2xl px-5 py-4 shadow-sm ${message.role === "user"
                      ? "rounded-br-md bg-blue-900 text-white"
                      : "rounded-bl-md bg-white text-slate-800"
                    }`}
                >
                  <div
                    className={`prose max-w-none leading-7 ${message.role === "user"
                        ? "prose-invert prose-p:text-white"
                        : "prose-slate"
                      }`}
                  >
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>

                  {message.role === "bot" && (
                    <div className="mt-4 border-t border-slate-200 pt-3 text-sm text-slate-500">
                      {message.category && (
                        <span className="mr-2 inline-block rounded-full bg-blue-100 px-3 py-1 font-semibold text-blue-700">
                          {message.category}
                        </span>
                      )}

                      {typeof message.similarity_score === "number" && (
                        <span className="font-semibold">Score: {message.similarity_score.toFixed(4)}</span>
                      )}

                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-2">
                          {message.sources.map((src, i) => {
                            const lower = src.toLowerCase();
                            const ext = lower.split('.').pop() || '';

                            const getIcon = () => {
                              if (ext === 'pdf') return <AiFillFilePdf className="h-4 w-4 text-red-600" />;
                              if (ext === 'txt') return <BiSolidFileTxt className="h-4 w-4 text-slate-700" />;
                              if (ext === 'doc' || ext === 'docx') return <FaFileWord className="h-4 w-4 text-blue-700" />;
                              if (['png','jpg','jpeg','gif','svg'].includes(ext)) return <FiImage className="h-4 w-4 text-emerald-600" />;
                              return <BiFile className="h-4 w-4 text-slate-500" />;
                            };

                            return (
                              <button
                                key={i}
                                className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer"
                              >
                                {getIcon()}
                                <span className="truncate max-w-[18rem]">{src}</span>
                              </button>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="rounded-2xl rounded-bl-md bg-white px-5 py-4 shadow-sm">
                  Sedang mencari jawaban dari knowledge base...
                </div>
              </div>
            )}
          </div>
        </section>

        <div className="border-t border-slate-200 bg-white px-6 py-4">
          <div className="mb-4 flex flex-wrap gap-2">
            {quickSuggestions.map((item) => {
              const IconComponent = item.icon;
              return (
                <button
                  key={item.text}
                  onClick={() => sendMessage(item.text)}
                  className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-4 py-2 text-sm text-slate-700 font-semibold transition hover:bg-slate-100 cursor-pointer"
                >
                  <IconComponent className="h-4 w-4" />
                  {item.text}
                </button>
              );
            })}
          </div>

          <div className="flex gap-3">
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") sendMessage();
              }}
              placeholder="Tuliskan masalah IT Anda..."
              className="flex-1 rounded-full border border-slate-300 px-5 py-3 outline-none focus:border-blue-400"
            />
            <button
              onClick={() => sendMessage()}
              disabled={isLoading}
              className="rounded-full bg-blue-900 px-6 py-3 font-semibold text-white transition hover:bg-blue-950 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
              aria-label="Kirim"
            >
              <RiSendPlaneFill className="h-5 w-5" />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;