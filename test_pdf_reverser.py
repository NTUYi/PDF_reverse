import pytest
import os
import tempfile
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf_reverser import concise_filename, reverse_pdf_page_order
from rich.progress import Progress

def test_concise_filename():
    assert concise_filename("short_name.pdf") == "short_name.pdf"
    assert concise_filename("a" * 21 + ".pdf") == "a" * 21 + ".pdf"
    long_name = "a" * 50 + ".pdf"
    expected = "a" * 11 + "..." + "a" * 7 + ".pdf"
    print(expected)
    assert concise_filename(long_name, max_len=25) == expected

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_sample_pdf(file_path, page1_text, page2_text):
    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, A4[1] - 50, page1_text)
    c.showPage()
    c.drawString(50, A4[1] - 50, page2_text)
    c.showPage()
    c.save()

def test_reverse_pdf_page_order():
    page1_text = "This is page 1."
    page2_text = "This is page 2."

    with tempfile.TemporaryDirectory() as temp_dir:
        input_pdf_path = os.path.join(temp_dir, "input.pdf")
        output_pdf_path = os.path.join(temp_dir, "output.pdf")

        # Create a sample PDF file with two pages containing text
        create_sample_pdf(input_pdf_path, page1_text, page2_text)

        with Progress() as progress:
            task_id = progress.add_task("progress", total=2)
            reverse_pdf_page_order(input_pdf_path, output_pdf_path, task_id, progress)

        with open(input_pdf_path, 'rb') as input_file, open(output_pdf_path, 'rb') as output_file:
            input_pdf_reader = PdfFileReader(input_file)
            output_pdf_reader = PdfFileReader(output_file)

            assert output_pdf_reader.numPages == input_pdf_reader.numPages

            # Check if the pages are reversed
            assert output_pdf_reader.getPage(0).extractText().strip() == page2_text
            assert output_pdf_reader.getPage(1).extractText().strip() == page1_text


