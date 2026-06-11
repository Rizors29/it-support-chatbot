import KnowledgeBaseCard from "../knowledgebase/KnowledgeBaseCard";
import AdminPanel from "../admin/AdminPanel";
import type { AuthUser } from "../../types/chat";

interface SidebarProps {
	user: AuthUser;
	adminMessage: string;
	isUploading: boolean;
	isRebuilding: boolean;
	setSelectedFile: (f: File | null) => void;
	onUpload: () => Promise<void>;
	onRebuild: () => Promise<void>;
}

function Sidebar({
	user,
	adminMessage,
	isUploading,
	isRebuilding,
	setSelectedFile,
	onUpload,
	onRebuild,
}: SidebarProps) {
	const cards = [
		{ title: "Microsoft 365", description: "Registrasi MFA, portal Office, Authenticator" },
		{ title: "Printer", description: "Install driver C3371 dan pengaturan printer" },
		{ title: "Windows 11", description: "Instalasi Windows, BIOS, drive tidak muncul" },
	];

	return (
		<aside className="sticky top-0 hidden h-screen w-80 flex-col border-r border-slate-200 bg-white lg:flex">
			<div className="shrink-0 border-b border-slate-100 bg-white px-6 py-6">
				<div className="flex items-center gap-3">
					<div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100">
						<img
							src="/chatbot-icon.svg"
							alt="Chatbot Icon"
							className="h-8 w-8 object-contain"
						/>
					</div>

					<div>
						<h2 className="text-xl font-bold">Knowledge Base</h2>
						<p className="text-sm text-slate-500">IT Support RAG</p>
					</div>
				</div>
			</div>

			<div className="flex min-h-0 flex-1 flex-col">
				<div className="min-h-0 flex-1 overflow-y-auto p-6">
					{cards.map((c) => (
						<KnowledgeBaseCard
							key={c.title}
							title={c.title}
							description={c.description}
						/>
					))}
				</div>

				{user.role === "admin" && (
					<div className="shrink-0 border-t border-slate-200 bg-white p-6">
						<AdminPanel
							isUploading={isUploading}
							isRebuilding={isRebuilding}
							adminMessage={adminMessage}
							setSelectedFile={setSelectedFile}
							onUpload={onUpload}
							onRebuild={onRebuild}
						/>
					</div>
				)}
			</div>
		</aside>
	);
}

export default Sidebar;