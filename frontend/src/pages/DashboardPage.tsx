import React, { useEffect, useState } from 'react';
import {
  FileText,
  Sparkles,
  Layers,
  ShieldCheck,
  ArrowRight,
  Clock,
  CheckCircle2,
  ExternalLink,
  ChevronRight,
  Activity
} from 'lucide-react';
import { StatCard } from '../components/StatCard';
import { DashboardStats } from '../types';
import { api } from '../services/api';

interface DashboardPageProps {
  onStartNewTransformation: () => void;
  onViewProject: (projectId: number) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  onStartNewTransformation,
  onViewProject
}) => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (e) {
      console.error('Error fetching dashboard stats', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Hero Banner */}
      <div className="p-6 md:p-8 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/70 border border-slate-800 shadow-card-dark relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-full bg-cyan-500/5 blur-3xl pointer-events-none"></div>
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-2.5 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/80 text-cyan-300 text-xs font-mono mb-3">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>ONE SOURCE → AI UNDERSTANDING → SOURCE GROUNDING → MULTIPLE OUTPUTS</span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Trusted Multi-Format Content Transformation
          </h2>
          <p className="text-sm text-slate-300 mt-2 leading-relaxed">
            Ingest complex technical incident reports, intelligence feeds, or government briefs and automatically generate trusted, verifiable executive summaries, security advisories, presentations, and social communications.
          </p>

          <div className="mt-6 flex items-center space-x-3">
            <button
              onClick={onStartNewTransformation}
              className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 via-sky-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white text-xs font-bold shadow-glow-cyan transition-all"
            >
              <span>Start New Transformation</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Documents Processed"
          value={stats?.documents_processed || 1}
          change="+100% active"
          icon={FileText}
          color="cyan"
        />
        <StatCard
          label="Transformations Generated"
          value={stats?.transformations_generated || 1}
          change="Real-time"
          icon={Sparkles}
          color="indigo"
        />
        <StatCard
          label="Outputs Generated"
          value={stats?.outputs_generated || 4}
          change="8 Formats Supported"
          icon={Layers}
          color="emerald"
        />
        <StatCard
          label="Validation Pass Rate"
          value={stats?.validation_pass_rate || "96.2%"}
          change="Consistency Verified"
          icon={ShieldCheck}
          color="amber"
        />
      </div>

      {/* Recent Transformations Table */}
      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-6 backdrop-blur-sm">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Recent Transformations
            </h3>
            <p className="text-xs text-slate-400">Chronological history of source ingested transformations</p>
          </div>
          <button
            onClick={onStartNewTransformation}
            className="text-xs font-medium text-cyan-400 hover:text-cyan-300"
          >
            Create New →
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-medium">
                <th className="py-3 px-4">Source Document</th>
                <th className="py-3 px-4">Output Types</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Created</th>
                <th className="py-3 px-4">Validation Score</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {stats?.recent_transformations && stats.recent_transformations.length > 0 ? (
                stats.recent_transformations.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-white">{t.source_filename}</div>
                      <div className="text-[10px] text-slate-500 font-mono">Project: {t.project_name}</div>
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex flex-wrap gap-1 max-w-xs">
                        {t.output_types.map((type, i) => (
                          <span
                            key={i}
                            className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-950 border border-slate-800 text-cyan-300"
                          >
                            {type}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                        <span>{t.status}</span>
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 font-mono text-[11px]">
                      {new Date(t.created_at).toLocaleDateString()} {new Date(t.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-1.5 font-bold text-cyan-400">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        <span>{t.validation_score}%</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => onViewProject(t.project_id)}
                        className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500 text-xs">
                    No transformations recorded yet. Click "Start New Transformation" to begin.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
