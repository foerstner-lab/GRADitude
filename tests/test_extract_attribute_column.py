from graditudelib import extract_attribute_column
import os

def test_extract_columns():

    test_output_file = "tmp_extract_column_output.csv"
    reference_output_file = "tests/fixtures/extract_column_output.csv"
    
    extract_attribute_column.extract_columns(
        reference_output_file,
        "Name",
        test_output_file
    )
    
    assert open(reference_output_file).read() == open(test_output_file).read()
    os.remove(test_output_file)
