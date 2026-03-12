"""
@design-guard
role: Dataset loader implementations used by the registry.
layer: service
non_goals:
- Downloading datasets (separate capability).
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [NslKddDatasetLoader, PhiUsiilDatasetLoader, FixtureTabularDatasetLoader]
invariants:
- Loaders return binary labels and fixed feature ordering.
authority:
decides: [dataset-specific parsing and label mapping]
delegates: [preprocessing to preprocessing port]
extension_policy:
- Add new datasets as new loader implementations and register them in DatasetRegistry.
failure_contract:
- Raise FileNotFoundError when raw data files are missing.
testing_contract:
- Integration: fixture loader loads from local CSV in data/fixtures.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from cyberthreatdetect.ports.dataset_loader import TabularDataset

_NSL_KDD_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "label",
    "difficulty",
]


def _to_binary_label(series: pd.Series) -> np.ndarray:
    if series.dtype.kind in {"i", "u"}:
        arr = np.asarray(series.to_numpy(), dtype=np.int64)
        uniq = set(np.unique(arr).tolist())
        if uniq.issubset({0, 1}):
            return arr
        raise ValueError(f"Unsupported integer label values: {sorted(uniq)}")

    s = series.astype(str).str.strip().str.lower()
    if s.isin(["normal"]).any():
        return np.asarray((s != "normal").to_numpy(), dtype=np.int64)

    mapping_true = {"phishing", "phish", "malicious", "bad", "true", "1", "yes"}
    mapping_false = {"legitimate", "benign", "good", "false", "0", "no"}
    if s.isin(mapping_true | mapping_false).all():
        return np.asarray(s.isin(mapping_true).to_numpy(), dtype=np.int64)

    try:
        as_num = pd.to_numeric(series, errors="raise")
        return _to_binary_label(as_num)
    except Exception as e:
        raise ValueError("Could not map labels to binary {0,1}.") from e


def _ensure_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if out[col].dtype.kind not in {"i", "u", "f"}:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out.fillna(0.0)


@dataclass(frozen=True)
class NslKddDatasetLoader:
    data_dir: Path

    def load(self) -> TabularDataset:
        raw_dir = self.data_dir / "raw" / "nsl_kdd"
        train_path = raw_dir / "KDDTrain+.txt"
        test_path = raw_dir / "KDDTest+.txt"
        if not train_path.exists() or not test_path.exists():
            raise FileNotFoundError("NSL-KDD not downloaded yet. Use: ctd dataset download nsl_kdd")

        train_df = pd.read_csv(train_path, header=None, names=_NSL_KDD_COLUMNS)
        test_df = pd.read_csv(test_path, header=None, names=_NSL_KDD_COLUMNS)

        y_train = _to_binary_label(train_df["label"])
        y_test = _to_binary_label(test_df["label"])

        cat_cols = ["protocol_type", "service", "flag"]
        x_train_df = train_df.drop(columns=["label", "difficulty"])
        x_test_df = test_df.drop(columns=["label", "difficulty"])

        x_all = pd.concat([x_train_df, x_test_df], axis=0, ignore_index=True)
        x_all = pd.get_dummies(x_all, columns=cat_cols, drop_first=False)
        x_all = _ensure_numeric_features(x_all)

        x_train = x_all.iloc[: len(train_df)].to_numpy(dtype=np.float32)
        x_test = x_all.iloc[len(train_df) :].to_numpy(dtype=np.float32)
        feature_names = list(x_all.columns)

        return TabularDataset(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            feature_names=feature_names,
        )


@dataclass(frozen=True)
class PhiUsiilDatasetLoader:
    data_dir: Path

    def load(self) -> TabularDataset:
        raw_dir = self.data_dir / "raw" / "phiusiil"
        csv_path = raw_dir / "phiusiil.csv"
        if not csv_path.exists():
            raise FileNotFoundError(
                "PhiUSIIL not downloaded yet. Use: ctd dataset download phiusiil"
            )

        df = pd.read_csv(csv_path)
        label_candidates = [
            c
            for c in df.columns
            if c.strip().lower()
            in {"label", "class", "result", "target", "phishing", "is_phishing"}
        ]
        if not label_candidates:
            raise ValueError("Could not find label column in PhiUSIIL CSV.")
        label_col = label_candidates[0]

        y = _to_binary_label(df[label_col])
        x_df = df.drop(columns=[label_col])
        x_df = _ensure_numeric_features(x_df)

        x = x_df.to_numpy(dtype=np.float32)
        feature_names = list(x_df.columns)

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=1337, stratify=y
        )
        return TabularDataset(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            feature_names=feature_names,
        )


@dataclass(frozen=True)
class FixtureTabularDatasetLoader:
    data_dir: Path

    def load(self) -> TabularDataset:
        fixture_path = self.data_dir / "fixtures" / "tabular_binary.csv"
        if not fixture_path.exists():
            raise FileNotFoundError(
                f"Missing fixture file: {fixture_path}. In tests, pass --data-dir to point at a folder containing fixtures/."
            )

        df = pd.read_csv(fixture_path)
        if "label" not in df.columns:
            raise ValueError("Fixture dataset must have a 'label' column.")

        feature_cols = [c for c in df.columns if c != "label"]
        x = df[feature_cols].to_numpy(dtype=np.float32)
        y = df["label"].to_numpy(dtype=np.int64)

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=1337, stratify=y
        )
        return TabularDataset(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            feature_names=feature_cols,
        )
