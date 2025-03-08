import sys

def count_tokens(line):
    """Zählt die Anzahl der Tokens in einer Zeile (Wörter getrennt durch Leerzeichen)."""
    return len(line.strip().split())

def process_file(input_filename, output_filename, token_limit):
    """Liest die input.txt Datei und schreibt die begrenzte Anzahl an Token in output.txt."""
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    total_tokens = 0
    write_data = []
    block = []
    
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("\\t"):  # Neue Blockmarkierung
            if block and total_tokens + count_tokens(line) > token_limit:
                break  # Stoppt das Schreiben, wenn das Limit überschritten wird
            
            # Block in die Datei speichern, wenn es vorher einen gab
            if block:
                write_data.extend(block + ['\n'])
            
            block = [line + '\n']  # Neuer Block beginnt
            total_tokens += count_tokens(line)
        elif block:
            block.append(line + '\n')  # Restliche Zeilen zum aktuellen Block hinzufügen
    
    # Letzten gültigen Block speichern
    if block and total_tokens <= token_limit:
        write_data.extend(block + ['\n'])
    
    # Schreiben in die Datei nach vollständiger Verarbeitung
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(write_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 skriptFileName.py inputfileName.txt outputfileName.txt token_limit")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    try:
        token_limit = int(sys.argv[3])
    except ValueError:
        print("Error: token_limit must be an integer.")
        sys.exit(1)
    
    process_file(input_filename, output_filename, token_limit)
