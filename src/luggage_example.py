from unitfier import Unitfier
from data_reader_writer import DataReaderWriter


class LuggageExample:

    def __init__(self):
        self.without_unitfier()
        print()
        self.with_unitfier()

    def without_unitfier(self):
        # Instantiate object to read/create data
        drw = DataReaderWriter()

        # Read data
        data = drw.read_database_table(
            "../data/data.db", "luggage_data_without_uom")

        # Output the data elements and calculate the total weight
        total_luggage_weight = 0
        for passenger in data:
            print(
                f"Val: {passenger['Luggage_weight']}, Type: {type(passenger['Luggage_weight'])}")
            total_luggage_weight += float(passenger["Luggage_weight"])

        # Output total luggage weight into JSON file
        drw.create_json([{"Total_luggage_weight": total_luggage_weight}],
                        "../data/total_luggage_weight_without_uom.json")

    def with_unitfier(self):
        # Instantiate object to read/create data and object to format data into quantities
        drw = DataReaderWriter()
        u = Unitfier()

        # Read data and make quantaties
        data = u.make_file_format_to_code_format(
            drw.read_database_table("../data/data.db", "luggage_data_with_uom"))

        # Output elements and calculate the total weight
        total_luggage_weight = 0
        for passenger in data:
            print(
                f"Val: {passenger['Luggage_weight']}, Type: {type(passenger['Luggage_weight'])}")

            total_luggage_weight += passenger["Luggage_weight"]

        # Make data into file format and output into JSON file
        total_luggage_weight_file_format = u.make_code_format_to_file_format(
            [{"Total_luggage_weight": total_luggage_weight}], True, True)

        drw.create_json(total_luggage_weight_file_format,
                        "../data/total_luggage_weight_with_uom.json")


LuggageExample()
