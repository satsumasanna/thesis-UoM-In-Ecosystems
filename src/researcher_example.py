from data_reader_writer import DataReaderWriter
from unitfier import Unitfier

class ResearcherExample:

    def __init__(self):
        self.modify_data()
    
    def modify_data(self):
        # Instantiate object to read/create data and object to format data into quantities
        drw = DataReaderWriter()
        u = Unitfier(uom_in_key_separator_start="_(", uom_in_key_separator_end=")") # Set the seperator to _()
        
        # Read data from spreadsheet
        data = u.make_file_format_to_code_format(drw.read_csv("../data/researcher_example.csv"))

        # Add uom seperator placeholder to data and put in CSV file
        data = u.add_uom_placeholder(data, uom_in_key=True)
        drw.create_csv(data, "../data/researcher_example_with_uom_placeholder.csv")

        # Manually modify data in CSV file ...


ResearcherExample()