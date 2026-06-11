import type { AuthUser } from "../../types/chat";

interface HeaderProps {
	user: AuthUser;
	onLogout: () => void;
}

function Header({ user, onLogout }: HeaderProps) {
	return (
		<header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5">
			<div>
				<h1 className="text-2xl font-bold">IT Support Chatbot</h1>
				<p className="text-sm text-slate-500">Berbasis RAG</p>
			</div>

			<div className="flex items-center gap-3">
				<div className="text-right">
					<p className="text-sm font-semibold text-slate-800">
						{user.name}
					</p>
					<p className="text-xs capitalize text-slate-500">
						{user.role}
					</p>
				</div>

				<span className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
					Online
				</span>

				<button
					onClick={onLogout}
					className="cursor-pointer rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100"
				>
					Logout
				</button>
			</div>
		</header>
	);
}

export default Header;
