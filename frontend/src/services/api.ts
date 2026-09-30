import {
  DashboardStats,
  DocumentExtractResponse,
  SourceDocument,
  Project,
  GeneratedOutput,
  OutputVersion,
  ValidationResult,
  Template,
  AuditLog,
  SystemSettings
} from '../types';

const API_BASE = '/api';

export const api = {
  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) throw new Error('Failed to fetch dashboard stats');
    return res.json();
  },

  // Documents
  async uploadDocument(file: File): Promise<DocumentExtractResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  async loadSampleDocument(): Promise<DocumentExtractResponse> {
    const res = await fetch(`${API_BASE}/documents/sample/load`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to load sample document');
    return res.json();
  },

  async getDocument(id: number): Promise<SourceDocument> {
    const res = await fetch(`${API_BASE}/documents/${id}`);
    if (!res.ok) throw new Error('Failed to fetch document');
    return res.json();
  },

  // Projects
  async getProjects(): Promise<Project[]> {
    const res = await fetch(`${API_BASE}/projects`);
    if (!res.ok) throw new Error('Failed to fetch projects');
    return res.json();
  },

  async getProject(id: number): Promise<Project> {
    const res = await fetch(`${API_BASE}/projects/${id}`);
    if (!res.ok) throw new Error('Failed to fetch project');
    return res.json();
  },

  async createProject(data: Partial<Project>): Promise<Project> {
    const res = await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create project');
    return res.json();
  },

  async duplicateProject(id: number): Promise<Project> {
    const res = await fetch(`${API_BASE}/projects/${id}/duplicate`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to duplicate project');
    return res.json();
  },

  async deleteProject(id: number): Promise<void> {
    const res = await fetch(`${API_BASE}/projects/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete project');
  },

  // Transformations
  async runTransformation(data: {
    project_id: number;
    selected_outputs: string[];
    audience?: string;
    tone?: string;
    language?: string;
    detail_level?: string;
    objective?: string;
    style?: string;
  }): Promise<GeneratedOutput[]> {
    const res = await fetch(`${API_BASE}/transform`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Transformation failed');
    }
    return res.json();
  },

  async getProjectOutputs(projectId: number): Promise<GeneratedOutput[]> {
    const res = await fetch(`${API_BASE}/transform/outputs/${projectId}`);
    if (!res.ok) throw new Error('Failed to fetch project outputs');
    return res.json();
  },

  async getSingleOutput(outputId: number): Promise<GeneratedOutput> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}`);
    if (!res.ok) throw new Error('Failed to fetch output');
    return res.json();
  },

  async updateOutput(outputId: number, data: { content_markdown: string; approval_state?: string; change_summary?: string }): Promise<GeneratedOutput> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}/update`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update output');
    return res.json();
  },

  async regenerateSection(outputId: number, sectionName: string, currentContent: string, feedback?: string): Promise<GeneratedOutput> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}/regenerate-section`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        output_id: outputId,
        section_name: sectionName,
        current_content: currentContent,
        feedback
      }),
    });
    if (!res.ok) throw new Error('Failed to regenerate section');
    return res.json();
  },

  async approveOutput(outputId: number): Promise<GeneratedOutput> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}/approve`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to approve output');
    return res.json();
  },

  async rejectOutput(outputId: number): Promise<GeneratedOutput> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}/reject`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to reject output');
    return res.json();
  },

  async getOutputVersions(outputId: number): Promise<OutputVersion[]> {
    const res = await fetch(`${API_BASE}/transform/output/${outputId}/versions`);
    if (!res.ok) throw new Error('Failed to fetch versions');
    return res.json();
  },

  // Validation
  async getOutputValidation(outputId: number): Promise<ValidationResult> {
    const res = await fetch(`${API_BASE}/validate/output/${outputId}`);
    if (!res.ok) throw new Error('Failed to fetch validation');
    return res.json();
  },

  // Exports
  async exportPDF(outputId: number): Promise<{ filename: string; download_url: string }> {
    const res = await fetch(`${API_BASE}/export/pdf?output_id=${outputId}`, { method: 'POST' });
    if (!res.ok) throw new Error('PDF export failed');
    return res.json();
  },

  async exportDocx(outputId: number): Promise<{ filename: string; download_url: string }> {
    const res = await fetch(`${API_BASE}/export/docx?output_id=${outputId}`, { method: 'POST' });
    if (!res.ok) throw new Error('DOCX export failed');
    return res.json();
  },

  async exportPptx(outputId: number): Promise<{ filename: string; download_url: string }> {
    const res = await fetch(`${API_BASE}/export/pptx?output_id=${outputId}`, { method: 'POST' });
    if (!res.ok) throw new Error('PPTX export failed');
    return res.json();
  },

  async exportText(outputId: number, formatType: 'md' | 'txt' | 'json'): Promise<{ filename: string; download_url: string }> {
    const res = await fetch(`${API_BASE}/export/text?output_id=${outputId}&format_type=${formatType}`, { method: 'POST' });
    if (!res.ok) throw new Error(`${formatType.toUpperCase()} export failed`);
    return res.json();
  },

  async getRecentExports(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/export/recent`);
    if (!res.ok) throw new Error('Failed to fetch recent exports');
    return res.json();
  },

  // History & Audit
  async getHistory(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) throw new Error('Failed to fetch history');
    return res.json();
  },

  async getAuditLogs(): Promise<AuditLog[]> {
    const res = await fetch(`${API_BASE}/audit-logs`);
    if (!res.ok) throw new Error('Failed to fetch audit logs');
    return res.json();
  },

  // Templates
  async getTemplates(): Promise<Template[]> {
    const res = await fetch(`${API_BASE}/templates`);
    if (!res.ok) throw new Error('Failed to fetch templates');
    return res.json();
  },

  // Settings
  async getSettings(): Promise<SystemSettings> {
    const res = await fetch(`${API_BASE}/settings`);
    if (!res.ok) throw new Error('Failed to fetch settings');
    return res.json();
  },

  async updateSettings(data: Partial<SystemSettings>): Promise<SystemSettings> {
    const res = await fetch(`${API_BASE}/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update settings');
    return res.json();
  }
};
