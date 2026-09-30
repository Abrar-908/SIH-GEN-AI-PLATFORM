import React, { useEffect, useState } from 'react';
import { ScrollText, Shield, CheckCircle2, AlertCircle, Clock } from 'lucide-react';
import { AuditLog } from '../types';
import { api } from '../services/api';

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await api.getAuditLogs();
      setLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action: string) => {
    if (action.includes('Approved')) return 'text-emerald-400 bg-emerald-950/80 border-emerald-800';
    if (action.includes('Rejected')) return 'text-red-400 bg-red-950/80 border-red-800';
    if (action.includes('Exported')) return 'text-indigo-400 bg-indigo-950/80 border-indigo-800';
    if (action.includes('Edited')) return 'text-amber-400 bg-amber-950/80 border-amber-800';
    return 'text-cyan-400 bg-cyan-950/80 border-cyan-800';
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-800">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <ScrollText className="w-5 h-5 text-cyan-400" />
          Enterprise Audit Logs & Compliance Trail
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Immutable audit record of all document uploads, AI transformations, human reviews, edits, and file exports.
        </p>
      </div>

      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 overflow-hidden">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60 text-slate-400 font-medium">
              <th className="py-3 px-5">Timestamp</th>
              <th className="py-3 px-5">User & Role</th>
              <th className="py-3 px-5">Action</th>
              <th className="py-3 px-5">Target / Source</th>
              <th className="py-3 px-5">Details</th>
              <th className="py-3 px-5 text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-5 font-mono text-[11px] text-slate-400">
                  {new Date(log.timestamp).toLocaleDateString()} {new Date(log.timestamp).toLocaleTimeString()}
                </td>
                <td className="py-3.5 px-5">
                  <div className="font-semibold text-white">{log.user_name}</div>
                  <span className="text-[10px] text-slate-500 font-mono">Role: {log.user_role}</span>
                </td>
                <td className="py-3.5 px-5">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${getActionColor(log.action)}`}>
                    {log.action}
                  </span>
                </td>
                <td className="py-3.5 px-5 font-mono text-slate-300">
                  {log.source || 'System Core'}
                </td>
                <td className="py-3.5 px-5 text-slate-400 max-w-sm truncate">
                  {log.details || '—'}
                </td>
                <td className="py-3.5 px-5 text-right">
                  <span className="inline-flex items-center space-x-1 text-emerald-400 text-[11px]">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>{log.status}</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
