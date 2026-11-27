from collections.abc import Callable
from contextlib import closing
from functools import cached_property

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from domain.exception.report_exception import ReportPdfUnavailableError


class S3ReportPdfStorage:
    def __init__(self, bucket: str | None, region: str, endpoint_url: str | None):
        self.bucket = bucket
        self.region = region
        self.endpoint_url = endpoint_url

    @cached_property
    def client(self):
        options = {}
        if self.endpoint_url:
            options = {
                "endpoint_url": self.endpoint_url,
                "config": Config(s3={"addressing_style": "path"}),
            }
        return boto3.session.Session().client("s3", region_name=self.region, **options)

    def get_or_create(self, key: str, generate: Callable[[], bytes]) -> bytes:
        if not self.bucket:
            raise ReportPdfUnavailableError()
        try:
            existing = self._get(key)
            if existing is not None:
                return existing

            content = generate()
            try:
                self.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=content,
                    ContentType="application/pdf",
                    IfNoneMatch="*",
                )
            except ClientError as error:
                if error.response["Error"]["Code"] not in (
                    "PreconditionFailed",
                    "ConditionalRequestConflict",
                    "412",
                    "409",
                ):
                    raise
                existing = self._get(key)
                if existing is None:
                    raise
                return existing
            return content
        except (BotoCoreError, ClientError) as error:
            raise ReportPdfUnavailableError() from error

    def _get(self, key: str) -> bytes | None:
        try:
            result = self.client.get_object(Bucket=self.bucket, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise
        with closing(result["Body"]) as body:
            return body.read()
