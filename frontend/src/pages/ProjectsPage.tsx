import React, { useEffect, useState } from 'react';
import { FolderKanban, Copy, Trash2, ArrowUpRight, Plus, Sparkles, Layers } from 'lucide-react';
import { Project } from '../types';
import { api } from '../services/api';

interface ProjectsPageProps {
  onOpenProject: (projectId: number) => void;
  onNewTransformation: () => void;
}

export const ProjectsPage: React.FC<ProjectsPageProps> = ({
  onOpenProject,
  onNewTransformation
}) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await api.getProjects();
      setProjects(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDuplicate = async (id: number) => {
    try {
      await api.duplicateProject(id);
      loadProjects();
    } catch (e) {
      alert('Failed to duplicate project');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this project?')) return;
    try {
      await api.deleteProject(id);
      loadProjects();
    } catch (e) {
      alert('Failed to delete project');
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FolderKanban className="w-5 h-5 text-cyan-400" />
            Transformation Projects
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">Manage, duplicate, and reopen previous content transformations.</p>
        </div>
        <button
          onClick={onNewTransformation}
          className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-glow-cyan transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>New Project</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((p) => (
          <div
            key={p.id}
            className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">
                  {p.audience} · {p.tone}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                  p.status === 'Completed' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                  'bg-slate-800 text-slate-400'
                }`}>
                  {p.status}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white truncate mb-1">{p.name}</h3>
              <p className="text-xs text-slate-400 line-clamp-2 mb-3">{p.description || 'No description provided.'}</p>

              {p.selected_outputs && p.selected_outputs.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-4">
                  {p.selected_outputs.map((out, i) => (
                    <span key={i} className="px-1.5 py-0.5 rounded text-[9px] bg-slate-950 text-slate-300 border border-slate-800">
                      {out}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
              <span className="text-[10px] font-mono text-slate-500">
                {new Date(p.created_at).toLocaleDateString()}
              </span>
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => handleDuplicate(p.id)}
                  title="Duplicate Project"
                  className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-cyan-300"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleDelete(p.id)}
                  title="Delete Project"
                  className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-red-400"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => onOpenProject(p.id)}
                  className="flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 text-xs font-medium ml-1"
                >
                  <span>Open</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
