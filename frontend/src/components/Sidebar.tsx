import React from 'react';
import {
  LayoutDashboard,
  Sparkles,
  FolderKanban,
  History,
  FileCode,
  ShieldCheck,
  Download,
  ScrollText,
  Settings,
  Shield,
  Zap
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  demoMode: boolean;
  userRole: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  demoMode,
  userRole,
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'transform', label: 'Transform Workspace', icon: Sparkles, highlight: true },
    { id: 'projects', label: 'Projects', icon: FolderKanban },
    { id: 'history', label: 'History', icon: History },
    { id: 'templates', label: 'Templates', icon: FileCode },
    { id: 'validation', label: 'Validation Center', icon: ShieldCheck },
    { id: 'exports', label: 'Exports Center', icon: Download },
    { id: 'audit-logs', label: 'Audit Logs', icon: ScrollText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900/90 border-r border-slate-800 flex flex-col justify-between h-screen sticky top-0 backdrop-blur-xl z-20">
      <div>
        {/* Brand header */}
        <div className="p-5 border-b border-slate-800/80">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center shadow-glow-cyan">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
                IntelTransform <span className="text-cyan-400 text-xs px-1.5 py-0.5 rounded bg-cyan-950/80 border border-cyan-800">AI</span>
              </h1>
              <p className="text-[10px] text-slate-400 tracking-wider font-mono uppercase">SIH26154 Defense</p>
            </div>
          </div>
        </div>

        {/* Demo Mode Badge */}
        {demoMode && (
          <div className="mx-4 mt-4 px-3 py-2 rounded-lg bg-cyan-950/40 border border-cyan-800/60 flex items-center space-x-2">
            <Zap className="w-4 h-4 text-cyan-400 animate-pulse" />
            <div>
              <p className="text-xs font-semibold text-cyan-300">DEMO MODE ACTIVE</p>
              <p className="text-[10px] text-cyan-400/80">Offline Deterministic & RAG</p>
            </div>
          </div>
        )}

        {/* Navigation Items */}
        <nav className="p-3 space-y-1 mt-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span className="flex-1 text-left">{item.label}</span>
                {item.highlight && !isActive && (
                  <span className="w-2 h-2 rounded-full bg-cyan-400/80"></span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer User Info */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/40">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-cyan-400">
            {userRole[0]}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-slate-200 truncate">Analyst Workstation</p>
            <span className="inline-block px-1.5 py-0.2 rounded text-[10px] bg-slate-800 text-slate-400 font-mono">
              Role: {userRole}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
};
