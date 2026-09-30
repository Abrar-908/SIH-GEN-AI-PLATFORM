import React, { useEffect, useState } from 'react';
import { FileCode, ArrowRight, Shield, Sparkles, CheckCircle2 } from 'lucide-react';
import { Template } from '../types';
import { api } from '../services/api';

interface TemplatesPageProps {
  onApplyTemplate: (template: Template) => void;
}

export const TemplatesPage: React.FC<TemplatesPageProps> = ({ onApplyTemplate }) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const data = await api.getTemplates();
      setTemplates(data);
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
          <FileCode className="w-5 h-5 text-cyan-400" />
          Pre-Configured Intelligence Templates
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Select ready-to-use domain templates with curated tone, audience, and multi-format output targets.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {templates.map((t) => (
          <div
            key={t.id}
            className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/50 transition-all flex flex-col justify-between group"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800 font-semibold uppercase">
                  {t.category}
                </span>
                <span className="text-[11px] font-mono text-slate-400">
                  {t.target_audience}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white mb-1.5">{t.name}</h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">{t.description}</p>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800/80 mb-4 space-y-1.5 text-[11px]">
                <div className="flex justify-between text-slate-400">
                  <span>Tone & Style:</span>
                  <span className="text-slate-200 font-medium">{t.tone} · {t.content_style}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Detail Level:</span>
                  <span className="text-slate-200 font-medium">{t.detail_level}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Objective:</span>
                  <span className="text-cyan-300 font-medium">{t.objective}</span>
                </div>
              </div>

              <div className="space-y-1.5 mb-4">
                <span className="text-[10px] uppercase font-mono text-slate-500">Outputs Included:</span>
                <div className="flex flex-wrap gap-1">
                  {t.output_types.map((type, i) => (
                    <span key={i} className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-200 border border-slate-700">
                      {type}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => onApplyTemplate(t)}
              className="w-full py-2 px-3 rounded-lg bg-cyan-600/20 hover:bg-cyan-600/30 border border-cyan-500/40 text-cyan-300 text-xs font-semibold flex items-center justify-center space-x-1.5 group-hover:shadow-glow-cyan transition-all"
            >
              <span>Apply to Transformation</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
