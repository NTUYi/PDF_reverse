# PDF Reverser

PDF Reverser is a simple command-line utility that reverses the page order of PDF files. This can be helpful if you want to rearrange the pages of a PDF file in reverse order.

## Installation

1. Install Python 3.6 or higher.
2. Clone the repository:
```
git clone https://github.com/your-username/pdf-reverser.git
```
3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

Usage: main.py [OPTIONS] INPUT_PATH

Arguments:
INPUT_PATH Input PDF file or folder path

Options:
--output-folder TEXT Output folder path (optional)
--help Show this message and exit.


- To reverse the page order of a single PDF file:
```
python main.py --output-folder /path/to/output/folder /path/to/input/file.pdf
```


- To reverse the page order of all PDF files in a folder:
```
python main.py --output-folder /path/to/output/folder /path/to/input/folder
```


## Tests

To run the tests, run the following command:

```
pytest -s test_pdf_reverser.py
```