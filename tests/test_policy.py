"""Unit tests for the synthetic policy engine."""
import json
import unittest
from pathlib import Path
from app.policy import build_report, validate_resource

ROOT = Path(__file__).resolve().parents[1]
BASE_TAGS = {"environment": "testing", "owner": "demo-platform-team", "cost_center": "DEMO-100"}


def resource(kind, **kwargs):
    settings = {"s3": {"encryption_enabled": True, "block_public_access": True},
                "dynamodb": {"encryption_enabled": True, "point_in_time_recovery": True},
                "lambda": {"logging_enabled": True, "timeout_seconds": 30}}
    return {"id": "demo-resource", "type": kind, "tags": dict(BASE_TAGS),
            **settings.get(kind, {}), **kwargs}


class PolicyTests(unittest.TestCase):
    def test_compliant_s3(self):
        self.assertEqual(validate_resource(resource("s3")), [])

    def test_compliant_dynamodb(self):
        self.assertEqual(validate_resource(resource("dynamodb")), [])

    def test_compliant_lambda(self):
        self.assertEqual(validate_resource(resource("lambda")), [])

    def test_s3_encryption_required(self):
        self.assertTrue(any("encryption" in x for x in validate_resource(
            resource("s3", encryption_enabled=False))))

    def test_s3_public_access_block_required(self):
        self.assertTrue(any("public access" in x for x in validate_resource(
            resource("s3", block_public_access=False))))

    def test_dynamodb_backup_required(self):
        self.assertTrue(any("PITR" in x for x in validate_resource(
            resource("dynamodb", point_in_time_recovery=False))))

    def test_lambda_logging_required(self):
        self.assertTrue(any("logging" in x for x in validate_resource(
            resource("lambda", logging_enabled=False))))

    def test_lambda_timeout_limit(self):
        self.assertTrue(any("timeout" in x for x in validate_resource(
            resource("lambda", timeout_seconds=120))))

    def test_tags_required(self):
        self.assertTrue(any("owner" in x for x in validate_resource(
            resource("s3", tags={"environment": "testing", "cost_center": "DEMO-100"}))))

    def test_unknown_resource_rejected(self):
        self.assertTrue(any("unsupported" in x for x in validate_resource(resource("unknown"))))

    def test_all_seeded_resources_compliant(self):
        inventory = json.loads((ROOT / "sample_data" / "resources.json").read_text())
        report = build_report(inventory["resources"])
        self.assertEqual(report["checked"], 18)
        self.assertEqual(report["failed"], 0)


if __name__ == "__main__":
    unittest.main()
