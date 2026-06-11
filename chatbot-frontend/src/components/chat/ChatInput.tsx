import { RiSendPlaneFill } from "react-icons/ri";

interface ChatInputProps {
	input: string;
	setInput: (s: string) => void;
	onSend: () => void;
	isLoading: boolean;
}

function ChatInput({ input, setInput, onSend, isLoading }: ChatInputProps) {
	const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
		setInput(event.target.value);
		event.target.style.height = "52px";
		event.target.style.height = `${event.target.scrollHeight}px`;
	};

	return (
		<div className="flex items-end gap-3">
			<textarea
				value={input}
				onChange={handleInput}
				onKeyDown={(event) => {
					if (event.key === "Enter" && !event.shiftKey) {
						event.preventDefault();
						onSend();
					}
				}}
				placeholder="Tuliskan masalah IT Anda..."
				className="flex-1 h-[52px] max-h-[200px] resize-none rounded-3xl border border-slate-300 px-5 py-3 outline-none placeholder:font-medium focus:border-blue-400 overflow-y-auto"
			/>
			<button
				onClick={onSend}
				disabled={isLoading}
				className="self-end h-[52px] rounded-full bg-blue-900 px-6 py-3 font-semibold text-white transition hover:bg-blue-950 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
				aria-label="Kirim"
			>
				<RiSendPlaneFill className="h-5 w-5" />
			</button>
		</div>
	);
};

export default ChatInput;
