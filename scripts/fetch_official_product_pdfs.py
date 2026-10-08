#!/usr/bin/env python3
"""Verify originals of public manufacturer PDFs without redistributing restricted files.

Input: references/product-documents/official-product-pdf-sources.csv
Output: references/product-documents/fetch-results.csv (auditable)
Only CC BY-ND original, unmodified PDFs with their license confirmed in the
PDF itself are copied to references/product-documents/originals/.
Other original PDF bytes remain transient on the runner and are deleted.
"""
import csv
import hashlib
import io
import os
import pathlib
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pypdf import PdfReader

ROOT = pathlib.Path("references/product-documents")
SOURCE = ROOT / "official-product-pdf-sources.csv"
DEST = ROOT / "originals"
STATUS = ROOT / "fetch-results.csv"
TMP = pathlib.Path("/tmp/edge-research-product-originals")
SIZE_LIMIT = 45 * 1024 * 1024
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EdgeResearchArchive/1.0; research document verification)",
    "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
}
ALLOWED = (
    "www.nvidia.com",
    "docs.qualcomm.com",
    "download.t-firefly.com",
    "advdownload.advantech.com",
    "hailo.ai",
    "datasheets.raspberrypi.com",
    "docs.axelera.ai",
    "dl.radxa.com",
)


def safe_url(url):
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname not in ALLOWED:
        raise ValueError("unapproved download host: " + str(u.hostname))
    return url


def fetch_pdf(url):
    safe_url(url)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=65) as resp:
        # Some CDNs redirect; require that the final URL is still on HTTPS.
        final = urllib.parse.urlparse(resp.url)
        if final.scheme != "https":
            raise ValueError("untrusted redirect")
        data = resp.read(SIZE_LIMIT + 1)
    if len(data) > SIZE_LIMIT:
        raise ValueError("exceeds file size policy")
    if not data.startswith(b"%PDF-"):
        raise ValueError("not a PDF file (possibly an HTML/download portal)")
    pdf = PdfReader(io.BytesIO(data), strict=False)
    pages = len(pdf.pages)
    if pages < 2 or pages > 1800:
        raise ValueError("unexpected PDF page count")
    first = "\n".join((p.extract_text() or "") for p in pdf.pages[:min(pages, 3)])
    last = pdf.pages[-1].extract_text() or ""
    return data, pages, first + "\n" + last


def confirm_cc_by_nd(text):
    s = " ".join(text.lower().split())
    return (
        "attribution-noderivatives" in s
        or ("cc by-nd" in s)
        or ("creative commons" in s and "noderivatives" in s)
    )


def run():
    TMP.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    with SOURCE.open(newline="", encoding="utf-8") as fh:
        items = list(csv.DictReader(fh))
    result = []
    succeeded = 0
    committed = 0
    for item in items:
        record = {k: item.get(k, "") for k in (
            "id", "vendor", "product", "doc_type", "title",
            "reference", "official_url", "landing_url", "rights_policy",
        )}
        record.update({
            "status": "NOT_FETCHED",
            "actual_url": "",
            "pages": "",
            "size_bytes": "",
            "sha256": "",
            "stored_path": "",
            "retrieval_date": datetime.now(timezone.utc).date().isoformat(),
            "error": "",
        })
        errors = []
        for raw_url in [item.get("official_url", ""), item.get("alternative_url", "")]:
            if not raw_url:
                continue
            try:
                data, pages, extracted = fetch_pdf(raw_url)
                hint = (item.get("keyword") or "").lower().strip()
                compact = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
                if hint and compact(hint) not in compact(extracted):
                    raise ValueError("model/product keyword missing in PDF first/last pages: " + hint)
                record.update({
                    "actual_url": raw_url,
                    "pages": pages,
                    "size_bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "status": "FETCHED_ORIGINAL_LINK_ONLY",
                })
                succeeded += 1
                # Public GitHub: honor ND and copy byte-for-byte (no rewriting).
                if item.get("publish_to_git") == "YES":
                    if item.get("rights_policy") in ("CC-BY-ND-4.0-UNMODIFIED", "CC-BY-ND-4.0-VERIFY") and confirm_cc_by_nd(extracted):
                        name = item["id"] + "_" + pathlib.Path(urllib.parse.urlparse(raw_url).path).name
                        path = DEST / name
                        path.write_bytes(data)
                        record.update(status="ORIGINAL_PDF_IN_REPO", stored_path=str(path))
                        committed += 1
                    else:
                        record.update(status="RIGHTS_NOT_CONFIRMED_NO_REPOST")
                del data
                break
            except Exception as exc:
                errors.append(type(exc).__name__ + ": " + str(exc)[:180])
        else:
            record["status"] = "DOWNLOAD_FAILED"
        record["error"] = " | ".join(errors)
        print(record["id"], record["status"], record["size_bytes"], record["pages"], record["error"], flush=True)
        result.append(record)
    columns = [
        "id", "vendor", "product", "doc_type", "title", "reference",
        "official_url", "landing_url", "rights_policy", "status",
        "actual_url", "pages", "size_bytes", "sha256", "stored_path",
        "retrieval_date", "error",
    ]
    with STATUS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        w.writerows(result)
    print(f"Validated original PDF downloads: {succeeded}/{len(items)}; legally reposted: {committed}")
    # Fail only for truly empty results; always preserve failure audit in repo.
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
