from abc import ABC, abstractmethod


class Report(ABC):
    def __init__(self):
        self.data = []

    @abstractmethod
    def generate_report(self):
        raise NotImplementedError

    def add_data(self, record):
        self.data.append(record)


class ReportCSV(Report):

    def generate_report(self):
        print('Report in CSV')


csv = ReportCSV()

class WeatherService:
    def get_report(self, report_service: Report):
        report_service.generate_report()


ws = WeatherService()
ws.get_report(csv)