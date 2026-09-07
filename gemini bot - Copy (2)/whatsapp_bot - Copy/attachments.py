
import os

import requests
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)
target_doctype = "Issue"
base_url = erpnext_local

def attach_files(docname, audio_path=None):
    if not audio_path:
        return None

    if not os.path.isfile(audio_path):
        print(f"File not found: {audio_path}")
        return None

    with open(audio_path, "rb") as audio_file:

        file_response = requests.post(
            f"{base_url}/api/method/upload_file",
            headers={
                "Authorization":
                    f"token {erpnext_local_key}:{erpnext_local_secret}"
            },
            files={
                "file": audio_file
            },
            data={
                "doctype": target_doctype,
                "docname": docname,
                "is_private": 1
            },
            timeout=60
        )

    file_response.raise_for_status()
    file_data = file_response.json()
    # print("File Upload Response:", file_data)

    uploaded_file = file_data.get("message", {})

    return uploaded_file.get("file_url")
        
# print(attach_files("ISS-2026-00024", "audio_file\918140021166.mp3"))