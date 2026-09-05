import argparse
import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "aidenote.py"
SPEC = importlib.util.spec_from_file_location("aidenote_client", MODULE_PATH)
AIDENOTE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = AIDENOTE
SPEC.loader.exec_module(AIDENOTE)


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post(self, path, body, *, operation):
        self.calls.append((path, body, operation))
        return self.response


class AudioUrlTests(unittest.TestCase):
    def test_returns_only_normalized_temporary_url_fields(self):
        client = FakeClient(
            {
                "code": 200,
                "result": {
                    "audiofileFileid": "recording-123",
                    "audiofileTitle": "Weekly meeting",
                    "audiofileFileName": "meeting.m4a",
                    "audioUrl": "https://aidenote.oss-cn.example/recording.m4a?Expires=123&Signature=signed",
                    "audioUrlExpiresAt": "2026-09-05T09:00:00+00:00",
                    "expiresInSeconds": 3600,
                    "audiofileFilePath": "private/user/path",
                },
            }
        )

        result = AIDENOTE.audio_url(client, argparse.Namespace(file_id="recording-123"))

        self.assertEqual(
            client.calls,
            [
                (
                    "/api/audiofileMstr/audioUrl",
                    {"audiofileFileid": "recording-123"},
                    "get recording audio URL",
                )
            ],
        )
        self.assertEqual(result["operation"], "audio-url")
        self.assertEqual(result["fileId"], "recording-123")
        self.assertEqual(result["expiresInSeconds"], 3600)
        self.assertNotIn("audiofileFilePath", result)

    def test_rejects_non_https_url(self):
        client = FakeClient(
            {
                "code": 200,
                "result": {
                    "audiofileFileid": "recording-123",
                    "audioUrl": "http://example.test/recording.m4a",
                },
            }
        )

        with self.assertRaises(AIDENOTE.AideNoteError) as caught:
            AIDENOTE.audio_url(client, argparse.Namespace(file_id="recording-123"))

        self.assertEqual(caught.exception.code, "invalid_response")

    def test_parser_requires_file_id(self):
        parser = AIDENOTE.build_parser()
        args = parser.parse_args(["audio-url", "--file-id", "recording-123"])

        self.assertEqual(args.command, "audio-url")
        self.assertEqual(args.file_id, "recording-123")


if __name__ == "__main__":
    unittest.main()
