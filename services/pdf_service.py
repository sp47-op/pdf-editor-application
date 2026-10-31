import fitz  # PyMuPDF
import os


class PDFService:

    def merge_pdfs(self, pdf_files, output_path):
        merged_pdf = fitz.open()

        try:
            for pdf in pdf_files:
                doc = fitz.open(pdf)
                merged_pdf.insert_pdf(doc)
                doc.close()

            merged_pdf.save(output_path)
            merged_pdf.close()

            return output_path

        except Exception as e:
            raise Exception(f"Merge failed: {e}")

    def split_pdf(self, input_pdf, start_page, end_page, output_path):
        try:
            doc = fitz.open(input_pdf)
            new_pdf = fitz.open()

            new_pdf.insert_pdf(
                doc,
                from_page=start_page - 1,
                to_page=end_page - 1
            )

            new_pdf.save(output_path)

            doc.close()
            new_pdf.close()

            return output_path

        except Exception as e:
            raise Exception(f"Split failed: {e}")

    def rotate_page(self, input_pdf, page_number, angle, output_path):
        try:
            doc = fitz.open(input_pdf)

            page = doc[page_number - 1]
            page.set_rotation(angle)

            doc.save(output_path)
            doc.close()

            return output_path

        except Exception as e:
            raise Exception(f"Rotation failed: {e}")

    def delete_pages(self, input_pdf, pages_to_delete, output_path):
        try:
            doc = fitz.open(input_pdf)

            for page in sorted(pages_to_delete, reverse=True):
                doc.delete_page(page - 1)

            doc.save(output_path)
            doc.close()

            return output_path

        except Exception as e:
            raise Exception(f"Delete failed: {e}")

    def extract_text(self, input_pdf):
        try:
            doc = fitz.open(input_pdf)

            text = ""

            for page in doc:
                text += page.get_text()

            doc.close()

            return text

        except Exception as e:
            raise Exception(f"Extraction failed: {e}")