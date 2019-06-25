import json

from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def generate_report(self, data):
        raise NotImplementedError


class ReportCSV(Report):
    def generate_report(self, data):
        print('Report in CSV')
        out = '\n'.join([','.join([str(item) for item in row]) for row in data])
        return out


class ReportJSON(Report):
    def generate_report(self, data):
        print('Report in JSON')
        out = json.dumps(data)
        return out


class ReportHTML(Report):
    def generate_report(self, data):
        body = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table {
          width:100%;
        }
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 15px;
          text-align: left;
        }
        table#t01 tr:nth-child(even) {
          background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
         background-color: #fff;
        }
        table#t01 th {
          background-color: black;
          color: white;
        }
        </style>
        </head>
        <body>
        
        <h2>HTML Report</h2>
        <table>
        """
        for row in data:
            body += " <tr> "
            for cell in row:
                body += f" <td>{cell}</td>\n "
            body += " </tr>\n "
        body += "</table>\n</body>\n</html>"

        return body