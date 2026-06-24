interface AdminPanelProps {
  onOpenKnowledgeBase: () => void;
}

function AdminPanel({
  onOpenKnowledgeBase,
}: AdminPanelProps) {
  return (
    <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4">
      <h3 className="font-semibold text-blue-900 text-center">
        Welcome, Admin!
      </h3>

      <button
        onClick={onOpenKnowledgeBase}
        className="mt-4 w-full rounded-xl border border-green-300 bg-white px-4 py-2 text-sm font-semibold text-green-700 hover:bg-green-50 cursor-pointer"
      >
        Manage Knowledge Base
      </button>
    </div>
  );
}

export default AdminPanel;
