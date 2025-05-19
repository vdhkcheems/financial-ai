import re

def load_company_descriptions(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by company block
    blocks = re.split(r"=== Company: (.+?) ===", content)
    result = {}

    # Blocks[0] is empty preamble, so zip blocks[1::2] and blocks[2::2]
    for company, block in zip(blocks[1::2], blocks[2::2]):
        sector_match = re.search(r"Sector:\s*(.+)", block)
        summary_match = re.search(r"Summary:\s*(.+)", block)
        highlights_match = re.findall(r"- (.+)", block)

        result[company.strip()] = {
            "sector": sector_match.group(1).strip() if sector_match else "Unknown",
            "summary": summary_match.group(1).strip() if summary_match else "",
            "highlights": highlights_match,
        }

    return result
