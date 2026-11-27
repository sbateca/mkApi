#!/bin/sh
set -eu

if ! awslocal s3api head-bucket --bucket "$REPORT_PDF_BUCKET" --region "$REPORT_PDF_REGION" 2>/dev/null; then
    set -- --bucket "$REPORT_PDF_BUCKET" --region "$REPORT_PDF_REGION"
    if [ "$REPORT_PDF_REGION" != "us-east-1" ]; then
        set -- "$@" --create-bucket-configuration "LocationConstraint=$REPORT_PDF_REGION"
    fi
    awslocal s3api create-bucket "$@"
fi
