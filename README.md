# docsorter

CLI to organize documents into Year/Month folders based on detected dates.

## Install (development)
    pip install -e .

## Usage
    docsorter run "C:\Users\André\Downloads" "C:\Users\André\Desktop\Arquivo" --dry-run

Date priority: filename patterns → EXIF (images) → file modification time.

## License
MIT
