import requests
from pathlib import Path
from security import read_env

env = read_env()

def whatsapp_send_file(to_number, file_path, message=""):
    send_url = "https://api.11za.in/apis/sendMessage/sendMessages"

    candidate = Path(file_path)
    if not candidate.exists():
        project_root = Path(__file__).resolve().parent
        legacy_candidate = project_root / candidate.name
        if legacy_candidate.exists():
            candidate = legacy_candidate
        else:
            matches = list(project_root.rglob(candidate.name))
            if matches:
                candidate = matches[0]
            else:
                raise FileNotFoundError(f"File not found: {file_path}")

    clean_number = "".join(char for char in str(to_number) if char.isdigit())

    if len(clean_number) == 10:
        clean_number = "91" + clean_number

    payload = {
        "authToken": env.get("WHATSAPP_TOKEN"),
        "sendto": clean_number,
        "originWebsite": env.get("WHATSAPP_ORIGIN_WEBSITE"),
        "contentType": "document",
        "text": message,
    }

    with open(candidate, "rb") as excel_file:
        files = {
            "myfile": (
                candidate.name,
                excel_file,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }

        response = requests.post(
            send_url,
            data=payload,
            files=files,
            timeout=30,
        )

    # print("Status:", response.status_code)

    try:
        # print(response.json())
        return response.json()
    except ValueError:
        print(response.text)
        return response.text


# whatsapp_send_file(
#     "8140021166",
#     r"D:\test\Gopi_Vaid_(Mumbai)_report.xlsx",
#     "Hello, Excel file attached."
# )

