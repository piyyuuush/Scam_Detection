"""
@design-guard
role: Downloads raw datasets into data/raw/<dataset_id>/ and writes SOURCE.json with attribution.
layer: service
non_goals:
- Parsing datasets into features; that is done by dataset loaders.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [HttpDatasetDownloader]
invariants:
- Raw data is stored under data/raw and never committed to git.
authority:
decides: [download URLs and provenance metadata shape]
delegates: [parsing to loaders; orchestration to UI/facade]
extension_policy:
- Add new datasets by adding URL metadata and download steps here.
failure_contract:
- Raise ValueError for unknown dataset ids; OSError/network errors bubble up.
testing_contract:
- Unit: unknown dataset raises ValueError; integration tests avoid network by using fixtures.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZipFile

import httpx


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_to_path(*, url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with (
        httpx.Client(
            follow_redirects=True,
            timeout=httpx.Timeout(60.0, read=300.0),
        ) as client,
        client.stream("GET", url) as r,
        path.open("wb") as f,
    ):
        r.raise_for_status()
        for chunk in r.iter_bytes():
            f.write(chunk)


def _write_source_json(*, out_dir: Path, payload: dict[str, object]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "SOURCE.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


@dataclass(frozen=True)
class HttpDatasetDownloader:
    data_dir: Path

    def download(self, *, dataset_id: str) -> None:
        raw_root = self.data_dir / "raw"
        downloaded_at_utc = datetime.now(tz=UTC).isoformat()

        if dataset_id == "nsl_kdd":
            out_dir = raw_root / "nsl_kdd"
            train_url = (
                "https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTrain%2B.txt"
            )
            test_url = (
                "https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTest%2B.txt"
            )

            train_path = out_dir / "KDDTrain+.txt"
            test_path = out_dir / "KDDTest+.txt"
            _download_to_path(url=train_url, path=train_path)
            _download_to_path(url=test_url, path=test_path)

            _write_source_json(
                out_dir=out_dir,
                payload={
                    "dataset_id": "nsl_kdd",
                    "name": "NSL-KDD",
                    "task": "intrusion_detection_binary",
                    "downloaded_at_utc": downloaded_at_utc,
                    "source_urls": [train_url, test_url],
                    "attribution": "NSL-KDD dataset. See UNB CIC NSL-KDD dataset page for citation.",
                    "checksums_sha256": {
                        train_path.name: _sha256_file(train_path),
                        test_path.name: _sha256_file(test_path),
                    },
                },
            )
            return

        if dataset_id == "phiusiil":
            out_dir = raw_root / "phiusiil"
            zip_url = (
                "https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip"
            )
            zip_path = out_dir / "phiusiil.zip"
            _download_to_path(url=zip_url, path=zip_path)

            out_dir.mkdir(parents=True, exist_ok=True)
            csv_candidates: list[str] = []
            with ZipFile(zip_path) as zf:
                for name in zf.namelist():
                    if name.lower().endswith(".csv"):
                        csv_candidates.append(name)
                if not csv_candidates:
                    raise ValueError("PhiUSIIL zip did not contain a CSV file.")

                chosen = sorted(csv_candidates)[0]
                extracted = zf.extract(chosen, path=out_dir)
                extracted_path = Path(extracted)

            csv_path = out_dir / "phiusiil.csv"
            extracted_path.replace(csv_path)

            _write_source_json(
                out_dir=out_dir,
                payload={
                    "dataset_id": "phiusiil",
                    "name": "PhiUSIIL Phishing URL Dataset (UCI)",
                    "task": "phishing_detection_binary",
                    "downloaded_at_utc": downloaded_at_utc,
                    "source_urls": [zip_url],
                    "license": "CC BY 4.0 (per UCI listing)",
                    "checksums_sha256": {csv_path.name: _sha256_file(csv_path)},
                },
            )
            return

        raise ValueError(f"Unknown dataset_id '{dataset_id}'.")
