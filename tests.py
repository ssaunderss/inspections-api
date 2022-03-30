import unittest
from app.validations import *
import json

class ValidationModelCase(unittest.TestCase):
    def test_valid_inspection_1(self):
        f = open('sample_inspections/valid_inspection_01.json')
        inspection = json.load(f)
        f.close()
        # the only way an inspection will be a dict is if it passes all validations
        assert isinstance(InspectionSchema().load(inspection), dict)

    def test_valid_inspection_2(self):
        f = open('sample_inspections/valid_inspection_02.json')
        inspection = json.load(f)
        f.close()
        assert isinstance(InspectionSchema().load(inspection), dict)

    def test_valid_inspection_3(self):
        f = open('sample_inspections/valid_inspection_03.json')
        inspection = json.load(f)
        f.close()
        assert isinstance(InspectionSchema().load(inspection), dict)
    
    def test_invalid_inspection_1(self):
        f = open('sample_inspections/invalid_inspection_01.json')
        inspection = json.load(f)
        f.close()
        with self.assertRaises(ValidationError):
            InspectionSchema().load(inspection)

    def test_invalid_inspection_2(self):
        f = open('sample_inspections/invalid_inspection_02.json')
        inspection = json.load(f)
        f.close()
        with self.assertRaises(ValidationError):
            InspectionSchema().load(inspection)

    def test_invalid_inspection_3(self):
        f = open('sample_inspections/invalid_inspection_03.json')
        inspection = json.load(f)
        f.close()
        with self.assertRaises(ValidationError):
            InspectionSchema().load(inspection)

    def test_invalid_4(self):
        f = open('sample_inspections/invalid_inspection_04.json')
        inspection = json.load(f)
        f.close()
        with self.assertRaises(ValidationError):
            InspectionSchema().load(inspection)

if __name__ == '__main__':
    unittest.main()
