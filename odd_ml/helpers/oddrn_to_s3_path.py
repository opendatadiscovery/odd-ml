def oddrn_to_s3_path(oddrn: str) -> str:
    """Convert oddrn to s3 path"""
    s3_prefix = "//s3"
    if not oddrn.startswith(s3_prefix):
        raise ValueError(f"Unsupported oddrn format {oddrn}, must start with //s3")

    _, bucket, _, keys = oddrn.split("/")[-4:]

    # by default s3 adapter join keys with ":"
    keys = keys.replace(":", "/")

    return f"s3://{bucket}/{keys}"
