import React from 'react';
import { Sliders, Users, Volume2, Globe, FileSpreadsheet, Target, Palette } from 'lucide-react';

interface ConfigPanelProps {
  audience: string;
  setAudience: (val: string) => void;
  tone: string;
  setTone: (val: string) => void;
  language: string;
  setLanguage: (val: string) => void;
  detailLevel: string;
  setDetailLevel: (val: string) => void;
  objective: string;
  setObjective: (val: string) => void;
  style: string;
  setStyle: (val: string) => void;
}

export const ConfigPanel: React.FC<ConfigPanelProps> = ({
  audience,
  setAudience,
  tone,
  setTone,
  language,
  setLanguage,
  detailLevel,
  setDetailLevel,
  objective,
  setObjective,
  style,
  setStyle,
}) => {
  const audiences = [
    'Executive',
    'General Public',
    'Government Officer',
    'Security Analyst',
    'Technical Team',
    'Media',
    'Researcher'
  ];

  const tones = [
    'Professional',
    'Formal',
    'Technical',
    'Neutral',
    'Urgent',
    'Simplified'
  ];

  const languages = [
    'English',
    'Hindi',
    'Tamil',
    'Telugu'
  ];

  const detailLevels = [
    'Brief',
    'Standard',
    'Detailed',
    'Very Detailed'
  ];

  const objectives = [
    'Inform',
    'Summarize',
    'Warn',
    'Educate',
    'Brief',
    'Analyze',
    'Publish'
  ];

  const styles = [
    'Government',
    'Corporate',
    'Technical',
    'Academic',
    'News',
    'Social Media'
  ];

  return (
    <div className="bg-slate-900/80 rounded-xl border border-slate-800 p-5 backdrop-blur-sm">
      <div className="flex items-center space-x-2 pb-3 border-b border-slate-800 mb-4">
        <Sliders className="w-4 h-4 text-cyan-400" />
        <h3 className="text-sm font-semibold text-white">Transformation Parameters</h3>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {/* Audience */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <Users className="w-3.5 h-3.5 text-cyan-400" />
            Target Audience
          </label>
          <select
            value={audience}
            onChange={(e) => setAudience(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {audiences.map((a) => (
              <option key={a} value={a}>{a}</option>
            ))}
          </select>
        </div>

        {/* Tone */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <Volume2 className="w-3.5 h-3.5 text-indigo-400" />
            Tone
          </label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {tones.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        {/* Language */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <Globe className="w-3.5 h-3.5 text-emerald-400" />
            Language
          </label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {languages.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </div>

        {/* Detail Level */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <FileSpreadsheet className="w-3.5 h-3.5 text-amber-400" />
            Detail Level
          </label>
          <select
            value={detailLevel}
            onChange={(e) => setDetailLevel(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {detailLevels.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        {/* Objective */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <Target className="w-3.5 h-3.5 text-purple-400" />
            Communication Objective
          </label>
          <select
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {objectives.map((o) => (
              <option key={o} value={o}>{o}</option>
            ))}
          </select>
        </div>

        {/* Content Style */}
        <div>
          <label className="text-xs font-medium text-slate-400 flex items-center gap-1.5 mb-1.5">
            <Palette className="w-3.5 h-3.5 text-rose-400" />
            Content Style
          </label>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-medium"
          >
            {styles.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};
