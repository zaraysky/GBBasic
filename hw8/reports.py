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

