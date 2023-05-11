import pint
import sys
import pytest
sys.path.insert(0, '../unitfier/src')
from unitfier import Unitfier

class Tests:

    def test_can_unitfy_data(self):
        # Input mock data
        input = [{
            "time": 1,
            "time_uom": "s",
            "length": 1,
            "length_uom": "m",
            "mass": 1,
            "mass_uom": "kg",
            "electric_current": 1,
            "electric_current_uom": "A",
            "thermodynamic_temperature": 1,
            "thermodynamic_temperature_uom": "K",
            "amount_of_substance": 1,
            "amount_of_substance_uom": "mol",
            "luminous_intensity": 1,
            "luminous_intensity_uom": "cd",
            "string": "one"
        }, {
            "time_uom_s": 2,
            "length_uom_m": 2,
            "mass_uom_kg": 2,
            "electric_current_uom_A": 2,
            "thermodynamic_temperature_uom_K": 2,
            "amount_of_substance_uom_mol": 2,
            "luminous_intensity_uom_cd": 2,
            "string": "one"
        }]

        # Expected output
        expected_output = [{
            "time": pint.Quantity(1.0, "s").to_base_units(),
            "length": pint.Quantity(1.0, "m").to_base_units(),
            "mass": pint.Quantity(1.0, "kg").to_base_units(),
            "electric_current": pint.Quantity(1.0, "A").to_base_units(),
            "thermodynamic_temperature": pint.Quantity(1.0, "K").to_base_units(),
            "amount_of_substance": pint.Quantity(1.0, "mol").to_base_units(),
            "luminous_intensity": pint.Quantity(1.0, "cd").to_base_units(),
            "string": "one"
        }, {
            "time": pint.Quantity(2.0, "s").to_base_units(),
            "length": pint.Quantity(2.0, "m").to_base_units(),
            "mass": pint.Quantity(2.0, "kg").to_base_units(),
            "electric_current": pint.Quantity(2.0, "A").to_base_units(),
            "thermodynamic_temperature": pint.Quantity(2.0, "K").to_base_units(),
            "amount_of_substance": pint.Quantity(2.0, "mol").to_base_units(),
            "luminous_intensity": pint.Quantity(2.0, "cd").to_base_units(),
            "string": "one"
        }]

        # Input mock data (other separator and suffix and not base units)
        input2 = [{
            "time": 1,
            "time unit": "min",
            "length (cm)": 1,
        }]

        # Expected output (other separator and suffix and not base units)
        expected_output2 = [{
            "time": pint.Quantity(1.0, "min").to_base_units(),
            "length": pint.Quantity(1.0, "cm").to_base_units(),
        }]

        # Input mock data (faulty data)
        input3 = [{
            "time_uom_x": 1,
        }]

        # Test
        u = Unitfier()
        assert u.make_file_format_to_code_format(input) == expected_output
        
        u2 = Unitfier(" unit", " (", ")")
        assert u2.make_file_format_to_code_format(input2) == expected_output2

        with pytest.raises(pint.errors.UndefinedUnitError):
             u.make_file_format_to_code_format(input3)


    def test_can_add_uom_suffix_and_separator(self):
        # Input mock data
        input = [{
            "time": 1,
            "length": 1
        }]

        # Expected output (uom_in_key = False)
        expected_output_with_suffix = [{
            "time": 1,
            "time_uom": "x",
            "length": 1,
            "length_uom": "x"
        }]
        
        # Expected output (uom_in_key = True)
        expected_output_with_separator = [{
            "time_uom_x": 1,
            "length_uom_x": 1
        }]

        # Expected output (uom_in_key = False and other suffix)
        expected_output_with_other_suffix = [{
            "time": 1,
            "time unit": "x",
            "length": 1,
            "length unit": "x"
        }]
        
        # Expected output (uom_in_key = True and other separator)
        expected_output_with_other_separator = [{
            "time (x)": 1,
            "length (x)": 1
        }]

        # Test
        u = Unitfier()
        assert u.add_uom_placeholder(input) == expected_output_with_suffix
        assert u.add_uom_placeholder(input, True) == expected_output_with_separator

        u2 = Unitfier(" unit", " (", ")")
        assert u2.add_uom_placeholder(input) == expected_output_with_other_suffix
        assert u2.add_uom_placeholder(input, True) == expected_output_with_other_separator

    def test_can_make_unit_dicts_to_file_format(self):
        # Input mock data
        input = [{
            "time": 1,
            "time_uom": "s",
            "length": 2,
            "length_uom": "m",
            "string": "one"
        }]  
        u = Unitfier("_uom", "_uom_")
        input = u.make_file_format_to_code_format(input)

        # Expected output 
        expected_output = [{
            "time": 1,
            "time_uom": "second",
            "length": 2,
            "length_uom": "meter",
            "string": "one"
        }]

        # Expected output (uom_in_key = True, uom_abbreviated = True) 
        expected_output_abbreviated = [{
            "time_uom_s": 1,
            "length_uom_m": 2,
            "string": "one"
        }]

        # Test
        assert u.make_code_format_to_file_format(input) == expected_output
        assert u.make_code_format_to_file_format(input, True, True) == expected_output_abbreviated

    def test_can_make_pint_quantities_to_file_format(self):
        # Input mock data
        input = [
            pint.Quantity(1, "s"),
            pint.Quantity(1, "m"),
            pint.Quantity(1, "kg"),
            pint.Quantity(1, "A"),
            pint.Quantity(1, "K"),
            pint.Quantity(1, "mol"),
            pint.Quantity(1, "cd")
        ]

        # Expected output 
        expected_output = [{
            "id0_time": 1,
            "id0_time_uom": "second",
            "id1_length": 1,
            "id1_length_uom": "meter",
            "id2_mass": 1,
            "id2_mass_uom": "kilogram",
            "id3_current": 1,
            "id3_current_uom": "ampere",
            "id4_temperature": 1,
            "id4_temperature_uom": "kelvin",
            "id5_substance": 1,
            "id5_substance_uom": "mole",
            "id6_luminosity": 1,
            "id6_luminosity_uom": "candela",
        }]

        # Expected output (uom_in_key = True, uom_abbreviated = True)
        expected_output_uom_in_key = [{
            "id0_time_uom_s": 1,
            "id1_length_uom_m": 1,
            "id2_mass_uom_kg": 1,
            "id3_current_uom_A": 1,
            "id4_temperature_uom_K": 1,
            "id5_substance_uom_mol": 1,
            "id6_luminosity_uom_cd": 1,
        }]
        
        # Test
        u = Unitfier()
        assert u.make_pint_quantities_to_file_format(input) == expected_output
        assert u.make_pint_quantities_to_file_format(input, True, True) == expected_output_uom_in_key
