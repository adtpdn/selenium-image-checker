import json
from string import Template

def generate_html(results):
    html_template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Check Status</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .ok { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>Image Check Status</h1>
        <p>Last updated: $timestamp</p>
        <table>
            <tr>
                <th>URL</th>
                <th>Chrome Status</th>
                <th>Firefox Status</th>
            </tr>
            $table_rows
        </table>
    </body>
    </html>
    """)

    rows = ""
    for url in results['chrome']:
        chrome_status = results['chrome'][url]['status']
        firefox_status = results['firefox'][url]['status']
        rows += f"""
        <tr>
            <td>{url}</td>
            <td class="{'ok' if chrome_status == 'OK' else 'error'}">{chrome_status}</td>
            <td class="{'ok' if firefox_status == 'OK' else 'error'}">{firefox_status}</td>
        </tr>
        """

    return html_template.substitute(timestamp=results['timestamp'], table_rows=rows)

with open('results.json', 'r') as f:
    results = json.load(f)

html_report = generate_html(results)

with open('public/index.html', 'w') as f:
    f.write(html_report)