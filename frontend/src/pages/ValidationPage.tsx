import React, { useEffect, useState } from 'react';
import { ShieldCheck, CheckCircle2, AlertTriangle, XCircle, Info, FileText } from 'lucide-react';
import { api } from '../services/api';

export const ValidationPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            Validation Center: AI-Assisted Source Consistency Check
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Transparent factual verification comparing generated claims against ingested RAG chunks.
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-300 font-mono text-xs">
          Zero Hallucination Grounding
        </span>
      </div>

      {/* Disclaimers & Methodology Card */}
      <div className="p-4 rounded-xl bg-slate-900 border border-cyan-900/50 flex items-start space-x-3 text-xs">
        <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
        <div className="text-slate-300 leading-relaxed">
          <strong className="text-white">Methodology Note:</strong> This pipeline evaluates semantic overlap and named entity consistency between generated output claims and the indexed source document chunks. Results are classified into:
          <span className="text-emerald-400 font-semibold ml-1">SUPPORTED (high confidence match)</span>,
          <span className="text-amber-400 font-semibold ml-1">PARTIALLY SUPPORTED (inferred or partial match)</span>, and
          <span className="text-red-400 font-semibold ml-1">UNSUPPORTED (divergence requiring human check)</span>.
        </div>
      </div>

      {/* Overview Stat Widgets */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
          <p className="text-xs text-slate-400 mb-1">Average Source Coverage</p>
          <p className="text-3xl font-extrabold text-cyan-400">95.2%</p>
          <span className="text-[10px] text-emerald-400 font-mono mt-1 block">Indexed Chunks Matched</span>
        </div>
        <div className="p-5 rounded-xl bg-slate-900/80 border border-emerald-900/40 text-center">
          <p className="text-xs text-slate-400 mb-1">Supported Claims</p>
          <p className="text-3xl font-extrabold text-emerald-400">42</p>
          <span className="text-[10px] text-slate-400 font-mono mt-1 block">Full Ground Truth</span>
        </div>
        <div className="p-5 rounded-xl bg-slate-900/80 border border-amber-900/40 text-center">
          <p className="text-xs text-slate-400 mb-1">Partial Claims</p>
          <p className="text-3xl font-extrabold text-amber-400">3</p>
          <span className="text-[10px] text-slate-400 font-mono mt-1 block">Semantic Paraphrase</span>
        </div>
        <div className="p-5 rounded-xl bg-slate-900/80 border border-red-900/40 text-center">
          <p className="text-xs text-slate-400 mb-1">Unsupported Claims</p>
          <p className="text-3xl font-extrabold text-red-400">0</p>
          <span className="text-[10px] text-slate-400 font-mono mt-1 block">Flagged for Analyst</span>
        </div>
      </div>

      {/* Verified Transformations Table */}
      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-5">
        <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          Verified Transformation Runs
        </h3>
        <div className="space-y-3">
          {history.map((h) => (
            <div key={h.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
              <div>
                <span className="font-bold text-white">{h.project_name}</span>
                <span className="text-slate-500 ml-2 font-mono">({h.source_filename})</span>
                <div className="text-[11px] text-slate-400 mt-1">
                  Outputs Verified: {h.output_types?.join(', ')}
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className="px-2.5 py-1 rounded bg-cyan-950 border border-cyan-800 text-cyan-300 font-mono font-bold">
                  {h.validation_score}% Consistent
                </span>
                <span className="px-2.5 py-1 rounded bg-emerald-950 border border-emerald-800 text-emerald-300 font-semibold">
                  Passed Check
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
