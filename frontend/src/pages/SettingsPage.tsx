import React, { useEffect, useState } from 'react';
import { Settings, Key, Cpu, Database, Save, CheckCircle2, Zap } from 'lucide-react';
import { SystemSettings } from '../types';
import { api } from '../services/api';

interface SettingsPageProps {
  onSettingsUpdated: (settings: SystemSettings) => void;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ onSettingsUpdated }) => {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [geminiKey, setGeminiKey] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [provider, setProvider] = useState('gemini');
  const [demoMode, setDemoMode] = useState(true);
  const [temperature, setTemperature] = useState(0.2);
  const [maxTokens, setMaxTokens] = useState(4096);
  const [chunkSize, setChunkSize] = useState(600);
  const [chunkOverlap, setChunkOverlap] = useState(120);
  const [topK, setTopK] = useState(5);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await api.getSettings();
      setSettings(data);
      setProvider(data.ai_provider);
      setDemoMode(data.demo_mode);
      setTemperature(data.temperature);
      setMaxTokens(data.max_tokens);
      setChunkSize(data.chunk_size);
      setChunkOverlap(data.chunk_overlap);
      setTopK(data.top_k);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSave = async () => {
    try {
      const updated = await api.updateSettings({
        ai_provider: provider,
        gemini_api_key: geminiKey || undefined,
        openai_api_key: openaiKey || undefined,
        demo_mode: demoMode,
        temperature,
        max_tokens: maxTokens,
        chunk_size: chunkSize,
        chunk_overlap: chunkOverlap,
        top_k: topK,
      });
      setSettings(updated);
      onSettingsUpdated(updated);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (e) {
      alert('Failed to update settings');
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Settings className="w-5 h-5 text-cyan-400" />
            System & AI Provider Settings
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Configure LLM backends, API credentials, RAG chunking parameters, and Demo Mode.
          </p>
        </div>
        {saveSuccess && (
          <span className="px-3 py-1 rounded-lg bg-emerald-950 border border-emerald-800 text-emerald-300 text-xs font-semibold flex items-center gap-1.5 animate-fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Settings Saved
          </span>
        )}
      </div>

      {/* DEMO MODE HIGHLIGHT CARD */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 to-cyan-950/70 border border-cyan-800/80 shadow-glow-cyan flex items-center justify-between">
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400">
            <Zap className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Smart India Hackathon Demo Mode</h3>
            <p className="text-xs text-slate-300 max-w-md">
              When enabled, deterministic source-grounded outputs and synthetic reports run flawlessly without external API key quotas or timeouts.
            </p>
          </div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={demoMode}
            onChange={(e) => setDemoMode(e.target.checked)}
            className="sr-only peer"
          />
          <div className="w-12 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-500"></div>
        </label>
      </div>

      {/* AI Provider Section */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div className="flex items-center space-x-2 pb-2 border-b border-slate-800">
          <Key className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white">LLM Provider Configuration</h3>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1.5">Primary Provider</label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              <option value="gemini">Google Gemini API (Default)</option>
              <option value="openai">OpenAI Compatible Provider</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1.5">
              {provider === 'gemini' ? 'Gemini API Key' : 'OpenAI API Key'}
            </label>
            <input
              type="password"
              placeholder={provider === 'gemini' ? 'AIzaSy...' : 'sk-...'}
              value={provider === 'gemini' ? geminiKey : openaiKey}
              onChange={(e) => provider === 'gemini' ? setGeminiKey(e.target.value) : setOpenaiKey(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-2">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Temperature: {temperature}</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="w-full accent-cyan-500"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Max Output Tokens</label>
            <input
              type="number"
              value={maxTokens}
              onChange={(e) => setMaxTokens(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200"
            />
          </div>
        </div>
      </div>

      {/* RAG Settings Section */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div className="flex items-center space-x-2 pb-2 border-b border-slate-800">
          <Database className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white">RAG Hyperparameters & Retrieval</h3>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Chunk Size (chars)</label>
            <input
              type="number"
              value={chunkSize}
              onChange={(e) => setChunkSize(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Chunk Overlap (chars)</label>
            <input
              type="number"
              value={chunkOverlap}
              onChange={(e) => setChunkOverlap(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Top-K Context Chunks</label>
            <input
              type="number"
              value={topK}
              onChange={(e) => setTopK(parseInt(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200"
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end pt-2">
        <button
          onClick={handleSave}
          className="flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold shadow-glow-cyan transition-all"
        >
          <Save className="w-4 h-4" />
          <span>Save Configuration</span>
        </button>
      </div>
    </div>
  );
};
