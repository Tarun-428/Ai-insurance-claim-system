import asyncio
import os
import json
from pathlib import Path

from dotenv import load_dotenv

# Import your existing services
from backend.services.ocr_service import extract_text_from_file
from backend.services.ai_service import analyze_claim_with_ai


# ---------- CONFIGURE YOUR TEST FILES HERE ----------
# Put 3–4 absolute or relative paths to your bill/report images or PDFs
FILE_PATHS = [
    r"samples\report1.jpg",
    r"samples\bill2.png",
    r"samples\report2.jpg",
    # r"D:\Ai Insurance Claim\samples\report2.jpg",
]


async def main():
    # Load .env (same as server.py)
    ROOT_DIR = Path(__file__).resolve().parent
    load_dotenv(ROOT_DIR / ".env")

    print("🔑 OPENROUTER_API_KEY present?:", "YES" if os.environ.get("OPENROUTER_API_KEY") else "NO")

    extracted_texts = []

    print("\n===== 🧾 OCR PHASE =====")
    for path_str in FILE_PATHS:
        path = Path(path_str)
        if not path.exists():
            print(f"⚠ [OCR] File not found: {path}")
            continue

        print(f"\n[OCR] Extracting text from: {path}")
        text = extract_text_from_file(str(path))
        print(f"[OCR] Extracted {len(text)} characters from {path.name}")
        # Optionally preview small part
        preview = text[:200].replace("\n", " ")
        print(f"[OCR] Preview: {preview}...")
        extracted_texts.append(text)

    if not extracted_texts:
        print("\n❌ No texts extracted from any files. Check paths & formats.")
        return

    print("\n===== 📄 DUMMY CLAIM DATA =====")
    # Dummy claim – edit these to test different scenarios
    claim_data = {
        "id": "test-claim-001",
        "insurance id":"POL01",
        "hospital_name": "Suyash Hospital",
        "date_of_admission": "2025-11-20",
        "disease_description": "High fever and dengue-like symptoms, admitted for observation.",
        "total_claim_amount": 50000,
        "aadhar_no": "1234-5678-9012",
    }
    print(json.dumps(claim_data, indent=2))

    print("\n===== 🤖 AI ANALYSIS (OpenRouter) =====")
    result = await analyze_claim_with_ai(claim_data, extracted_texts)

    print("\n===== ✅ AI RESULT =====")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
