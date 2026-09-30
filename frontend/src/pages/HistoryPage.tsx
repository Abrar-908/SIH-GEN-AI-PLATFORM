import React, { useEffect, useState } from 'react';
import { History, ShieldCheck, CheckCircle2, ChevronRight, FileText } from 'lucide-react';
import { api } from '../services/api';

interface HistoryPageProps {
  onInspectProject: (projectId: number) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onInspectProject }) => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-800">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <History className="w-5 h-5 text-cyan-400" />
          Transformation History
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">Complete record of multi-format runs and consistency audits.</p>
      </div>

      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 overflow-hidden">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60 text-slate-400 font-medium">
              <th className="py-3 px-5">ID</th>
              <th className="py-3 px-5">Source Ingestion</th>
              <th className="py-3 px-5">Output Formats</th>
              <th className="py-3 px-5">Consistency Score</th>
              <th className="py-3 px-5">Status</th>
              <th className="py-3 px-5">Execution Date</th>
              <th className="py-3 px-5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {history.map((h) => (
              <tr key={h.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-4 px-5 font-mono text-cyan-400 font-bold">#{h.id}</td>
                <td className="py-4 px-5">
                  <div className="font-semibold text-white">{h.source_filename}</div>
                  <div className="text-[10px] text-slate-500 font-mono">Format: {h.source_type}</div>
                </td>
                <td className="py-4 px-5">
                  <div className="flex flex-wrap gap-1 max-w-xs">
                    {h.output_types.map((type: string, i: number) => (
                      <span key={i} className="px-2 py-0.5 rounded text-[10px] bg-slate-950 border border-slate-800 text-cyan-300 font-mono">
                        {type}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-4 px-5">
                  <div className="flex items-center space-x-1 font-bold text-cyan-400">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>{h.validation_score}%</span>
                  </div>
                </td>
                <td className="py-4 px-5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">
                    {h.status}
                  </span>
                </td>
                <td className="py-4 px-5 font-mono text-slate-400 text-[11px]">
                  {new Date(h.created_at).toLocaleString()}
                </td>
                <td className="py-4 px-5 text-right">
                  <button
                    onClick={() => onInspectProject(h.project_id)}
                    className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 text-xs font-medium"
                  >
                    View Project
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
