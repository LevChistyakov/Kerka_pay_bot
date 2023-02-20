import csv
import os.path

from tortoise import Model


class CsvFile:

    def __init__(self, file_name: str):
        self.file_name = self.get_correct_file_name(file_name)
        self.path_to_file = self.create_path()

    def create_path(self):
        path = os.path.join("app", "files", "local_files", "tables", self.file_name)

        return path

    @staticmethod
    def get_correct_file_name(file_name: str) -> str:
        if not file_name.endswith(".csv"):
            return file_name + ".csv"

        return file_name

    def create_table_from_query_result(self, query_result: list[Model]):
        with open(self.path_to_file, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(
                file,
                delimiter=";",
            )

            attr_names = query_result[0]._meta.fields
            writer.writerow(attr_names)

            for item in query_result:
                writer.writerow([getattr(item, attr_name) for attr_name in attr_names])
