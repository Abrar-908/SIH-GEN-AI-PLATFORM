export interface DocumentChunk {
  chunk_id: string;
  page_number: number;
  section_name: string;
  text: string;
}

export interface SourceDocument {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  page_count: number;
  title?: string;
  raw_text?: string;
  created_at: string;
  chunks?: DocumentChunk[];
}

export interface DocumentExtractResponse {
  document_id: number;
  filename: string;
  page_count: number;
  chunk_count: number;
  headings: string[];
  sample_text: string;
  chunks: DocumentChunk[];
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  source_document_id?: number;
  source_document?: SourceDocument;
  audience: string;
  tone: string;
  language: string;
  detail_level: string;
  objective: string;
  style: string;
  selected_outputs: string[];
  status: string;
  created_at: string;
  updated_at: string;
}

export interface SourceReference {
  claim: string;
  source_page: number;
  source_chunk: string;
  confidence: number;
  supporting_passage: string;
}

export interface ValidationClaim {
  claim: string;
  source_page: number;
  source_chunk: string;
  status: 'SUPPORTED' | 'PARTIALLY_SUPPORTED' | 'UNSUPPORTED';
  confidence: number;
  analysis: string;
}

export interface ValidationResult {
  id: number;
  output_id: number;
  source_coverage: number;
  supported_claims_count: number;
  partial_claims_count: number;
  unsupported_claims_count: number;
  consistency_score: number;
  claims_detail: ValidationClaim[];
  created_at: string;
}

export interface OutputVersion {
  id: number;
  output_id: number;
  version_number: number;
  content_markdown: string;
  changed_by: string;
  change_summary: string;
  approval_state: string;
  created_at: string;
}

export interface GeneratedOutput {
  id: number;
  project_id: number;
  transformation_id?: number;
  output_type: string;
  title: string;
  content_markdown: string;
  structured_json?: any;
  source_references: SourceReference[];
  validation?: ValidationResult;
  status: string;
  approval_state: string;
  version_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Template {
  id: number;
  name: string;
  category: string;
  description: string;
  target_audience: string;
  tone: string;
  language: string;
  detail_level: string;
  objective: string;
  content_style: string;
  output_types: string[];
  created_at: string;
}

export interface AuditLog {
  id: number;
  timestamp: string;
  user_name: string;
  user_role: string;
  action: string;
  source?: string;
  details?: string;
  status: string;
}

export interface DashboardStats {
  documents_processed: number;
  transformations_generated: number;
  outputs_generated: number;
  validation_pass_rate: string;
  recent_transformations: Array<{
    id: number;
    project_id: number;
    project_name: string;
    source_filename: string;
    output_types: string[];
    status: string;
    created_at: string;
    validation_score: number;
  }>;
}

export interface SystemSettings {
  ai_provider: string;
  gemini_configured: boolean;
  openai_configured: boolean;
  gemini_api_key?: string;
  openai_api_key?: string;
  gemini_model: string;
  openai_model: string;
  temperature: number;
  max_tokens: number;
  chunk_size: number;
  chunk_overlap: number;
  top_k: number;
  demo_mode: boolean;
}

export interface User {
  username: string;
  email: string;
  full_name: string;
  role: 'Admin' | 'Analyst' | 'Reviewer';
}
