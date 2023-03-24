import os
import glob
import PyPDF2
import typer
import time
from rich.progress import Progress, BarColumn, TextColumn
from concurrent.futures import ThreadPoolExecutor

app = typer.Typer()

def concise_filename(filename: str, max_len: int = 25):
    if len(filename) <= max_len:
        return filename
    half_len = (max_len - 3) // 2
    return f"{filename[:half_len]}...{filename[-half_len:]}"

def reverse_pdf_page_order(input_pdf: str, output_pdf: str, task_id: int, progress: Progress):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)

        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in reversed(range(pdf_reader.numPages)):
            pdf_writer.addPage(pdf_reader.getPage(page_num))
            progress.update(task_id, advance=1)

        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)

    typer.echo(f"Reversed PDF page order for {input_pdf}. Output saved to {output_pdf}")

def update_main_progress(main_task_id, progress):
    progress.update(main_task_id, advance=1)

@app.command()
def main(input_path: str = typer.Argument(..., help="Input PDF file or folder path"),
         output_folder: str = typer.Option(None, help="Output folder path (optional)")):

    pdf_files = []

    if os.path.isfile(input_path):
        pdf_files.append(input_path)
    elif os.path.isdir(input_path):
        pdf_files = glob.glob(os.path.join(input_path, "*.pdf"))
    else:
        typer.echo("Invalid input path. Please provide a valid PDF file or folder path.")
        return

    if not pdf_files:
        typer.echo("No PDF files found in the input folder.")
        return

    total_files = len(pdf_files)
    with Progress(TextColumn("[bold {task.fields[color]}]{task.fields[name]}", justify="right"),
                  BarColumn(bar_width=None),
                  "[bold {task.fields[color]}]{task.percentage:>3.1f}%", auto_refresh=True) as progress:

        main_task_id = progress.add_task("progress", name="Main Progress", color="blue", total=total_files, spacing="")
        tasks = []

        for pdf_file in pdf_files:
            if output_folder is None:
                output_folder = os.path.dirname(pdf_file)
            output_pdf = os.path.join(output_folder, f"{os.path.basename(pdf_file).replace('.pdf', '')}_rev.pdf")
            with open(pdf_file, 'rb') as file:
                num_pages = PyPDF2.PdfFileReader(file).numPages

            base_name = os.path.basename(pdf_file).replace('.pdf', '')
            concise_name = concise_filename(base_name)
            task_id = progress.add_task("progress", name=concise_name, color="cyan", total=num_pages, spacing="    ")
            tasks.append((pdf_file, output_pdf, task_id))

        with ThreadPoolExecutor() as executor:
            futures = []
            for task_args in tasks:
                future = executor.submit(reverse_pdf_page_order, *task_args, progress=progress)
                future.add_done_callback(lambda _: update_main_progress(main_task_id, progress=progress))
                futures.append(future)

            for future in futures:
                future.result()

if __name__ == "__main__":
    app()
