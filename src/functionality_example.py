import random
import pint
from unitfier import Unitfier
from data_reader_writer import DataReaderWriter


class FunctionalityExample:

    def __init__(self):
        u = Unitfier()
        drw = DataReaderWriter()

        ### REFACTOR DATA ###
        example_data = [{
            "time": 1,
            "length": 1,
            "mass": 1,
            "electric_current": 1,
            "thermodynamic_temperature": 1,
            "amount_of_substance": 1,
            "luminous_intensity": 1,
        }]

        # Refactor data in two ways
        example_data_uom_in_value = u.add_uom_placeholder(example_data, False)
        example_data_uom_in_key = u.add_uom_placeholder(example_data, True)

        # Show result
        print("REFACTORE DATA\n")
        print(f"Data with uom in value: {example_data_uom_in_value}\n")
        print(f"Data with uom in key: {example_data_uom_in_key}\n")
        print("##############################\n")

        ### CONVERT PINT QUANTITIES TO FILE AND CODE FORMAT ###
        # Pint quantities
        distance = pint.Quantity(1, "m")
        speed = pint.Quantity(1, "km/hour")
        force = pint.Quantity(1, "newton")

        # Format pint quantities to "file format"
        data_quantities_in_file_format = u.make_pint_quantities_to_file_format([distance, force, speed])

        # Format quantities in "file format" to "code format"
        data_quantities_in_code_format = u.make_file_format_to_code_format(data_quantities_in_file_format)

        # Format quantities in "code format" to "file format"
        data_quantities_back_to_file_format = u.make_code_format_to_file_format(data_quantities_in_code_format)

        # Show result
        print("CONVERT PINT QUANTITIES TO FILE AND CODE FORMAT\n")
        print(f"Original data: {[distance, force, speed]}\n")
        print(f"Data in file format: {data_quantities_in_file_format}\n")
        print(f"Data in code format: {data_quantities_in_code_format}\n")
        print(f"Data back in file format: {data_quantities_back_to_file_format}\n")
        print("##############################\n")

        ######### USE FLOW #########

        ### STEP 1 - READ DATA FROM FILES ###
        # Read data from different file formats/database
        # Data with _uom (uom in value suffix) and _uom_ (uom in key separator)
        data_from_csv = drw.read_csv("../data/data_si_examples_input.csv")
        data_from_json = drw.read_json("../data/data_si_examples_input.json")
        data_from_xml = drw.read_xml("../data/data_si_examples_input.xml")
        data_from_database = drw.read_database_table("../data/data.db", "data_si_examples_input")

        # Show result
        print("STEP 1 - READ DATA\n")
        print(f"Data read from csv: {data_from_csv}\n")
        print(f"Data read from json: {data_from_json}\n")
        print(f"Data read from xml: {data_from_xml}\n")
        print(f"Data read from database: {data_from_database}\n")
        print("##############################\n")

        ### STEP 2 - MAKE UNITS OF DATA ###
        # Make machine readable quantities from the read data
        data_csv_units = u.make_file_format_to_code_format(data_from_csv)
        data_json_units = u.make_file_format_to_code_format(data_from_json)
        data_xml_units = u.make_file_format_to_code_format(data_from_xml)
        data_database_units = u.make_file_format_to_code_format(data_from_database)

        # Make data that is not specified in SI base form to machine readable quantities
        data_si_not_base = {
            "speed_uom_min": 1,
            "height_uom_cm": 1,
            "weight_uom_g": 1,
        }
        data_si_base = u.make_file_format_to_code_format([data_si_not_base])

        # Show result
        print("STEP 2 - MAKE DATA TO CODE FORMAT (UNITFY)\n")
        print(f"Csv data in code format: {data_csv_units}\n")
        print(f"Json data in code format: {data_json_units}\n")
        print(f"Xml data in code format: {data_xml_units}\n")
        print(f"Database data in code format: {data_database_units}\n")
        print(f"Data from code in code fromat: {data_si_base}\n")
        print("##############################\n")

        ### STEP 3 - PERFORM CALCULATIONS WITH THE DATA ###

        # Helper function
        def try_perform_addition(x, y):
            try:
                result = x + y
            except:
                result = "Error"
            print(f"{x} + {y} = {result}\n")

        print("STEP 3 - CALCULATE\n")
        # Addition with units of same UoM
        try_perform_addition(
            data_csv_units[0]["time"], data_json_units[0]["time"])
        # Addition of with units of different UoM (error)
        try_perform_addition(
            data_database_units[0]["length"], data_xml_units[0]["mass"])
        # Addition with string and unit (error)
        try_perform_addition(
            data_csv_units[0]["string"], data_csv_units[0]["electric_current"])
        print("##############################\n")

        ### STEP 4 - ADD NEW AND MODIFY THE DATA ###
        # Add new row to the csv data
        csv_row = {}
        for key in data_csv_units[0]:
            if (type(data_csv_units[0][key]) == pint.Quantity):
                csv_row[key] = pint.Quantity(random.randint(
                    0, 9), data_csv_units[0][key].units)
            else:
                csv_row[key] = random.randint(0, 9)
        data_csv_units.append(csv_row)

        # Modify the first row of the csv data
        for key in data_csv_units[0]:
            if key == "mass":
                data_csv_units[0][key] = data_csv_units[0][key] + \
                    pint.Quantity(10, "kg")

        # Add a new dict of units to the json data
        data_json_units.append(data_quantities_back_to_file_format[0])

        print("STEP 4 - ADD NEW AND MODIFY THE DATA\n")
        print(f"Csv data with added and modified row: {data_csv_units}\n")
        print(f"Json data with added dict: {data_json_units}\n")
        print("##############################\n")

        ### STEP 5 - CREATE A NEW FILE FROM THE DATA ###
        # Convert data in "code format" to "file format"
        data_to_csv = u.make_code_format_to_file_format(data_csv_units, False, False)
        data_to_json = u.make_code_format_to_file_format(data_json_units, True, True)
        data_to_xml = u.make_code_format_to_file_format(data_xml_units, True, False)
        data_to_database = u.make_code_format_to_file_format(data_database_units, False, True)

        # Create files containing the converted data
        drw.create_csv(data_to_csv, "../data/examples_output.csv")
        drw.create_json(data_to_json, "../data/examples_output.json")
        drw.create_xml(data_to_xml, "../data/examples_output.xml")
        drw.create_database_table(data_to_database, "../data/data.db", "examples_output")

        print("STEP 5 - CREATE NEW FILES FROM THE DATA\n")
        print(f"Csv data converted to file format: {data_to_csv}\n")
        print(f"Json data converted to file format: {data_to_json}\n")
        print(f"Xml data converted to file format: {data_to_xml}\n")
        print(f"Database data converted to file format: {data_to_database}\n")
        print("(The converted data is put in files)\n")


FunctionalityExample()
