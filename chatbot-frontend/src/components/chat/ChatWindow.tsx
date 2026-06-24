import type { ChatMessage } from "../../types/chat";
import MessageBubble from "./MessageBubble";
import LoadingMessage from "./LoadingMessage";

interface ChatWindowProps {
	messages: ChatMessage[];
	isLoading: boolean;
}

function ChatWindow({ messages, isLoading }: ChatWindowProps) {
	return (
		<div>
			{messages.length === 0 && (
				<div className="mt-28 text-center">
					<h2 className="text-2xl font-bold text-slate-800">Halo, ada kendala IT apa?</h2>
					<p className="mt-2 text-slate-500">Pilih pertanyaan cepat atau ketik masalah Anda.</p>
				</div>
			)}

			<div className="space-y-1">
				{messages.map((m, i) => (
					<MessageBubble key={i} message={m} />
				))}

				{isLoading && (
					<div className="flex justify-start">
						<div className="rounded-2xl rounded-bl-md bg-white px-5 py-4 border-1 border-slate-200">
							<LoadingMessage />
						</div>
					</div>
				)}
			</div>
		</div>
	);
};

export default ChatWindow;
