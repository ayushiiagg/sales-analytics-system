def read_sales_file(file_path):
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.readlines()
    except Exception as e:
        print("Error reading file:", e)
        return []
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns:
    list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

                # Skip header
                lines = lines[1:]

                # Remove empty lines
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        cleaned_lines.append(line)

                return cleaned_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []
