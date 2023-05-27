from typing import List
import pint  # UoM lib


class Unitfier:
    # The constructor takes variables to set the suffix and start/end separator.
    def __init__(self, uom_in_value_suffix: str = "_uom", uom_in_key_separator_start: str = "_uom_", uom_in_key_separator_end: str = ""):
        self.uom_suffix = uom_in_value_suffix
        self.uom_separator_start = uom_in_key_separator_start
        self.uom_separator_end = uom_in_key_separator_end
    
    # A method that adds separators or suffixes, with a unit of measurement placeholder value (x), to all elements in a list of dictionaries. 
    # The method takes a list of dictionaries, to add the placeholders too, as input and a boolean for whether separators (uom_in_key = True) 
    # or suffixes (uom_in_key = False) should be added. The method outputs a list of dictionaries with placeholders added.
    def add_uom_placeholder(self, data: List[dict], uom_in_key: bool = False) -> List[dict]:
        new_data = []
        for dict in data:
            new_dict = {}
            for key in dict:
                if uom_in_key:
                    new_dict[key+self.uom_separator_start+"x"+self.uom_separator_end] = dict[key]
                else:
                    new_dict[key] = dict[key]
                    new_dict[key + self.uom_suffix] = "x"
            new_data.append(new_dict)
        return new_data
    
    # A method that makes data in “code format” into “file format”. The method takes a list of dictionaries as input, containing the data that
    # is to be converted. The method takes a boolean for whether the file format data should use separators (uom_in_key = True) or suffixes 
    # (uom_in_key = False). The method takes an input for whether the unit of measurement names should be given in full or abbreviated form. 
    # The method outputs a list of dictionaries with data in file format.
    def make_code_format_to_file_format(self, data: List[dict], uom_in_key: bool = False, uom_abbreviated: bool = False) -> List[dict]:
        new_data = []

        for dict in data:
            new_dict = {}
            for key in dict:
                if type(dict[key]) == pint.Quantity:
                    units = str(dict[key].units).replace(' ', '')
                    if uom_abbreviated:
                        units = '{:~}'.format(dict[key].units).replace(' ', '')

                    if uom_in_key:
                        new_dict[key+self.uom_separator_start+units] = dict[key].magnitude
                    else:
                        new_dict[key] = dict[key].magnitude
                        new_dict[key+self.uom_suffix] = units
                else:
                    new_dict[key] = dict[key]
            new_data.append(new_dict)

        return new_data
    
    # A method that makes a list of Pint quantities into data in file format. The method takes a list of Pint quantities as input. The method takes a boolean
    # for whether the file format data should use separators (uom_in_key = True) or suffixes (uom_in_key = False). The method takes an input for whether the 
    # unit of measurement names should be given in full or abbreviated form. The method outputs a dictionary of data in file format.
    def make_pint_quantities_to_file_format(self, quantities: List[pint.Quantity], uom_in_key: bool = False, uom_abbreviated: bool = False) -> List[dict]:
        new_dict = {}
        for i, quant in enumerate(quantities):
            key = "id" + str(i) + "_" + str(quant.dimensionality).replace('[', '').replace(']', '').replace(' ', '')
            units = str(quant.units).replace(' ', '')
            if uom_abbreviated:
                units = '{:~}'.format(quant.units).replace(' ', '')

            if uom_in_key:
                new_dict[key+self.uom_separator_start+units] = quant.magnitude
            else:
                new_dict[key] = quant.magnitude
                new_dict[key+self.uom_suffix] = units

        return [new_dict]

    # A method that makes data in “file format” into “code format”. The method takes a list of dictionaries as input, containing the data that is to be converted. 
    # The method outputs a list of dictionaries with data in code format.
    def make_file_format_to_code_format(self, data: List[dict]) -> List[dict]:
        data_unitfied = []

        for obj in data:
            temp_obj = {}

            for key in obj:
                
                # If UoM information is in key:
                # Make unit value (converted to base eg. mm -> m)
                if self.uom_separator_start in key:
                    header_parts = key.split(self.uom_separator_start)
                    
                    if len(header_parts) > 2: 
                        print(f"Error: Key/header '{key}' are not allowed to contain the separator sign '{self.uom_separator_start}' more than ones.") 
                        return False

                    temp_obj[header_parts[0]] = pint.Quantity(float(obj[key]), str(header_parts[1])[0:len(header_parts[1])-len(self.uom_separator_end)]).to_base_units()

                # If UoM information is in seperate column:
                # Make unit value (converted to base eg. mm -> m)
                elif (key+self.uom_suffix) in obj:
                    temp_obj[key] = pint.Quantity(
                        float(obj[key]), str(obj[key+self.uom_suffix])).to_base_units()

                # If no UoM information:
                # Make unitliess value
                else:
                    # Exclude keys containing UoM suffix
                    if (len(key) > len(self.uom_suffix)):
                        if (key[-len(self.uom_suffix):] != self.uom_suffix):
                            temp_obj[key] = obj[key]
                    else:
                        temp_obj[key] = obj[key]

            data_unitfied.append(temp_obj)
        return data_unitfied
