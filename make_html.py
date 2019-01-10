import sys
with open('charts-template.html', 'r') as file_temp:
    html_template = file_temp.read()
with open('charts.html', 'w') as file_html:
    file_html.write(html_template.replace(
        '__CHART_DATA_GOES_HERE__', sys.stdin.read()))
