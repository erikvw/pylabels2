import warnings
from unittest import TestCase

from pylabels import predefined
from pylabels.specifications import Specification


class TestPredefinedSpecs(TestCase):
    def test_get_all_predefined(self):
        for spec_name, spec_class in predefined.all_predefined_specs():
            # Ensure that each returned spec is a tuple containing class name and class object
            self.assertIsInstance(spec_name, str)
            self.assertTrue(issubclass(spec_class, Specification))

    def test_warning_for_direct_construction(self):
        # Get an arbitrary spec class
        spec_class = next(predefined.all_predefined_specs())[1]

        # Verify we get a warning when constructing it directly
        with warnings.catch_warnings(record=True) as warning_list:
            # Pass 6 positional arguments as required by Specification
            spec_class(1, 1, 1, 1, 1, 1)

            # That should generate a warning since we shouldn't use the constructor directly.
            self.assertEqual(len(warning_list), 1)
