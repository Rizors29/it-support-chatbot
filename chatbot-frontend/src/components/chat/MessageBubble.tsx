import ReactMarkdown from "react-markdown";
import { MdContentCopy } from "react-icons/md";
import type { ChatMessage } from "../../types/chat";
import SourceBadge from "./SourceBadge";

interface MessageBubbleProps {
  message: ChatMessage;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const copyText = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
    } catch (error) {
      console.error("Gagal menyalin teks:", error);
    }
  };

  return (
    <div
      className={`group flex flex-col ${message.role === "user" ? "items-end" : "items-start"
        }`}
    >
      <div
        className={`max-w-3xl rounded-2xl px-5 py-4 border-1 border-slate-200 ${message.role === "user"
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
              <span className="font-semibold">
                Score: {message.similarity_score.toFixed(4)}
              </span>
            )}

            {message.sources && message.sources.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {message.sources.map((src, i) => (
                  <SourceBadge key={i} src={src} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <button
        onClick={copyText}
        type="button"
        className="
				mt-2
				inline-flex
				items-center
				rounded-full
				p-2
				text-slate-700
				opacity-0
				transition-all
				duration-200
				group-hover:opacity-100
				hover:bg-slate-200
				focus:outline-none
				focus:ring-2
				focus:ring-slate-300
        cursor-pointer
			"
        title="Copy"
      >
        <MdContentCopy className="h-5 w-5" />
      </button>
    </div>
  );
};

export default MessageBubble;
