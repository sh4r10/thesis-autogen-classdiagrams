import os
import pickle
import sys
from pathlib import Path

def read_stat_file(file_path):
    """Reads a .stat file using pickle and returns the loaded dictionary."""
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def generate_html_table(stat_dict, file_name):
    """Generates an HTML table for the statistics dictionary."""
    html = f"<h2>{file_name}</h2>\n"
    html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse;'>\n"
    html += "<tr><th>Category</th><th>TP</th><th>FP</th><th>FN</th><th>Precision</th><th>Recall</th><th>F1</th></tr>\n"

    for category, metrics in stat_dict.items():
        html += f"<tr><td>{category}</td>"
        html += f"<td>{metrics.get('tp', '-')}</td>"
        html += f"<td>{metrics.get('fp', '-')}</td>"
        html += f"<td>{metrics.get('fn', '-')}</td>"
        html += f"<td>{metrics.get('precision', '-')}</td>"
        html += f"<td>{metrics.get('recall', '-')}</td>"
        html += f"<td>{metrics.get('f1', '-')}</td>"
        html += "</tr>\n"

    html += "</table>\n"
    return html

def main(folder_path):
    """Main function to read .stat files and generate an HTML report."""
    folder = Path(folder_path)
    if not folder.is_dir():
        print("Error: The specified path is not a directory.")
        sys.exit(1)

    html_content = "<html>\n<head><title>Statistics Report</title></head>\n<body>\n"
    html_content += "<h1>Statistics Report</h1>\n"

    stat_files = list(folder.glob("*.stat"))
    if not stat_files:
        print("No .stat files found in the specified folder.")
        sys.exit(1)

    for stat_file in stat_files:
        try:
            stat_data = read_stat_file(stat_file)
            file_name = stat_file.name
            html_content += generate_html_table(stat_data, file_name)
        except Exception as e:
            print(f"Error reading {stat_file}: {e}")
    
    html_content += "</body>\n</html>"

    output_file = folder / "statistics_report.html"
    with open(output_file, 'w') as file:
        file.write(html_content)

    print(f"HTML report generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    main(folder_path)

