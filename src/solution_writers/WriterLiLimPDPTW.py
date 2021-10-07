from src.instance_readers import Reader
from src.solution_writers import Writer

class WriterLiLimPDPTW(Writer):

    def __init__(self):
        super().__init__("WriterLiLimPDPTW")


    def initialize_class_attributes(self):
        return super().initialize_class_attributes()


    def make_header(self):
        text = ""
        text += "Instance name : " + Reader().input_name.split(".")[0] + "\n"
        text += "Authors : " + "" + "\n"
        text += "Date : " + "" + "\n"
        text += "Reference " + "" + "\n"
        text += "Solution" + "\n"
        return text

    def write_solution_specific(self, output_file_name, solution):
        text = self.make_header()
        text += solution.get_routes_output_text()

        with open(output_file_name, "w") as output_file:
            output_file.write(text)

