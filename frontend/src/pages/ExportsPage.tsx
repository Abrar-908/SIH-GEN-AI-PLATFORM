import React, { useEffect, useState } from 'react';
import { Download, FileText, Presentation, FileCode, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export const ExportsPage: React.FC = () => {
  const [recentExports, setRecentExports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExports();
  }, []);

  const loadExports = async () => {
    try {
      const data = await api.getRecentExports();
      setRecentExports(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const getFormatBadge = (type: string) => {
    if (type === 'PDF') return 'bg-red-950 text-red-300 border-red-800';
    if (type === 'DOCX') return 'bg-blue-950 text-blue-300 border-blue-800';
    if (type === 'PPTX') return 'bg-orange-950 text-orange-300 border-orange-800';
    return 'bg-slate-800 text-slate-300 border-slate-700';
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-800">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Download className="w-5 h-5 text-cyan-400" />
          Export Center & Download Repository
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Access all published executive PDFs, DOCX reports, PowerPoint decks, and raw JSON/MD artifacts.
        </p>
      </div>

      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-6">
        <h3 className="text-sm font-bold text-white mb-4">Generated Files Available for Download</h3>

        {recentExports.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">
            No exported files generated yet. Perform a transformation and click "Download" to generate artifacts.
          </div>
        ) : (
          <div className="space-y-3">
            {recentExports.map((f, i) => (
              <div
                key={i}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between hover:border-slate-700 transition-all"
              >
                <div className="flex items-center space-x-3">
                  <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-cyan-400">
                    {f.file_type === 'PPTX' ? <Presentation className="w-5 h-5" /> : <FileText className="w-5 h-5" />}
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{f.filename}</h4>
                    <span className="text-[10px] text-slate-500 font-mono">
                      {(f.file_size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${getFormatBadge(f.file_type)}`}>
                    {f.file_type}
                  </span>
                  <a
                    href={f.download_url}
                    download
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-cyan-600/20 hover:bg-cyan-600/30 border border-cyan-500/40 text-cyan-300 text-xs font-semibold transition-all shadow-sm"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
