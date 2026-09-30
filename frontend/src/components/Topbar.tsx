import React from 'react';
import { Shield, Sparkles, UserCheck, Bell, Activity } from 'lucide-react';

interface TopbarProps {
  userRole: string;
  setUserRole: (role: string) => void;
  onNewTransformation: () => void;
}

export const Topbar: React.FC<TopbarProps> = ({ userRole, setUserRole, onNewTransformation }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center space-x-3">
        <span className="text-xs font-mono text-cyan-400 bg-cyan-950/70 border border-cyan-800/80 px-2 py-0.5 rounded">
          SIH26154 PROTOTYPE
        </span>
        <span className="text-slate-500">|</span>
        <h2 className="text-sm font-medium text-slate-300 hidden md:block">
          Trusted Multi-Format Content Transformation Engine
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        {/* Role Switcher */}
        <div className="flex items-center space-x-2 bg-slate-800/80 px-2.5 py-1.5 rounded-lg border border-slate-700/80 text-xs">
          <UserCheck className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400">Role:</span>
          <select
            value={userRole}
            onChange={(e) => setUserRole(e.target.value)}
            className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer"
          >
            <option value="Analyst" className="bg-slate-900 text-slate-200">Analyst</option>
            <option value="Admin" className="bg-slate-900 text-slate-200">Admin</option>
            <option value="Reviewer" className="bg-slate-900 text-slate-200">Reviewer</option>
          </select>
        </div>

        {/* Quick CTA */}
        <button
          onClick={onNewTransformation}
          className="flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-glow-cyan transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>New Transformation</span>
        </button>
      </div>
    </header>
  );
};
