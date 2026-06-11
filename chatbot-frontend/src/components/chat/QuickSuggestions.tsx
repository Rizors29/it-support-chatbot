interface Suggestion {
	text: string;
	icon?: React.ComponentType<{ className?: string }>;
}

interface QuickSuggestionsProps {
	suggestions: Suggestion[];
	onSelect: (text: string) => void;
}

function QuickSuggestions({ suggestions, onSelect }: QuickSuggestionsProps) {
	return (
		<div className="mb-4 flex flex-wrap gap-2 justify-center">
			{suggestions.map((item) => {
				const IconComponent = item.icon;
				return (
					<button
						key={item.text}
						onClick={() => onSelect(item.text)}
						className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-4 py-2 text-sm text-slate-700 font-semibold transition hover:bg-slate-100 cursor-pointer"
					>
						{IconComponent && <IconComponent className="h-4 w-4" />}
						{item.text}
					</button>
				);
			})}
		</div>
	    );
	};

export default QuickSuggestions;
