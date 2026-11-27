from io import BytesIO
from unittest.mock import Mock

import boto3
from botocore.response import StreamingBody
from botocore.stub import Stubber

from infrastructure.output.storage.s3_report_pdf_storage import S3ReportPdfStorage


def test_s3_storage_creates_once_and_reuses_existing_pdf():
    bucket = "reports-test"
    key = "reports/example.pdf"
    content = b"%PDF-1.4 example"
    storage = S3ReportPdfStorage(bucket, "us-east-1", None)
    storage.client = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    generate = Mock(return_value=content)
    address = {"Bucket": bucket, "Key": key}
    with Stubber(storage.client) as s3:
        s3.add_client_error(
            "get_object", service_error_code="NoSuchKey", expected_params=address
        )
        s3.add_response(
            "put_object",
            {},
            address
            | {
                "Body": content,
                "ContentType": "application/pdf",
                "IfNoneMatch": "*",
            },
        )
        s3.add_response(
            "get_object",
            {"Body": StreamingBody(BytesIO(content), len(content))},
            address,
        )
        assert storage.get_or_create(key, generate) == content
        assert storage.get_or_create(key, generate) == content
        s3.assert_no_pending_responses()
    generate.assert_called_once_with()
