import os
import sys

from dotenv import load_dotenv


def mask_secret(secret: str) -> str:
    prefix = secret[:3]
    return f"{prefix}**"


def main() -> int:
    load_dotenv()
    secret = os.getenv("APP_SECRET")

    if not secret:
        print("Error: APP_SECRET is not set.")
        return 1

    print(f"System started. Secret hash: {mask_secret(secret)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
