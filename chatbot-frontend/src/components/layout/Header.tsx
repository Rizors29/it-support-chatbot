import type { AuthUser } from "../../types/chat";
import { FaRegUser } from "react-icons/fa";

interface HeaderProps {
  user: AuthUser | null;
  onLogout: () => void;
  onLogin: () => void;
}

function Header({ user, onLogout, onLogin }: HeaderProps) {
	return (
		<header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5">
			<div>
				<h1 className="font-bold">
					<span className="block text-md sm:hidden">
						IT Support
						<br />
						Chatbot
					</span>

					<span className="hidden text-2xl sm:block">
						IT Support Chatbot
					</span>
				</h1>
				<p className="hidden text-sm text-slate-500 sm:flex">Berbasis RAG</p>
			</div>

			<div className="flex items-center gap-3">
				<div className="text-right">
					<p className="flex items-center gap-2 text-sm font-semibold text-slate-800 border-1 border-blue-300 bg-blue-100 px-4 py-2 rounded-full">
						<FaRegUser />
						{user ? user.name : "Guest"}
					</p>
				</div>

				<span className="hidden rounded-full border-1 border-green-300 bg-green-100 px-4 py-2 text-sm font-semibold text-green-700 sm:flex">
					Online
				</span>

				<button
					onClick={user ? onLogout : onLogin}
					className="cursor-pointer rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100"
				>
					{user ? "Logout" : "Login"}
				</button>
			</div>
		</header>
	);
}

export default Header;
