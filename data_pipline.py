import os
import json
import re
import uuid
import fitz
from docx import Document


class DataPipeline:

    def __init__(
        self,
        input_folder="Data_layer/raw_data",
        output_folder="Data_layer/processed_chunks",
        chunk_size=800,
        overlap=150
    ):

        self.input_folder = input_folder
        self.output_folder = output_folder
        self.chunk_size = chunk_size
        self.overlap = overlap

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    # ==================================
    # PDF Reader
    # ==================================
    def read_pdf(self, file_path):

        documents = []

        pdf = fitz.open(file_path)

        for page_num in range(len(pdf)):

            page = pdf.load_page(page_num)

            text = page.get_text()

            documents.append({

                "file_name":
                os.path.basename(file_path),

                "document_type":
                "pdf",

                "page_number":
                page_num + 1,

                "content":
                text
            })

        return documents

    # ==================================
    # DOCX Reader
    # ==================================
    def read_docx(self, file_path):

        doc = Document(file_path)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
            if para.text.strip()
        )

        return [{

            "file_name":
            os.path.basename(file_path),

            "document_type":
            "docx",

            "page_number":
            None,

            "content":
            text
        }]

    # ==================================
    # JSON Reader
    # ==================================
    def read_json(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return [{

            "file_name":
            os.path.basename(file_path),

            "document_type":
            "json",

            "page_number":
            None,

            "content":
            json.dumps(data)
        }]

    # ==================================
    # Generic Reader
    # ==================================
    def read_file(self, file_path):

        ext = os.path.splitext(
            file_path
        )[1].lower()

        if ext == ".pdf":
            return self.read_pdf(file_path)

        elif ext == ".docx":
            return self.read_docx(file_path)

        elif ext == ".json":
            return self.read_json(file_path)

        return []

    # ==================================
    # Read Folder
    # ==================================
    def read_directory(self):

        all_docs = []

        for file_name in os.listdir(
            self.input_folder
        ):

            file_path = os.path.join(
                self.input_folder,
                file_name
            )

            docs = self.read_file(
                file_path
            )

            all_docs.extend(docs)

        return all_docs

    # ==================================
    # Clean Text
    # ==================================
    def clean_text(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==================================
    # Chunk Text
    # ==================================
    def chunk_text(self, text):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + self.chunk_size

            chunk = " ".join(
                words[start:end]
            )

            chunks.append(chunk)

            start += (
                self.chunk_size -
                self.overlap
            )

        return chunks

    # ==================================
    # Process Documents
    # ==================================
    def process_documents(
        self,
        documents
    ):

        all_chunks = []

        for doc in documents:

            text = self.clean_text(
                doc["content"]
            )

            chunks = self.chunk_text(
                text
            )

            for idx, chunk in enumerate(
                chunks
            ):

                all_chunks.append({

                    "chunk_id":
                    str(uuid.uuid4()),

                    "pdf_id":
                    doc["file_name"],

                    "file_name":
                    doc["file_name"],

                    "document_type":
                    doc["document_type"],

                    "page_number":
                    doc["page_number"],

                    "chunk_number":
                    idx + 1,

                    "bounding_box":
                    None,

                    "chunk_text":
                    chunk
                })

        return all_chunks

    # ==================================
    # Save Chunks
    # ==================================
    def save_chunks(
        self,
        chunks
    ):

        output_path = os.path.join(
            self.output_folder,
            "chunks.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chunks,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(chunks)} chunks"
        )

        print(
            f"Location: {output_path}"
        )

    # ==================================
    # Full Pipeline
    # ==================================
    def run(self):

        documents = self.read_directory()

        print(
            f"Loaded {len(documents)} documents"
        )

        chunks = self.process_documents(
            documents
        )

        self.save_chunks(chunks)

        return chunks


# ==================================
# Main
# ==================================

if __name__ == "__main__":

    pipeline = DataPipeline()

    chunks = pipeline.run()

    print(
        f"Total Chunks: {len(chunks)}"
    )