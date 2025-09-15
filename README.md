# Advanced File Metadata Analyzer 🕵️‍♂️

A command-line tool written in Python to extract and analyze metadata from various file types, including images and PDFs. This project is a great introduction to digital forensics and data extraction.

This tool can uncover hidden information within files, such as camera settings, software used, and even GPS coordinates where a photo was taken.



---

## ✨ Features

* **Multi-File Support:** Analyzes metadata for images (`.jpg`, `.jpeg`, `.png`) and PDF documents.
* **GPS Data Parsing:** Automatically detects and decodes GPS coordinates from image EXIF data and provides a direct Google Maps link.
* **Data Export:** Saves the extracted metadata to a clean `.txt` file for logging and analysis.
* **User-Friendly CLI:** Simple and straightforward to use from any terminal.

---

## 🛠️ Setup & Installation

Follow these steps to get the tool running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Shreyas1860/File-Metadata-Analyser
    cd File-Metadata-Analyser
    ```

2.  **Create and activate a virtual environment:**
    *(This is the recommended best practice for managing Python dependencies)*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install Pillow PyPDF2
    ```

---

##  usage

The script is run from the command line, with the path to the file as an argument.

* **To analyze an image and print to console:**
    ```bash
    python3 advanced_analyzer.py /path/to/your/image.jpg
    ```

* **To analyze a PDF:**
    ```bash
    python3 advanced_analyzer.py /path/to/your/document.pdf
    ```

* **To analyze a file and export the results:**
    Add the `--export` flag at the end of the command. A new file named `your_file_metadata.txt` will be created.
    ```bash
    python3 advanced_analyzer.py /path/to/your/image.jpg --export
    ```

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, please fork the repository and open a pull request.
