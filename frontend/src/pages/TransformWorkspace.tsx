import React, { useState, useEffect } from 'react';
import { UploadZone } from '../components/UploadZone';
import { ConfigPanel } from '../components/ConfigPanel';
import { OutputSelector } from '../components/OutputSelector';
import { GenerationProgress } from '../components/GenerationProgress';
import { OutputCard } from '../components/OutputCard';
import { OutputDetailModal } from '../components/OutputDetailModal';
import { DocumentExtractResponse, GeneratedOutput, Project } from '../types';
import { api } from '../services/api';
import { Sparkles, Layers, CheckCircle2, AlertCircle } from 'lucide-react';

interface TransformWorkspaceProps {
  initialProjectId?: number | null;
}

export const TransformWorkspace: React.FC<TransformWorkspaceProps> = ({ initialProjectId }) => {
  const [extractedDoc, setExtractedDoc] = useState<DocumentExtractResponse | null>(null);
  const [isLoadingDoc, setIsLoadingDoc] = useState(false);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);

  // Transformation configuration parameters
  const [audience, setAudience] = useState('Executive');
  const [tone, setTone] = useState('Professional');
  const [language, setLanguage] = useState('English');
  const [detailLevel, setDetailLevel] = useState('Detailed');
  const [objective, setObjective] = useState('Brief');
  const [style, setStyle] = useState('Government');

  // Selected outputs (default to 4 key formats requested)
  const [selectedOutputs, setSelectedOutputs] = useState<string[]>([
    'Executive Summary',
    'Security Advisory',
    'Presentation',
    'LinkedIn Post'
  ]);

  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedOutputs, setGeneratedOutputs] = useState<GeneratedOutput[]>([]);
  const [selectedOutputForDetail, setSelectedOutputForDetail] = useState<GeneratedOutput | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  useEffect(() => {
    if (initialProjectId) {
      loadExistingProject(initialProjectId);
    } else {
      // Auto-load sample document if fresh
      handleLoadSample();
    }
  }, [initialProjectId]);

  const loadExistingProject = async (id: number) => {
    try {
      const p = await api.getProject(id);
      setCurrentProject(p);
      setAudience(p.audience);
      setTone(p.tone);
      setLanguage(p.language);
      setDetailLevel(p.detail_level);
      setObjective(p.objective);
      setStyle(p.style);
      if (p.selected_outputs?.length > 0) {
        setSelectedOutputs(p.selected_outputs);
      }
      if (p.source_document) {
        setExtractedDoc({
          document_id: p.source_document.id,
          filename: p.source_document.filename,
          page_count: p.source_document.page_count,
          chunk_count: p.source_document.chunks?.length || 4,
          headings: ['Incident Summary', 'Timeline', 'Impact', 'Indicators'],
          sample_text: p.source_document.raw_text?.slice(0, 500) || '',
          chunks: p.source_document.chunks || []
        });
      }

      // Load existing outputs
      const outputs = await api.getProjectOutputs(p.id);
      setGeneratedOutputs(outputs);
    } catch (e) {
      console.error('Failed to load project', e);
    }
  };

  const handleLoadSample = async () => {
    setIsLoadingDoc(true);
    try {
      const sample = await api.loadSampleDocument();
      setExtractedDoc(sample);
      setNotification('Loaded simulated Cybersecurity Incident Report.');
      setTimeout(() => setNotification(null), 3000);
    } catch (e: any) {
      alert('Failed to load sample: ' + e.message);
    } finally {
      setIsLoadingDoc(false);
    }
  };

  const handleGenerate = async () => {
    if (!extractedDoc) {
      alert('Please upload or load a source document first.');
      return;
    }

    setIsGenerating(true);
    setNotification(null);

    try {
      // 1. Create or use current Project
      let projId = currentProject?.id;
      if (!projId) {
        const newProj = await api.createProject({
          name: `${extractedDoc.filename.replace(/\.[^/.]+$/, '')} Transformation`,
          description: `Automated multi-format transformation for ${audience} audience`,
          source_document_id: extractedDoc.document_id,
          audience,
          tone,
          language,
          detail_level: detailLevel,
          objective,
          style,
          selected_outputs: selectedOutputs
        });
        setCurrentProject(newProj);
        projId = newProj.id;
      }

      // 2. Run Transformation pipeline
      const outputs = await api.runTransformation({
        project_id: projId,
        selected_outputs: selectedOutputs,
        audience,
        tone,
        language,
        detail_level: detailLevel,
        objective,
        style
      });

      setGeneratedOutputs(outputs);
      setNotification(`Successfully generated ${outputs.length} source-grounded outputs!`);
      setTimeout(() => setNotification(null), 4000);
    } catch (e: any) {
      alert('Transformation error: ' + (e.message || 'Unknown error'));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleQuickDownload = async (output: GeneratedOutput, format: string) => {
    try {
      let res;
      if (format === 'pdf') res = await api.exportPDF(output.id);
      else if (format === 'docx') res = await api.exportDocx(output.id);
      else if (format === 'pptx') res = await api.exportPptx(output.id);
      else res = await api.exportText(output.id, format as any);

      window.open(res.download_url, '_blank');
      setNotification(`Downloaded ${res.filename}`);
      setTimeout(() => setNotification(null), 3000);
    } catch (e) {
      alert('Export failed');
    }
  };

  const handleOutputUpdated = (updated: GeneratedOutput) => {
    setGeneratedOutputs((prev) =>
      prev.map((o) => (o.id === updated.id ? updated : o))
    );
    setSelectedOutputForDetail(updated);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-cyan-400" />
            Transformation Workspace
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Ingest source document, configure multi-target parameters, and generate grounded multi-format outputs.
          </p>
        </div>

        {notification && (
          <div className="px-3.5 py-1.5 rounded-lg bg-cyan-950 border border-cyan-800 text-cyan-300 text-xs font-medium flex items-center space-x-2 animate-fade-in shadow-sm">
            <CheckCircle2 className="w-4 h-4 text-cyan-400" />
            <span>{notification}</span>
          </div>
        )}
      </div>

      {/* Generation Progress Pipeline */}
      <GenerationProgress isGenerating={isGenerating} />

      {/* Main Two-Panel Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT PANEL: Source Ingestion */}
        <div className="lg:col-span-5 h-full">
          <UploadZone
            onExtracted={(doc) => setExtractedDoc(doc)}
            isLoading={isLoadingDoc}
            setIsLoading={setIsLoadingDoc}
            extractedDoc={extractedDoc}
            onLoadSample={handleLoadSample}
          />
        </div>

        {/* RIGHT PANEL: Configuration */}
        <div className="lg:col-span-7 flex flex-col space-y-6">
          <ConfigPanel
            audience={audience}
            setAudience={setAudience}
            tone={tone}
            setTone={setTone}
            language={language}
            setLanguage={setLanguage}
            detailLevel={detailLevel}
            setDetailLevel={setDetailLevel}
            objective={objective}
            setObjective={setObjective}
            style={style}
            setStyle={setStyle}
          />

          <OutputSelector
            selectedOutputs={selectedOutputs}
            setSelectedOutputs={setSelectedOutputs}
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
            canGenerate={!!extractedDoc}
          />
        </div>
      </div>

      {/* GENERATED OUTPUTS SECTION */}
      {generatedOutputs.length > 0 && (
        <div className="mt-8 pt-6 border-t border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                Generated Transformation Outputs ({generatedOutputs.length})
              </h3>
              <p className="text-xs text-slate-400">
                Click "Review & Edit" on any card to inspect claims, citations, versions, or download.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {generatedOutputs.map((output) => (
              <OutputCard
                key={output.id}
                output={output}
                onOpenDetail={(o) => setSelectedOutputForDetail(o)}
                onQuickDownload={handleQuickDownload}
              />
            ))}
          </div>
        </div>
      )}

      {/* Detail & Review Modal */}
      <OutputDetailModal
        output={selectedOutputForDetail}
        onClose={() => setSelectedOutputForDetail(null)}
        onUpdated={handleOutputUpdated}
      />
    </div>
  );
};
