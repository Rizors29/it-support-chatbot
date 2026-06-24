import { useRef } from "react";
import { RiSendPlaneFill } from "react-icons/ri";

interface ChatInputProps {
	input: string;
	setInput: (s: string) => void;
	onSend: () => void;
	isLoading: boolean;
}

function ChatInput({ input, setInput, onSend, isLoading }: ChatInputProps) {
	const textareaRef = useRef<HTMLTextAreaElement>(null);

	const resetTextareaHeight = () => {
		if (textareaRef.current) {
			textareaRef.current.style.height = "52px";
		}
	};

	const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
		setInput(event.target.value);
		event.target.style.height = "52px";
		event.target.style.height = `${event.target.scrollHeight}px`;
	};

	const handleSend = () => {
		resetTextareaHeight();
		onSend();
	};

	return (
		<div className="relative">
			<textarea
				ref={textareaRef}
				value={input}
				onChange={handleInput}
				onKeyDown={(event) => {
					if (event.key === "Enter" && !event.shiftKey) {
						event.preventDefault();
						handleSend();
					}
				}}
				placeholder="Tuliskan masalah IT Anda..."
				className="w-full h-[52px] md:max-h-[200px] resize-none rounded-3xl border border-slate-300 px-5 py-3 pr-16 outline-none placeholder:font-medium focus:border-blue-400 overflow-y-auto"
			/>
			<button
				onClick={handleSend}
				disabled={isLoading}
				className="absolute right-2 bottom-3 h-[40px] w-[40px] rounded-full bg-blue-900 flex items-center justify-center font-semibold text-white transition hover:bg-blue-950 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
				aria-label="Kirim"
			>
				<RiSendPlaneFill className="h-5 w-5" />
			</button>
		</div>
	);
}

export default ChatInput;
