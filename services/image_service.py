from PIL import Image
import fitz
import os


class ImageService:

    def image_to_pdf(self, image_files, output_path):
        images = []

        for file in image_files:
            img = Image.open(file).convert("RGB")
            images.append(img)

        if images:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:]
            )

        return output_path

    def pdf_to_images(self, pdf_file, output_folder):
        pdf = fitz.open(pdf_file)

        for i, page in enumerate(pdf):
            pix = page.get_pixmap()
            pix.save(os.path.join(output_folder, f"page_{i+1}.png"))

        pdf.close()