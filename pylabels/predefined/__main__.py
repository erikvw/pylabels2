""" A convenient way to print a list of all known predefined specs. """

from __future__ import print_function

from pylabels.predefined import all_predefined_specs

print("Predefined Specifications:")


for spec_name, _ in all_predefined_specs():
    print(spec_name)
