"""Validate infrastructure inventory against fictional company policy.

This is demonstration data and makes no calls to AWS or any other provider.
"""
from __future__ import annotations

REQUIRED_TAGS = ("environment", "owner", "cost_center")
VALID_ENVIRONMENTS = {"development", "testing", "staging"}


def validate_resource(resource: dict) -> list[str]:
    """Return human-readable policy violations for one resource."""
    errors: list[str] = []
    resource_id = resource.get("id", "<missing-id>")
    kind = resource.get("type")
    tags = resource.get("tags", {})

    if not isinstance(tags, dict):
        tags = {}
    for key in REQUIRED_TAGS:
        if not tags.get(key):
            errors.append(f"{resource_id}: required tag '{key}' is missing")
    if tags.get("environment") not in VALID_ENVIRONMENTS:
        errors.append(f"{resource_id}: invalid environment tag")

    if kind == "s3":
        if resource.get("encryption_enabled") is not True:
            errors.append(f"{resource_id}: S3 encryption must be enabled")
        if resource.get("block_public_access") is not True:
            errors.append(f"{resource_id}: S3 public access must be blocked")
    elif kind == "dynamodb":
        if resource.get("encryption_enabled") is not True:
            errors.append(f"{resource_id}: DynamoDB encryption must be enabled")
        if resource.get("point_in_time_recovery") is not True:
            errors.append(f"{resource_id}: DynamoDB PITR must be enabled")
    elif kind == "lambda":
        if resource.get("logging_enabled") is not True:
            errors.append(f"{resource_id}: Lambda logging must be enabled")
        if not (1 <= resource.get("timeout_seconds", 0) <= 60):
            errors.append(f"{resource_id}: Lambda timeout must be between 1 and 60 seconds")
    else:
        errors.append(f"{resource_id}: unsupported resource type '{kind}'")

    return errors


def build_report(resources: list[dict]) -> dict:
    results = []
    for resource in resources:
        errors = validate_resource(resource)
        results.append({"id": resource.get("id", "<missing-id>"),
                        "type": resource.get("type"), "passed": not errors,
                        "violations": errors})
    return {"checked": len(results),
            "passed": sum(item["passed"] for item in results),
            "failed": sum(not item["passed"] for item in results),
            "results": results}
