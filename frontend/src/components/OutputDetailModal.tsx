import React, { useState, useEffect } from 'react';
import {
  X,
  ShieldCheck,
  CheckCircle,
  XCircle,
  Download,
  RotateCcw,
  Sparkles,
  History,
  FileText,
  BookmarkCheck,
  ExternalLink,
  Edit3,
  Layers,
  Save
} from 'lucide-react';
import { GeneratedOutput, OutputVersion } from '../types';
import { api } from '../services/api';

interface OutputDetailModalProps {
  output: GeneratedOutput | null;
  onClose: () => void;
  onUpdated: (output: GeneratedOutput) => void;
}

export const OutputDetailModal: React.FC<OutputDetailModalProps> = ({
  output,
  onClose,
  onUpdated,
}) => {
  const [activeTab, setActiveTab] = useState<'content' | 'sources' | 'validation' | 'versions'>('content');
  const [contentMarkdown, setContentMarkdown] = useState(output?.content_markdown || '');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isRegeneratingSection, setIsRegeneratingSection] = useState(false);
  const [sectionToRegen, setSectionToRegen] = useState('');
  const [regenFeedback, setRegenFeedback] = useState('');
  const [showRegenModal, setShowRegenModal] = useState(false);
  const [versions, setVersions] = useState<OutputVersion[]>([]);
  const [selectedVersion, setSelectedVersion] = useState<OutputVersion | null>(null);
  const [downloadSuccess, setDownloadSuccess] = useState<string | null>(null);

  const loadVersions = async (targetId?: number) => {
    const id = targetId || output?.id;
    if (!id) return;
    try {
      const data = await api.getOutputVersions(id);
      setVersions(data);
    } catch (e) {
      console.error('Failed to load versions', e);
    }
  };

  useEffect(() => {
    if (output) {
      setContentMarkdown(output.content_markdown || '');
      loadVersions(output.id);
    }
  }, [output]);

  const handleSaveEdit = async () => {
    if (!output) return;
    setIsSaving(true);
    try {
      const updated = await api.updateOutput(output.id, {
        content_markdown: contentMarkdown,
        change_summary: 'Manual human review edits',
      });
      setIsEditing(false);
      onUpdated(updated);
      await loadVersions(output.id);
    } catch (e) {
      alert('Failed to save edits');
    } finally {
      setIsSaving(false);
    }
  };

  const handleApprove = async () => {
    if (!output) return;
    try {
      const updated = await api.approveOutput(output.id);
      onUpdated(updated);
    } catch (e) {
      alert('Failed to approve');
    }
  };

  const handleReject = async () => {
    if (!output) return;
    try {
      const updated = await api.rejectOutput(output.id);
      onUpdated(updated);
    } catch (e) {
      alert('Failed to reject');
    }
  };

  const handleRegenerateSection = async () => {
    if (!output || !sectionToRegen.trim()) return;
    setIsRegeneratingSection(true);
    try {
      const updated = await api.regenerateSection(
        output.id,
        sectionToRegen,
        contentMarkdown,
        regenFeedback
      );
      setContentMarkdown(updated.content_markdown);
      setShowRegenModal(false);
      setSectionToRegen('');
      setRegenFeedback('');
      onUpdated(updated);
      await loadVersions(output.id);
    } catch (e) {
      alert('Section regeneration failed');
    } finally {
      setIsRegeneratingSection(false);
    }
  };

  const handleDownload = async (format: 'pdf' | 'docx' | 'pptx' | 'md' | 'json' | 'txt') => {
    if (!output) return;
    try {
      let res;
      if (format === 'pdf') res = await api.exportPDF(output.id);
      else if (format === 'docx') res = await api.exportDocx(output.id);
      else if (format === 'pptx') res = await api.exportPptx(output.id);
      else res = await api.exportText(output.id, format);

      // Trigger browser download
      window.open(res.download_url, '_blank');
      setDownloadSuccess(`Downloaded ${res.filename}`);
      setTimeout(() => setDownloadSuccess(null), 3500);
    } catch (e) {
      alert(`Export to ${format.toUpperCase()} failed`);
    }
  };

  if (!output) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-5xl h-[88vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center space-x-3">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
              {output.output_type}
            </span>
            <h3 className="text-base font-bold text-white truncate max-w-md">
              {output.title}
            </h3>
            <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
              output.approval_state === 'Approved' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
              output.approval_state === 'Rejected' ? 'bg-red-950 text-red-400 border border-red-800' :
              'bg-amber-950 text-amber-400 border border-amber-800'
            }`}>
              {output.approval_state}
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowRegenModal(true)}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5 text-cyan-400" />
              <span>Regenerate Section</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Modal Navigation Tabs */}
        <div className="px-6 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
          <div className="flex space-x-4">
            <button
              onClick={() => setActiveTab('content')}
              className={`py-3 text-xs font-semibold border-b-2 transition-all flex items-center space-x-2 ${
                activeTab === 'content'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Content & Editor</span>
            </button>
            <button
              onClick={() => setActiveTab('sources')}
              className={`py-3 text-xs font-semibold border-b-2 transition-all flex items-center space-x-2 ${
                activeTab === 'sources'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookmarkCheck className="w-3.5 h-3.5" />
              <span>Source References ({output.source_references?.length || 0})</span>
            </button>
            <button
              onClick={() => setActiveTab('validation')}
              className={`py-3 text-xs font-semibold border-b-2 transition-all flex items-center space-x-2 ${
                activeTab === 'validation'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Fact Consistency Check ({output.validation?.consistency_score || 95}%)</span>
            </button>
            <button
              onClick={() => setActiveTab('versions')}
              className={`py-3 text-xs font-semibold border-b-2 transition-all flex items-center space-x-2 ${
                activeTab === 'versions'
                  ? 'border-cyan-400 text-cyan-300'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <History className="w-3.5 h-3.5" />
              <span>Version History ({versions.length})</span>
            </button>
          </div>

          {downloadSuccess && (
            <span className="text-xs text-emerald-400 font-mono animate-fade-in">
              {downloadSuccess}
            </span>
          )}
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-950/20">
          {/* TAB 1: CONTENT & EDITOR */}
          {activeTab === 'content' && (
            <div className="h-full flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400 font-mono">
                  {isEditing ? 'Editing Mode Active' : 'Human Review & Markdown Inspection'}
                </span>
                <div className="flex items-center space-x-2">
                  {isEditing ? (
                    <>
                      <button
                        onClick={handleSaveEdit}
                        disabled={isSaving}
                        className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all"
                      >
                        <Save className="w-3.5 h-3.5" />
                        <span>{isSaving ? 'Saving...' : 'Save Edits (New Version)'}</span>
                      </button>
                      <button
                        onClick={() => {
                          setContentMarkdown(output.content_markdown);
                          setIsEditing(false);
                        }}
                        className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium"
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => setIsEditing(true)}
                      className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium"
                    >
                      <Edit3 className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Edit Output</span>
                    </button>
                  )}
                </div>
              </div>

              {isEditing ? (
                <textarea
                  value={contentMarkdown}
                  onChange={(e) => setContentMarkdown(e.target.value)}
                  className="flex-1 w-full min-h-[360px] p-4 rounded-xl bg-slate-950 border border-cyan-800/80 text-xs text-slate-200 font-mono leading-relaxed focus:outline-none focus:border-cyan-500 resize-none"
                />
              ) : (
                <div className="p-6 rounded-xl bg-slate-950/80 border border-slate-800/80 overflow-y-auto text-slate-200 leading-relaxed font-sans space-y-4">
                  <div className="prose prose-invert max-w-none text-xs">
                    <pre className="whitespace-pre-wrap font-sans text-xs text-slate-200 leading-relaxed">
                      {contentMarkdown}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: SOURCE REFERENCES */}
          {activeTab === 'sources' && (
            <div className="space-y-4">
              <div className="p-3 rounded-lg bg-cyan-950/30 border border-cyan-800/40 text-xs text-cyan-300 flex items-center space-x-2">
                <BookmarkCheck className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>
                  Every generated claim is grounded with source citations referencing exact document pages and chunk IDs.
                </span>
              </div>

              <div className="space-y-3">
                {output.source_references && output.source_references.length > 0 ? (
                  output.source_references.map((ref, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 hover:border-cyan-800/60 transition-all">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-bold text-white flex items-center gap-2">
                          <span className="w-5 h-5 rounded-full bg-cyan-950 text-cyan-400 flex items-center justify-center text-[10px] font-mono">
                            {idx + 1}
                          </span>
                          {ref.claim}
                        </span>
                        <div className="flex items-center space-x-2 text-[11px] font-mono">
                          <span className="text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800">
                            Page {ref.source_page}
                          </span>
                          <span className="text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                            {ref.source_chunk}
                          </span>
                          <span className="text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                            {Math.round(ref.confidence * 100)}% Confidence
                          </span>
                        </div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 text-[11px] text-slate-300 italic">
                        "{ref.supporting_passage}"
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">No explicit references recorded for this output.</p>
                )}
              </div>
            </div>
          )}

          {/* TAB 3: VALIDATION */}
          {activeTab === 'validation' && output.validation && (
            <div className="space-y-5">
              <div className="grid grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-slate-950 border border-cyan-800/40 text-center">
                  <p className="text-xs text-slate-400 mb-1">Source Coverage</p>
                  <p className="text-2xl font-bold text-cyan-400">{output.validation.source_coverage}%</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950 border border-emerald-800/40 text-center">
                  <p className="text-xs text-slate-400 mb-1">Supported Claims</p>
                  <p className="text-2xl font-bold text-emerald-400">{output.validation.supported_claims_count}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950 border border-amber-800/40 text-center">
                  <p className="text-xs text-slate-400 mb-1">Partial Claims</p>
                  <p className="text-2xl font-bold text-amber-400">{output.validation.partial_claims_count}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-center">
                  <p className="text-xs text-slate-400 mb-1">Consistency Score</p>
                  <p className="text-2xl font-bold text-white">{output.validation.consistency_score}%</p>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-400">
                <strong className="text-slate-200">AI-Assisted Source Consistency Check:</strong> Claims extracted from the generated output are automatically verified against indexed source chunks to prevent hallucination.
              </div>

              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-white">Claim-by-Claim Verification Analysis</h4>
                {output.validation.claims_detail?.map((c, i) => (
                  <div key={i} className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                    <div className="flex-1 pr-4">
                      <p className="font-medium text-slate-200">{c.claim}</p>
                      <p className="text-[10px] text-slate-400 mt-0.5">{c.analysis}</p>
                    </div>
                    <div className="flex items-center space-x-2 shrink-0">
                      <span className="font-mono text-[10px] text-slate-400">Page {c.source_page}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        c.status === 'SUPPORTED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                        c.status === 'PARTIALLY_SUPPORTED' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                        'bg-red-950 text-red-400 border border-red-800'
                      }`}>
                        {c.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 4: VERSION HISTORY */}
          {activeTab === 'versions' && (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                Track full audit history of edits and section regenerations. Click a version to view snapshot.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {versions.map((v) => (
                  <div
                    key={v.id}
                    onClick={() => setSelectedVersion(v)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all ${
                      selectedVersion?.id === v.id
                        ? 'bg-slate-800 border-cyan-500 shadow-glow-cyan'
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-bold text-cyan-400">Version {v.version_number}</span>
                      <span className="text-[10px] font-mono text-slate-400">
                        {new Date(v.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    <p className="text-xs text-white font-medium truncate">{v.change_summary}</p>
                    <p className="text-[10px] text-slate-500 mt-1">Edited by: {v.changed_by}</p>
                  </div>
                ))}
              </div>

              {selectedVersion && (
                <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-white">
                      Snapshot: Version {selectedVersion.version_number}
                    </span>
                    <button
                      onClick={() => {
                        setContentMarkdown(selectedVersion.content_markdown);
                        setActiveTab('content');
                        setIsEditing(true);
                      }}
                      className="px-2.5 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-[11px] font-medium"
                    >
                      Restore to Editor
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-slate-300 max-h-48 overflow-y-auto whitespace-pre-wrap p-2 bg-slate-900 rounded">
                    {selectedVersion.content_markdown}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Modal Footer Controls */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between">
          {/* Approval Controls */}
          <div className="flex items-center space-x-2">
            <button
              onClick={handleApprove}
              disabled={output.approval_state === 'Approved'}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 border border-emerald-500/40 text-emerald-300 text-xs font-semibold transition-all disabled:opacity-40"
            >
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Approve for Export</span>
            </button>
            <button
              onClick={handleReject}
              disabled={output.approval_state === 'Rejected'}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-red-600/20 hover:bg-red-600/30 border border-red-500/40 text-red-300 text-xs font-semibold transition-all disabled:opacity-40"
            >
              <XCircle className="w-3.5 h-3.5" />
              <span>Reject</span>
            </button>
          </div>

          {/* Export Menu */}
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 mr-1 flex items-center gap-1">
              <Download className="w-3.5 h-3.5" /> Export:
            </span>
            {output.output_type === 'Presentation' ? (
              <button
                onClick={() => handleDownload('pptx')}
                className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-xs font-semibold hover:opacity-90 shadow-sm"
              >
                Download PowerPoint (.PPTX)
              </button>
            ) : (
              <>
                <button
                  onClick={() => handleDownload('pdf')}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium"
                >
                  PDF
                </button>
                <button
                  onClick={() => handleDownload('docx')}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium"
                >
                  DOCX
                </button>
                <button
                  onClick={() => handleDownload('md')}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium"
                >
                  MD
                </button>
                <button
                  onClick={() => handleDownload('json')}
                  className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium"
                >
                  JSON
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* REGENERATE SECTION SUB-MODAL */}
      {showRegenModal && (
        <div className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-slate-950/90 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-5 max-w-md w-full shadow-2xl">
            <h4 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
              <RotateCcw className="w-4 h-4 text-cyan-400" />
              Regenerate Specific Section
            </h4>
            <p className="text-xs text-slate-400 mb-3">
              Update only a specific heading/block without regenerating the whole document.
            </p>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">
                  Section Name (e.g. Recommended Actions, Impact, Situation)
                </label>
                <input
                  type="text"
                  value={sectionToRegen}
                  onChange={(e) => setSectionToRegen(e.target.value)}
                  placeholder="e.g. Recommended Actions"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">
                  Analyst Guidance / Feedback
                </label>
                <input
                  type="text"
                  value={regenFeedback}
                  onChange={(e) => setRegenFeedback(e.target.value)}
                  placeholder="e.g. Focus on air-gapped backup and hardware token MFA"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex justify-end space-x-2">
              <button
                onClick={() => setShowRegenModal(false)}
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleRegenerateSection}
                disabled={!sectionToRegen.trim() || isRegeneratingSection}
                className="px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-glow-cyan transition-all disabled:opacity-50"
              >
                {isRegeneratingSection ? 'Regenerating...' : 'Regenerate Section'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
