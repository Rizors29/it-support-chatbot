import { useState } from 'react';
import { HiCpuChip } from "react-icons/hi2";
import { MdKeyboardArrowDown } from "react-icons/md";

function ModelDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState('Llama 3.1 8B');

  return (
    <div className="relative inline-block">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-full bg-white text-sm font-medium hover:bg-gray-50 cursor-pointer transition-colors focus:outline-none focus:ring-1 focus:ring-blue-300"
      >
        <HiCpuChip /> {selected} <MdKeyboardArrowDown className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute left-0 bottom-full mb-2 w-56 rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden z-10">
          <div className="py-1">
            {['Llama 3.1 8B', 'Gemini 2.5 Flash', 'Qwen3-8B'].map((model) => (
              <button
                key={model}
                onClick={() => { setSelected(model); setIsOpen(false); }}
                className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
              >
                {model}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ModelDropdown;