from pathlib import Path


DEFAULT_ENV_FILE = Path(__file__).with_name(".env")


def read_env(filename=None):
    values = {}
    env_file = DEFAULT_ENV_FILE if filename is None else Path(filename)

    with env_file.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")

    return values


env = read_env()

whatsapp_token = env.get("WHATSAPP_TOKEN")
erpnext_api_key = env.get("ERPNEXT_API_KEY")
erpnext_api_secret = env.get("ERPNEXT_API_SECRET")
erpnext_url = env.get("ERPNEXT_URL")
gemini = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY")

erpnext_local= env.get("ERPNEXT_local")
erpnext_local_key = env.get("ERPNEXT_LOCAL_KEY")
erpnext_local_secret = env.get("ERPNEXT_LOCAL_SECRET")