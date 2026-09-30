import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Sparkles } from 'lucide-react';

interface GenerationProgressProps {
  isGenerating: boolean;
  onComplete?: () => void;
}

export const GenerationProgress: React.FC<GenerationProgressProps> = ({ isGenerating }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { num: '01', title: 'Document Analysis', desc: 'Parsing structure, headings & paragraphs' },
    { num: '02', title: 'Context Retrieval', desc: 'Querying RAG FAISS/vector store chunks' },
    { num: '03', title: 'Intent Understanding', desc: 'Evaluating target audience & style objective' },
    { num: '04', title: 'Output Planning', desc: 'Configuring multi-format output outlines' },
    { num: '05', title: 'Content Generation', desc: 'Executing source-grounded LLM synthesis' },
    { num: '06', title: 'Source Validation', desc: 'Classifying claims against source chunks' },
    { num: '07', title: 'Final Formatting', desc: 'Packaging presentations, advisories & briefs' },
  ];

  useEffect(() => {
    if (!isGenerating) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) return prev + 1;
        return prev;
      });
    }, 900);

    return () => clearInterval(interval);
  }, [isGenerating]);

  if (!isGenerating) return null;

  return (
    <div className="bg-slate-900/90 rounded-xl border border-cyan-500/40 p-5 backdrop-blur-md shadow-glow-cyan mb-6">
      <div className="flex items-center space-x-2.5 mb-4">
        <Sparkles className="w-4 h-4 text-cyan-400 animate-spin" />
        <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-300">
          Source-Grounded Transformation Pipeline in Progress
        </h4>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
        {steps.map((s, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div
              key={s.num}
              className={`p-3 rounded-lg border text-left transition-all duration-300 ${
                isDone
                  ? 'bg-emerald-950/40 border-emerald-800 text-emerald-300'
                  : isCurrent
                  ? 'bg-cyan-950/60 border-cyan-500 text-cyan-200 shadow-glow-cyan animate-pulse'
                  : 'bg-slate-950/40 border-slate-800/80 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-mono text-[10px] font-bold">{s.num}</span>
                {isDone ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                ) : isCurrent ? (
                  <Loader2 className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-slate-800"></span>
                )}
              </div>
              <p className="text-[11px] font-bold truncate">{s.title}</p>
              <p className="text-[9px] text-slate-400 mt-0.5 line-clamp-1">{s.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
