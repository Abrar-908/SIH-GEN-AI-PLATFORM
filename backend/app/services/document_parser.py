import os
import re
from typing import Dict, Any, List, Tuple
from pathlib import Path

class DocumentParserService:
    @staticmethod
    def parse_file(file_path: str, chunk_size: int = 600, chunk_overlap: int = 120) -> Dict[str, Any]:
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext == ".pdf":
            return DocumentParserService._parse_pdf(file_path, chunk_size, chunk_overlap)
        elif ext in (".docx", ".doc"):
            return DocumentParserService._parse_docx(file_path, chunk_size, chunk_overlap)
        elif ext in (".txt", ".md", ".json", ".csv"):
            return DocumentParserService._parse_txt(file_path, chunk_size, chunk_overlap)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: PDF, DOCX, TXT.")

    @staticmethod
    def _parse_pdf(file_path: str, chunk_size: int, chunk_overlap: int) -> Dict[str, Any]:
        import fitz  # PyMuPDF
        
        doc = fitz.open(file_path)
        page_count = len(doc)
        title = doc.metadata.get("title") or Path(file_path).stem.replace("_", " ").title()
        
        raw_text_pages: List[Tuple[int, str]] = []
        headings: List[str] = []
        
        for page_idx in range(page_count):
            page = doc[page_idx]
            page_text = page.get_text("text")
            page_num = page_idx + 1
            raw_text_pages.append((page_num, page_text))
            
            # Simple heading detection
            lines = [l.strip() for l in page_text.split("\n") if l.strip()]
            for line in lines:
                if len(line) < 80 and (line.isupper() or line.endswith(":") or line.startswith(("#", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8."))):
                    if line not in headings:
                        headings.append(line)
        
        doc.close()
        
        chunks = DocumentParserService._chunk_pages(raw_text_pages, headings, chunk_size, chunk_overlap)
        full_text = "\n\n".join([f"--- Page {p} ---\n{t}" for p, t in raw_text_pages])
        
        return {
            "title": title,
            "file_type": "PDF",
            "page_count": page_count,
            "raw_text": full_text,
            "headings": headings[:20],
            "chunks": chunks
        }

    @staticmethod
    def _parse_docx(file_path: str, chunk_size: int, chunk_overlap: int) -> Dict[str, Any]:
        import docx
        
        doc = docx.Document(file_path)
        title = Path(file_path).stem.replace("_", " ").title()
        headings: List[str] = []
        paragraphs_text: List[str] = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            if para.style.name.startswith("Heading"):
                headings.append(text)
            paragraphs_text.append(text)
            
        # Also parse tables
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_text = " | ".join([c.text.strip() for c in row.cells if c.text.strip()])
                if row_text:
                    table_data.append(row_text)
            if table_data:
                paragraphs_text.append("\n[TABLE DATA]\n" + "\n".join(table_data) + "\n[/TABLE DATA]")

        full_text = "\n\n".join(paragraphs_text)
        
        # In docx, approximate pages (approx 400 words per page)
        words = full_text.split()
        words_per_page = 400
        raw_text_pages: List[Tuple[int, str]] = []
        
        for i in range(0, max(1, len(words)), words_per_page):
            page_num = (i // words_per_page) + 1
            page_str = " ".join(words[i:i + words_per_page])
            raw_text_pages.append((page_num, page_str))
            
        chunks = DocumentParserService._chunk_pages(raw_text_pages, headings, chunk_size, chunk_overlap)
        
        return {
            "title": title,
            "file_type": "DOCX",
            "page_count": len(raw_text_pages),
            "raw_text": full_text,
            "headings": headings[:20],
            "chunks": chunks
        }

    @staticmethod
    def _parse_txt(file_path: str, chunk_size: int, chunk_overlap: int) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            full_text = f.read()
            
        title = Path(file_path).stem.replace("_", " ").title()
        headings: List[str] = []
        
        lines = [l.strip() for l in full_text.split("\n") if l.strip()]
        for line in lines:
            if len(line) < 80 and (line.isupper() or line.startswith(("#", "1.", "2.", "3.", "4.", "SECTION"))):
                if line not in headings:
                    headings.append(line)
                    
        words = full_text.split()
        words_per_page = 400
        raw_text_pages: List[Tuple[int, str]] = []
        
        for i in range(0, max(1, len(words)), words_per_page):
            page_num = (i // words_per_page) + 1
            page_str = " ".join(words[i:i + words_per_page])
            raw_text_pages.append((page_num, page_str))
            
        chunks = DocumentParserService._chunk_pages(raw_text_pages, headings, chunk_size, chunk_overlap)
        
        return {
            "title": title,
            "file_type": "TXT",
            "page_count": len(raw_text_pages),
            "raw_text": full_text,
            "headings": headings[:20],
            "chunks": chunks
        }

    @staticmethod
    def _chunk_pages(pages: List[Tuple[int, str]], headings: List[str], chunk_size: int, chunk_overlap: int) -> List[Dict[str, Any]]:
        chunks = []
        chunk_idx = 1
        
        current_section = "Executive Overview"
        
        for page_num, text in pages:
            # Check if this page contains any heading
            for h in headings:
                if h in text:
                    current_section = h
                    break
                    
            # Split page text into sentences/paragraphs
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            if not paragraphs:
                paragraphs = [text.strip()] if text.strip() else []
                
            current_buffer = ""
            for p in paragraphs:
                if len(current_buffer) + len(p) > chunk_size and len(current_buffer) > 0:
                    chunks.append({
                        "chunk_id": f"chunk_{chunk_idx:02d}",
                        "chunk_index": chunk_idx,
                        "page_number": page_num,
                        "section_name": current_section,
                        "text": current_buffer.strip(),
                        "token_count": len(current_buffer.split())
                    })
                    chunk_idx += 1
                    # Overlap
                    overlap_chars = current_buffer[-chunk_overlap:] if len(current_buffer) > chunk_overlap else ""
                    current_buffer = overlap_chars + " " + p
                else:
                    current_buffer += ("\n" if current_buffer else "") + p
                    
            if current_buffer.strip():
                chunks.append({
                    "chunk_id": f"chunk_{chunk_idx:02d}",
                    "chunk_index": chunk_idx,
                    "page_number": page_num,
                    "section_name": current_section,
                    "text": current_buffer.strip(),
                    "token_count": len(current_buffer.split())
                })
                chunk_idx += 1
                
        return chunks
