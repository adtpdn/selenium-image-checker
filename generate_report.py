import json
from datetime import datetime

def generate_html(results):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Check Status</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; }}
            th, td {{ border: 1px solid black; padding: 5px; }}
            .ok {{ color: green; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Image Check Status</h1>
        <p>Last updated: {timestamp}</p>
        <table>
            <tr><th>URL</th><th>Chrome Status</th><th>Firefox Status</th></tr>
            {table_rows}
        </table>
    </body>
    </html>
    """

    rows = ""
    for url, data in results['chrome'].items():
        chrome_status = data['status']
        firefox_status = results['firefox'][url]['status']
        rows += f"<tr><td>{url}</td><td class='{chrome_status.lower()}'>{chrome_status}</td><td class='{firefox_status.lower()}'>{firefox_status}</td></tr>"

    return html_template.format(timestamp=results['timestamp'], table_rows=rows)

try:
    # Read the results
    with open('results.json', 'r') as f:
        results = json.load(f)

    # Generate the HTML report
    html_report = generate_html(results)

    # Write the HTML report
    with open('public/index.html', 'w') as f:
        f.write(html_report)

    print("HTML report generated successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    raise