interface AdminPanelProps {
	isUploading: boolean;
	isRebuilding: boolean;
	adminMessage: string;
	setSelectedFile: (f: File | null) => void;
	onUpload: () => Promise<void>;
	onRebuild: () => Promise<void>;
}

function AdminPanel({ isUploading, isRebuilding, adminMessage, setSelectedFile, onUpload, onRebuild }: AdminPanelProps) {
	return (
		<div className="rounded-2xl border border-blue-200 bg-blue-50 p-4">
			<h3 className="font-semibold text-blue-900">Admin Panel</h3>
			<label className="mt-4 block text-sm text-blue-900">Upload Knowledge Base</label>

			<input
				type="file"
				accept=".pdf,.txt,.docx"
				onChange={(event) => {
					const file = event.target.files?.[0] || null;
					setSelectedFile(file);
				}}
				className="mt-2 w-full rounded-xl border border-blue-200 bg-white px-3 py-2 text-sm text-slate-700"
			/>

			<button
				onClick={onUpload}
				disabled={isUploading}
				className="mt-3 w-full rounded-xl bg-blue-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-950 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
			>
				{isUploading ? "Uploading..." : "Upload & Rebuild Index"}
			</button>

			<button
				onClick={onRebuild}
				disabled={isRebuilding}
				className="mt-3 w-full rounded-xl border border-blue-300 bg-white px-4 py-2 text-sm font-semibold text-blue-900 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
			>
				{isRebuilding ? "Rebuild Index..." : "Rebuild Index Manual"}
			</button>

			{adminMessage && (
				<p className="mt-3 rounded-xl bg-white px-3 py-2 text-sm text-blue-800">{adminMessage}</p>
			)}
		</div>
	);
};

export default AdminPanel;
