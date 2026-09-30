import React from 'react';
import {
  FileText,
  ShieldAlert,
  Presentation,
  BarChart3,
  Share2,
  MessageSquare,
  Film,
  BrainCircuit,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import { GeneratedOutput } from '../types';

interface OutputCardProps {
  output: GeneratedOutput;
  onOpenDetail: (output: GeneratedOutput) => void;
  onQuickDownload: (output: GeneratedOutput, format: string) => void;
}

export const OutputCard: React.FC<OutputCardProps> = ({
  output,
  onOpenDetail,
  onQuickDownload,
}) => {
  const getIcon = (type: string) => {
    switch (type) {
      case 'Executive Summary': return FileText;
      case 'Security Advisory': return ShieldAlert;
      case 'Presentation': return Presentation;
      case 'Infographic': return BarChart3;
      case 'LinkedIn Post': return Share2;
      case 'X/Twitter Post': return MessageSquare;
      case 'Video Package': return Film;
      case 'Intelligence Brief': return BrainCircuit;
      default: return FileText;
    }
  };

  const Icon = getIcon(output.output_type);

  const getStatusBadge = (state: string) => {
    if (state === 'Approved') {
      return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">Approved</span>;
    } else if (state === 'Rejected') {
      return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-red-950 text-red-300 border border-red-800">Rejected</span>;
    }
    return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-950 text-amber-300 border border-amber-800">Draft v{output.version_count || 1}</span>;
  };

  return (
    <div className="bg-slate-900/80 rounded-xl border border-slate-800 p-5 backdrop-blur-sm hover:border-slate-700 transition-all flex flex-col justify-between group">
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 rounded-lg bg-cyan-950/80 border border-cyan-800/80 text-cyan-400">
              <Icon className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono text-cyan-400 font-semibold uppercase tracking-wider">
                {output.output_type}
              </span>
              <h4 className="text-sm font-bold text-white truncate max-w-[200px]">
                {output.title}
              </h4>
            </div>
          </div>
          {getStatusBadge(output.approval_state)}
        </div>

        {/* Markdown Snippet Preview */}
        <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800/60 mb-3">
          <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed font-sans">
            {output.content_markdown.replace(/[#*`_]/g, '')}
          </p>
        </div>

        {/* Validation and Citations Summary Row */}
        <div className="flex items-center justify-between text-[11px] text-slate-400 mb-4 pb-2 border-b border-slate-800">
          <div className="flex items-center space-x-1.5 text-cyan-300">
            <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
            <span>Consistency: <strong>{output.validation?.consistency_score || 95}%</strong></span>
          </div>
          <span className="font-mono text-slate-400">
            {output.source_references?.length || 0} citations
          </span>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between pt-2">
        <div className="flex items-center space-x-1.5 text-xs">
          {output.output_type === 'Presentation' ? (
            <button
              onClick={() => onQuickDownload(output, 'pptx')}
              className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition-colors"
            >
              PPTX
            </button>
          ) : (
            <>
              <button
                onClick={() => onQuickDownload(output, 'pdf')}
                className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition-colors"
              >
                PDF
              </button>
              <button
                onClick={() => onQuickDownload(output, 'docx')}
                className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition-colors"
              >
                DOCX
              </button>
            </>
          )}
        </div>

        <button
          onClick={() => onOpenDetail(output)}
          className="flex items-center space-x-1 px-3 py-1 rounded-lg bg-cyan-600/20 hover:bg-cyan-600/30 border border-cyan-500/40 text-cyan-300 text-xs font-semibold transition-all group-hover:shadow-glow-cyan"
        >
          <span>Review & Edit</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
