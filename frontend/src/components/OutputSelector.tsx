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
  Check
} from 'lucide-react';

interface OutputSelectorProps {
  selectedOutputs: string[];
  setSelectedOutputs: (outputs: string[]) => void;
  onGenerate: () => void;
  isGenerating: boolean;
  canGenerate: boolean;
}

export const OutputSelector: React.FC<OutputSelectorProps> = ({
  selectedOutputs,
  setSelectedOutputs,
  onGenerate,
  isGenerating,
  canGenerate,
}) => {
  const outputOptions = [
    {
      id: 'Executive Summary',
      title: 'Executive Summary',
      desc: 'Situation, Key Findings, Impact, Facts & Recommendations',
      icon: FileText,
      badge: 'C-Suite',
      color: 'from-blue-500/20 to-cyan-500/20 text-cyan-400 border-cyan-500/30'
    },
    {
      id: 'Security Advisory',
      title: 'Security Advisory',
      desc: 'CVSS Severity, Threat Description, IoCs, Mitigation & Roadmap',
      icon: ShieldAlert,
      badge: 'Defense',
      color: 'from-red-500/20 to-amber-500/20 text-red-400 border-red-500/30'
    },
    {
      id: 'Presentation',
      title: 'Presentation',
      desc: '16:9 Slide Deck with Visual Bullet Points & Speaker Notes',
      icon: Presentation,
      badge: 'Slides',
      color: 'from-purple-500/20 to-indigo-500/20 text-purple-400 border-purple-500/30'
    },
    {
      id: 'Infographic',
      title: 'Infographic Blueprint',
      desc: 'Hierarchy, Metrics Callouts, Visual Flow & Icon References',
      icon: BarChart3,
      badge: 'Visual',
      color: 'from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30'
    },
    {
      id: 'LinkedIn Post',
      title: 'LinkedIn Post',
      desc: 'Thought Leadership, Key Takeaways & Industry Hashtags',
      icon: Share2,
      badge: 'Social',
      color: 'from-sky-500/20 to-blue-500/20 text-sky-400 border-sky-500/30'
    },
    {
      id: 'X/Twitter Post',
      title: 'X/Twitter Post',
      desc: '4-Part Multi-Tweet Operational Thread with Grounded Facts',
      icon: MessageSquare,
      badge: 'Real-time',
      color: 'from-slate-500/20 to-slate-400/20 text-slate-300 border-slate-500/30'
    },
    {
      id: 'Video Package',
      title: 'Video Package Storyboard',
      desc: 'Scene-by-Scene Visual Direction, Narration Script & Subtitles',
      icon: Film,
      badge: 'Media',
      color: 'from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30'
    },
    {
      id: 'Intelligence Brief',
      title: 'Intelligence Brief',
      desc: 'Adversary Attribution, Timeline, Risk Indicators & Assessment',
      icon: BrainCircuit,
      badge: 'Threat Intel',
      color: 'from-indigo-500/20 to-cyan-500/20 text-indigo-400 border-indigo-500/30'
    },
  ];

  const toggleOutput = (id: string) => {
    if (selectedOutputs.includes(id)) {
      setSelectedOutputs(selectedOutputs.filter((o) => o !== id));
    } else {
      setSelectedOutputs([...selectedOutputs, id]);
    }
  };

  const selectAll = () => {
    setSelectedOutputs(outputOptions.map((o) => o.id));
  };

  const clearAll = () => {
    setSelectedOutputs([]);
  };

  return (
    <div className="bg-slate-900/80 rounded-xl border border-slate-800 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-white">Target Output Formats</h3>
          <p className="text-xs text-slate-400">Select single or multiple outputs for parallel transformation</p>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <button
            onClick={selectAll}
            className="text-cyan-400 hover:text-cyan-300 font-medium"
          >
            Select All
          </button>
          <span className="text-slate-600">|</span>
          <button
            onClick={clearAll}
            className="text-slate-400 hover:text-slate-300 font-medium"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Grid of Output Format Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {outputOptions.map((opt) => {
          const Icon = opt.icon;
          const isSelected = selectedOutputs.includes(opt.id);
          return (
            <div
              key={opt.id}
              onClick={() => toggleOutput(opt.id)}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all duration-200 relative group flex flex-col justify-between ${
                isSelected
                  ? 'bg-slate-800/90 border-cyan-500 shadow-glow-cyan'
                  : 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/60'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-2 rounded-lg bg-gradient-to-tr ${opt.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex items-center space-x-1.5">
                    <span className="text-[10px] font-mono text-slate-400 px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800">
                      {opt.badge}
                    </span>
                    <div
                      className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${
                        isSelected
                          ? 'bg-cyan-500 border-cyan-500 text-slate-950'
                          : 'border-slate-700 group-hover:border-slate-500'
                      }`}
                    >
                      {isSelected && <Check className="w-3 h-3 stroke-[3]" />}
                    </div>
                  </div>
                </div>
                <h4 className="text-xs font-bold text-white mb-1">{opt.title}</h4>
                <p className="text-[11px] text-slate-400 leading-snug">{opt.desc}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Generation Bar CTA */}
      <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between">
        <div className="text-xs text-slate-400">
          <span className="text-cyan-400 font-bold">{selectedOutputs.length}</span> format(s) selected
        </div>
        <button
          onClick={onGenerate}
          disabled={!canGenerate || isGenerating || selectedOutputs.length === 0}
          className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 via-sky-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-bold shadow-glow-cyan transition-all flex items-center space-x-2"
        >
          <span>{isGenerating ? 'Transforming Content...' : 'Generate Selected Outputs'}</span>
        </button>
      </div>
    </div>
  );
};
