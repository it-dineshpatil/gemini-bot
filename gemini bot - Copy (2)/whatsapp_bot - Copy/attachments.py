
import os

import requests
from security import (
    erpnext_local,
    erpnext_local_key,
    erpnext_local_secret
)
target_doctype = "Issue"
base_url = erpnext_local

def attach_files(docname, audio_path):
    if audio_path:
        # audio_path = f"r{audio_path}"
        if not os.path.exists(audio_path):
            print(f"File not found: {audio_path}")
        else:
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

            file_url = uploaded_file.get("file_url")
            return file_url
        
print(attach_files("ISS-2026-00024", r"audio_file\918140021166.mp3"))