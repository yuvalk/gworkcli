#!/usr/bin/env python3
"""Upload a Markdown file as a Google Doc."""

import argparse
import os
import sys
from io import BytesIO
from pathlib import Path

import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SCRIPT_DIR = Path(__file__).resolve().parent
TOKEN_PATH = SCRIPT_DIR / "token.json"
CREDENTIALS_PATH = SCRIPT_DIR / "credentials.json"


def authenticate():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=8085, open_browser=False)
        TOKEN_PATH.write_text(creds.to_json())
    return creds


def upload(md_path):
    md_text = md_path.read_text()
    html = markdown.markdown(md_text)
    title = md_path.stem
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped:
            if stripped.startswith("#"):
                title = stripped.lstrip("#").strip()
            break

    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
    }
    media = MediaIoBaseUpload(
        BytesIO(html.encode("utf-8")), mimetype="text/html", resumable=False
    )
    doc = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"https://docs.google.com/document/d/{doc['id']}/edit")


def main():
    parser = argparse.ArgumentParser(description="Upload a Markdown file as a Google Doc.")
    parser.add_argument("file", help="Path to the .md file to upload")
    args = parser.parse_args()

    md_path = Path(args.file)
    if not md_path.is_file():
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    upload(md_path)


if __name__ == "__main__":
    main()
