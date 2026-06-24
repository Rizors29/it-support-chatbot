function LoadingMessage() {
	return (
		<div className="flex items-center gap-3">
			<div className="flex gap-1">
				<div className="w-1 h-1 bg-slate-500 rounded-full animate-bounce-loading" style={{ animationDelay: '0s' }}></div>
				<div className="w-1 h-1 bg-slate-500 rounded-full animate-bounce-loading" style={{ animationDelay: '0.2s' }}></div>
				<div className="w-1 h-1 bg-slate-500 rounded-full animate-bounce-loading" style={{ animationDelay: '0.4s' }}></div>
			</div>
			<p className="text-sm text-slate-600">Sedang mencari jawaban dari knowledge base...</p>
		</div>
	);
}

export default LoadingMessage;
