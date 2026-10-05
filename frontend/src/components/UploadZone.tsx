import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  FileUp,
  Image as ImageIcon,
  Mic,
  Video,
  Sparkles,
  ClipboardPaste,
  Layers,
  FileSpreadsheet
} from 'lucide-react';
import { DocumentExtractResponse } from '../types';
import { api } from '../services/api';

interface UploadZoneProps {
  onExtracted: (doc: DocumentExtractResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  extractedDoc: DocumentExtractResponse | null;
  onLoadSample: () => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({
  onExtracted,
  isLoading,
  setIsLoading,
  extractedDoc,
  onLoadSample
}) => {
  const [activeTab, setActiveTab] = useState<'upload' | 'paste' | 'multimodal'>('upload');
  const [pastedText, setPastedText] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (file: File) => {
    setErrorMsg(null);
    setIsLoading(true);
    try {
      const data = await api.uploadDocument(file);
      onExtracted(data);
    } catch (err: any) {
      setErrorMsg(err.message || 'Error parsing document');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasteSubmit = async () => {
    if (!pastedText.trim()) return;
    setErrorMsg(null);
    setIsLoading(true);
    try {
      const blob = new Blob([pastedText], { type: 'text/plain' });
      const file = new File([blob], 'pasted_intel_report.txt', { type: 'text/plain' });
      await handleFileUpload(file);
    } catch (err: any) {
      setErrorMsg(err.message || 'Error processing pasted text');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 rounded-xl border border-slate-800 p-5 backdrop-blur-sm flex flex-col h-full">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Source Ingestion & Extraction
          </h3>
          <p className="text-xs text-slate-400">PDF, DOCX, TXT with RAG metadata extraction</p>
        </div>
        <button
          onClick={onLoadSample}
          disabled={isLoading}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-cyan-950/70 hover:bg-cyan-900/80 border border-cyan-700/60 text-cyan-300 text-xs font-medium transition-all shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Load Sample Incident</span>
        </button>
      </div>

      {/* Ingestion Tabs */}
      <div className="flex space-x-1 p-1 bg-slate-950 rounded-lg border border-slate-800/80 mb-4 text-xs font-medium">
        <button
          onClick={() => setActiveTab('upload')}
          className={`flex-1 py-1.5 rounded-md flex items-center justify-center space-x-1.5 transition-all ${
            activeTab === 'upload' ? 'bg-slate-800 text-cyan-300 shadow-sm' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileUp className="w-3.5 h-3.5" />
          <span>File Upload</span>
        </button>
        <button
          onClick={() => setActiveTab('paste')}
          className={`flex-1 py-1.5 rounded-md flex items-center justify-center space-x-1.5 transition-all ${
            activeTab === 'paste' ? 'bg-slate-800 text-cyan-300 shadow-sm' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <ClipboardPaste className="w-3.5 h-3.5" />
          <span>Paste Text</span>
        </button>
        <button
          onClick={() => setActiveTab('multimodal')}
          className={`flex-1 py-1.5 rounded-md flex items-center justify-center space-x-1.5 transition-all ${
            activeTab === 'multimodal' ? 'bg-slate-800 text-cyan-300 shadow-sm' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Multi-Modal (Roadmap)</span>
        </button>
      </div>

      {errorMsg && (
        <div className="mb-4 p-3 rounded-lg bg-red-950/40 border border-red-800/60 text-red-300 text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Tab: File Upload */}
      {activeTab === 'upload' && (
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files?.[0]) {
              handleFileUpload(e.dataTransfer.files[0]);
            }
          }}
          className="border-2 border-dashed border-slate-700/80 hover:border-cyan-500/50 rounded-xl p-6 text-center cursor-pointer transition-all bg-slate-950/40 hover:bg-slate-950/60 group flex-1 flex flex-col justify-center items-center"
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
            accept=".pdf,.docx,.doc,.txt,.md,.json"
            className="hidden"
          />
          <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 group-hover:border-cyan-500/40 group-hover:bg-cyan-500/10 flex items-center justify-center mb-3 transition-all">
            <UploadCloud className="w-6 h-6 text-slate-400 group-hover:text-cyan-400 transition-colors" />
          </div>
          <p className="text-sm font-medium text-slate-200">
            Click to upload or drag & drop document
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Supports PDF (PyMuPDF), DOCX (python-docx), and TXT
          </p>
        </div>
      )}

      {/* Tab: Paste Text */}
      {activeTab === 'paste' && (
        <div className="flex-1 flex flex-col space-y-3">
          <textarea
            value={pastedText}
            onChange={(e) => setPastedText(e.target.value)}
            placeholder="Paste raw telemetry, incident report, or intelligence memo..."
            className="flex-1 w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 font-mono focus:outline-none focus:border-cyan-500 resize-none min-h-[160px]"
          />
          <button
            onClick={handlePasteSubmit}
            disabled={!pastedText.trim() || isLoading}
            className="py-2 px-4 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold shadow-glow-cyan transition-all"
          >
            {isLoading ? 'Extracting...' : 'Extract & Chunk Ingested Text'}
          </button>
        </div>
      )}

      {/* Tab: Multi-Modal Placeholders */}
      {activeTab === 'multimodal' && (
        <div className="flex-1 grid grid-cols-3 gap-3 p-3 bg-slate-950/40 rounded-xl border border-slate-800/80">
          <div className="p-4 rounded-lg border border-dashed border-slate-800 flex flex-col items-center justify-center text-center opacity-75">
            <ImageIcon className="w-6 h-6 text-slate-400 mb-2" />
            <span className="text-xs font-semibold text-slate-300">OCR Image</span>
            <span className="text-[10px] text-cyan-400 font-mono mt-1">Available in v2</span>
          </div>
          <div className="p-4 rounded-lg border border-dashed border-slate-800 flex flex-col items-center justify-center text-center opacity-75">
            <Mic className="w-6 h-6 text-slate-400 mb-2" />
            <span className="text-xs font-semibold text-slate-300">Audio Telemetry</span>
            <span className="text-[10px] text-cyan-400 font-mono mt-1">Whisper STT</span>
          </div>
          <div className="p-4 rounded-lg border border-dashed border-slate-800 flex flex-col items-center justify-center text-center opacity-75">
            <Video className="w-6 h-6 text-slate-400 mb-2" />
            <span className="text-xs font-semibold text-slate-300">Video Logs</span>
            <span className="text-[10px] text-cyan-400 font-mono mt-1">Frame Analysis</span>
          </div>
        </div>
      )}

      {/* Extracted Document Summary Card */}
      {extractedDoc && (
        <div className="mt-4 p-4 rounded-xl bg-slate-950/90 border border-cyan-800/50 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <div className="p-2 rounded-lg bg-cyan-950 border border-cyan-800 text-cyan-400">
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-white truncate max-w-[220px]">
                  {extractedDoc.filename}
                </p>
                <p className="text-[10px] text-slate-400 font-mono">
                  {extractedDoc.page_count} page(s) · {extractedDoc.chunk_count} RAG chunks
                </p>
              </div>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
              Ready
            </span>
          </div>

          {/* Sample Text Preview */}
          <div className="mt-3 p-2.5 rounded-lg bg-slate-900 border border-slate-800/80">
            <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono mb-1">
              <span>RAG Chunk Index Preview</span>
              <span>chunk_01</span>
            </div>
            <p className="text-xs text-slate-300 line-clamp-3 italic font-sans leading-relaxed">
              "{extractedDoc.sample_text}"
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
