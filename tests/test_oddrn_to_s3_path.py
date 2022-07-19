from odd_ml.helpers.oddrn_to_s3_path import oddrn_to_s3_path


def test_folder_path():
    test_str = "//s3/cloud/aws/account/account_id/region/eu-central-1/buckets/odd-s3-adapter/keys/csv"
    assert oddrn_to_s3_path(test_str) == "s3://odd-s3-adapter/csv"


def test_file_path():
    test_str = "//s3/cloud/aws/account/account_id/region/eu-central-1/buckets/odd-s3-adapter/keys/csv:file.csv"
    assert oddrn_to_s3_path(test_str) == "s3://odd-s3-adapter/csv/file.csv"


def test_s3_compatible_path():
    test_str = (
        "//s3_compatible/localhost/buckets/tripdata/keys/april:data-1654107834282.csv"
    )

    assert oddrn_to_s3_path(test_str) == "s3://tripdata/april/data-1654107834282.csv"
