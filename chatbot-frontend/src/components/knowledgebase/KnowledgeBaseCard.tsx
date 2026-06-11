interface KnowledgeBaseCardProps {
	title: string;
	description: string;
}

function KnowledgeBaseCard({ title, description }: KnowledgeBaseCardProps) {
	return (
		<div className="mb-4 rounded-2xl border border-slate-200 bg-slate-50 p-4">
			<h3 className="font-semibold text-blue-900">{title}</h3>
			<p className="mt-2 text-sm leading-6 text-slate-500">{description}</p>
		</div>
	);
};

export default KnowledgeBaseCard;
