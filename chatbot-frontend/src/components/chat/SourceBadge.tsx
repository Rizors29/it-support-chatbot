import { AiFillFilePdf } from "react-icons/ai";
import { BiFile, BiSolidFileTxt } from "react-icons/bi";
import { FaFileWord } from "react-icons/fa";
import { FiImage } from "react-icons/fi";

interface SourceBadgeProps {
	src: string;
}

function SourceBadge({ src }: SourceBadgeProps) {
	const lower = src.toLowerCase();
	const ext = lower.split('.').pop() || '';

	const getIcon = () => {
		if (ext === 'pdf') return <AiFillFilePdf className="h-4 w-4 text-red-600" />;
		if (ext === 'txt') return <BiSolidFileTxt className="h-4 w-4 text-slate-700" />;
		if (ext === 'doc' || ext === 'docx') return <FaFileWord className="h-4 w-4 text-blue-700" />;
		if (['png', 'jpg', 'jpeg', 'gif', 'svg'].includes(ext)) return <FiImage className="h-4 w-4 text-emerald-600" />;
		return <BiFile className="h-4 w-4 text-slate-500" />;
	};

	return (
		<button className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer">
			{getIcon()}
			<span className="truncate max-w-[18rem]">{src}</span>
		</button>
	);
};

export default SourceBadge;
