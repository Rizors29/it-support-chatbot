import { useEffect, useState } from "react";
import { AiOutlineClose } from "react-icons/ai";
import {
  FiFolder,
  FiFileText,
  FiChevronDown,
  FiChevronRight,
} from "react-icons/fi";

import type { KnowledgeFolder } from "../../types/chat";

import {
  deleteDocument,
  getDocuments,
  uploadKnowledgeBase,
} from "../../services/api";

interface KnowledgeBaseModalProps {
  token: string;
  refreshTrigger: number;
  onClose: () => void;
}

function KnowledgeBaseModal({
  token,
  refreshTrigger,
  onClose,
}: KnowledgeBaseModalProps) {
  const [folders, setFolders] = useState<KnowledgeFolder[]>([]);
  const [expandedFolders, setExpandedFolders] = useState<string[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(false);

  const [selectedFiles, setSelectedFiles] = useState<
    Record<string, File | null>
  >({});
  const [deletingFile, setDeletingFile] = useState<string | null>(null);
  const [uploadingFile, setUploadingFile] = useState<string | null>(null);

  const loadDocuments = async () => {
    try {
      setLoadingDocs(true);

      const result = await getDocuments(token);

      setFolders(result.folders || []);
    } catch (error) {
      console.error("Gagal memuat knowledge base:", error);
    } finally {
      setLoadingDocs(false);
    }
  };

  const handleToggleFolder = (folderName: string) => {
    setExpandedFolders((current) =>
      current.includes(folderName)
        ? current.filter((name) => name !== folderName)
        : [...current, folderName]
    );
  };

  const handleUpload = async (
    folderName: string
  ) => {
    const file = selectedFiles[folderName];

    if (!file) {
      alert("Pilih file terlebih dahulu.");
      return;
    }

    try {
      setUploadingFile(folderName);

      await uploadKnowledgeBase(
        file,
        folderName
      );

      await loadDocuments();

      alert(
        `Dokumen berhasil diupload ke folder ${folderName}.`
      );

      setSelectedFiles((prev) => ({
        ...prev,
        [folderName]: null,
      }));
    } catch (error) {
      console.error(error);

      alert("Upload dokumen gagal.");
    } finally {
      setUploadingFile(null);
    }
  };

  const handleDelete = async (
    folderName: string,
    filename: string
  ) => {
    const confirmed = window.confirm(
      `Yakin ingin menghapus "${filename}"?`
    );

    if (!confirmed) return;

    const deleteKey = `${folderName}-${filename}`;

    try {
      setDeletingFile(deleteKey);

      await deleteDocument(
        folderName,
        filename
      );

      await loadDocuments();

      alert(
        "Dokumen berhasil dihapus dan index berhasil diperbarui."
      );
    } catch (error) {
      console.error(error);

      alert("Gagal menghapus dokumen.");
    } finally {
      setDeletingFile(null);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, [token, refreshTrigger]);

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/40 p-4">
      <div className="relative w-full max-w-4xl rounded-2xl bg-white p-6 shadow-xl">

        <button
          type="button"
          onClick={onClose}
          aria-label="Tutup knowledge base"
          className="absolute right-4 top-4 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 cursor-pointer"
        >
          <AiOutlineClose className="h-5 w-5" />
        </button>

        <h3 className="mb-6 text-xl font-bold text-slate-800">
          Knowledge Base Management
        </h3>

        <div className="max-h-[600px] overflow-y-auto">
          {loadingDocs ? (
            <p>Memuat dokumen...</p>
          ) : folders.length === 0 ? (
            <p>Tidak ada folder knowledge base.</p>
          ) : (
            <div className="space-y-5">
              {folders.map((folder) => {
                const isExpanded =
                  expandedFolders.includes(
                    folder.folder_name
                  );

                return (
                  <div
                    key={folder.folder_name}
                    className="mb-4 rounded-xl border border-slate-200 p-2"
                  >
                    <button
                      type="button"
                      onClick={() =>
                        handleToggleFolder(
                          folder.folder_name
                        )
                      }
                      className="flex w-full items-center gap-2 rounded-xl bg-slate-100 px-4 py-3 text-left hover:bg-slate-200 cursor-pointer"
                    >
                      {isExpanded ? (
                        <FiChevronDown className="text-slate-500" />
                      ) : (
                        <FiChevronRight className="text-slate-500" />
                      )}

                      <FiFolder className="text-amber-500" />

                      <span className="font-semibold text-slate-800">
                        {folder.folder_name}
                      </span>

                      <span className="text-sm text-slate-500">
                        ({folder.files.length} file)
                      </span>
                    </button>

                    {isExpanded && (
                      <div className="mt-4">

                        {/* Upload Area - single row */}
                        <div className="mb-4 rounded-xl border border-dashed border-slate-300 p-4">
                          <div className="flex items-center justify-between gap-3">
                            <input
                              type="file"
                              accept=".pdf,.txt,.docx"
                              onChange={(event) => {
                                const file = event.target.files?.[0] || null;

                                setSelectedFiles((prev) => ({
                                  ...prev,
                                  [folder.folder_name]: file,
                                }));
                              }}
                              className="flex-1 text-sm"
                            />

                            <button
                              onClick={() => handleUpload(folder.folder_name)}
                              disabled={uploadingFile === folder.folder_name}
                              className={`ml-4 rounded-lg px-4 py-2 text-sm font-medium text-white transition ${
                                uploadingFile === folder.folder_name
                                  ? "cursor-not-allowed bg-slate-400"
                                  : "bg-blue-900 hover:bg-blue-950 cursor-pointer"
                              }`}
                            >
                              {uploadingFile === folder.folder_name
                                ? "Uploading..."
                                : "Upload"}
                            </button>
                          </div>
                        </div>

                        {folder.files.length === 0 ? (
                          <div className="px-4 py-3 text-sm text-slate-500">
                            Folder kosong
                          </div>
                        ) : (
                          folder.files.map((file) => (
                            <div
                              key={`${folder.folder_name}-${file.filename}`}
                              className="flex items-center justify-between px-4 py-3"
                            >
                              <div className="flex items-center gap-3">
                                <FiFileText className="text-blue-600" />

                                <div>
                                  <p className="font-medium">
                                    {file.filename}
                                  </p>

                                  <p className="text-sm text-slate-500">
                                    {file.size_kb} KB
                                  </p>
                                </div>
                              </div>

                              <button
                                onClick={() =>
                                  handleDelete(
                                    folder.folder_name,
                                    file.filename
                                  )
                                }
                                disabled={
                                  deletingFile ===
                                  `${folder.folder_name}-${file.filename}`
                                }
                                className={`rounded-lg px-3 py-1 text-sm transition
    ${deletingFile ===
                                    `${folder.folder_name}-${file.filename}`
                                    ? "cursor-not-allowed bg-slate-200 text-slate-500"
                                    : "cursor-pointer bg-red-100 text-red-700 hover:bg-red-200"
                                  }`}
                              >
                                {deletingFile ===
                                  `${folder.folder_name}-${file.filename}`
                                  ? "Deleting..."
                                  : "Delete"}
                              </button>
                            </div>
                          ))
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default KnowledgeBaseModal;