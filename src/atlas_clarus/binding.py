"""Normative ATLAS Clarus RGB-only binding primitives.

Source identity is selected exclusively by integer squared distance in
documented 8-bit sRGB. Lab, Delta E, Delta lambda, ICC data, and production
conditions cannot influence ``source_atlas_row_id``.
"""

from __future__ import annotations

import ast
import hashlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

EXPECTED_MASTER_FILENAME = "atlas_master__active_master__v2_illumext.pkl"
EXPECTED_MASTER_SHA256 = "8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4"
EXPECTED_MASTER_ROWS = 13_283
DELTA_LAMBDA_TOLERANCE_NM = 0.001

POSTHOC_MODE = "RGB_ONLY_DLambda_POSTHOC"
ACTIVE_MODE = "RGB_ONLY_DLambda_ACTIVE_PRODUCTION_SELECTION"


class MasterValidationError(ValueError):
    """Raised when a master does not satisfy the frozen contract."""


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _rgb_tuple(value: Any) -> tuple[int, int, int]:
    if isinstance(value, str):
        value = ast.literal_eval(value)
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise MasterValidationError(f"Invalid RGB value: {value!r}")
    rgb = tuple(int(channel) for channel in value)
    if any(channel < 0 or channel > 255 for channel in rgb):
        raise MasterValidationError(f"RGB channel outside 0..255: {rgb!r}")
    return rgb


def _input_rgb(value: Sequence[int]) -> tuple[int, int, int]:
    if len(value) != 3 or any(isinstance(channel, bool) for channel in value):
        raise ValueError("RGB input must contain exactly three integer channels")
    if any(not isinstance(channel, int) or channel < 0 or channel > 255 for channel in value):
        raise ValueError("RGB input channels must be integers in the range 0..255")
    return tuple(value)


@dataclass(frozen=True)
class AtlasMaster:
    frame: pd.DataFrame
    sha256: str
    source_path: Path | None = None

    @classmethod
    def load(cls, path: str | Path) -> "AtlasMaster":
        source = Path(path)
        digest = sha256_file(source)
        if digest != EXPECTED_MASTER_SHA256:
            raise MasterValidationError(
                f"Master SHA-256 mismatch: expected {EXPECTED_MASTER_SHA256}, got {digest}"
            )
        frame = pd.read_pickle(source)
        master = cls(frame=frame, sha256=digest, source_path=source)
        master.validate(require_frozen_contract=True)
        return master

    @classmethod
    def from_records(cls, records: Iterable[Mapping[str, Any]]) -> "AtlasMaster":
        frame = pd.DataFrame.from_records(records)
        master = cls(frame=frame, sha256="SYNTHETIC_TEST_MASTER")
        master.validate(require_frozen_contract=False)
        return master

    def validate(self, *, require_frozen_contract: bool) -> None:
        if not isinstance(self.frame, pd.DataFrame):
            raise MasterValidationError("Master must be a pandas DataFrame")
        required = {"reference", "rgb", "lambda_v2_nm", "lambda_ee_nm", "delta_lambda_nm"}
        missing = sorted(required.difference(self.frame.columns))
        if missing:
            raise MasterValidationError(f"Missing required columns: {', '.join(missing)}")
        if not self.frame.index.is_unique:
            raise MasterValidationError("DataFrame index must be unique; it is the atlas_row_id")
        if self.frame["reference"].isna().any() or not self.frame["reference"].is_unique:
            raise MasterValidationError("References must be present and unique")
        for value in self.frame["rgb"]:
            _rgb_tuple(value)
        for row_id, row in self.frame.iterrows():
            try:
                lambda_v2 = float(row["lambda_v2_nm"])
                lambda_ee = float(row["lambda_ee_nm"])
                delta_lambda = float(row["delta_lambda_nm"])
            except (TypeError, ValueError) as error:
                raise MasterValidationError(
                    f"Non-numeric lambda value at atlas_row_id {row_id}"
                ) from error
            if not all(math.isfinite(value) for value in (lambda_v2, lambda_ee, delta_lambda)):
                raise MasterValidationError(
                    f"Non-finite lambda value at atlas_row_id {row_id}"
                )
            expected_delta = lambda_v2 - lambda_ee
            if not math.isclose(
                delta_lambda, expected_delta, rel_tol=0.0,
                abs_tol=DELTA_LAMBDA_TOLERANCE_NM,
            ):
                raise MasterValidationError(
                    "delta_lambda_nm mismatch at atlas_row_id "
                    f"{row_id}: expected {expected_delta}, got {delta_lambda}"
                )
        if require_frozen_contract:
            if len(self.frame) != EXPECTED_MASTER_ROWS:
                raise MasterValidationError(
                    f"Master row count mismatch: expected {EXPECTED_MASTER_ROWS}, got {len(self.frame)}"
                )
            expected_index = pd.RangeIndex(0, EXPECTED_MASTER_ROWS)
            if not self.frame.index.equals(expected_index):
                raise MasterValidationError("Frozen master index must be RangeIndex(0, 13283)")


@dataclass(frozen=True)
class BindingResult:
    input_rgb: tuple[int, int, int]
    source_atlas_row_id: int
    production_atlas_row_id: int
    reference_variant: str
    source_rgb_distance_squared: int
    source_reference: str
    production_reference: str
    source_rgb: tuple[int, int, int]
    production_rgb: tuple[int, int, int]
    source_delta_lambda_nm: float
    production_delta_lambda_nm: float
    master_sha256: str

    def to_record(self) -> dict[str, Any]:
        return {
            "schema_id": "ATLAS_CLARUS_BINDING_RECORD_V0_1_0",
            "input_basis": "documented 8-bit sRGB",
            "input_rgb": list(self.input_rgb),
            "reference_variant": self.reference_variant,
            "source_atlas_row_id": self.source_atlas_row_id,
            "production_atlas_row_id": self.production_atlas_row_id,
            "source_rgb_distance_squared": self.source_rgb_distance_squared,
            "source_reference": self.source_reference,
            "production_reference": self.production_reference,
            "source_rgb": list(self.source_rgb),
            "production_rgb": list(self.production_rgb),
            "source_delta_lambda_nm": self.source_delta_lambda_nm,
            "production_delta_lambda_nm": self.production_delta_lambda_nm,
            "master_sha256": self.master_sha256,
            "deltaE_stage": "POSTHOC_ONLY",
            "deltaE_influenced_source_identity": False,
            "deltaE_influenced_production_selection": False,
        }


class AtlasBinder:
    def __init__(self, master: AtlasMaster):
        self.master = master

    def bind(self, rgb: Sequence[int], *, mode: str = POSTHOC_MODE) -> BindingResult:
        source_rgb = _input_rgb(rgb)
        ranked: list[tuple[int, int]] = []
        for row_id, value in self.master.frame["rgb"].items():
            atlas_rgb = _rgb_tuple(value)
            distance = sum((left - right) ** 2 for left, right in zip(source_rgb, atlas_rgb))
            ranked.append((distance, int(row_id)))
        ranked.sort(key=lambda item: (item[0], item[1]))
        source_distance, source_id = ranked[0]

        if mode == POSTHOC_MODE:
            production_id = source_id
        elif mode == ACTIVE_MODE:
            top_two = ranked[:2]
            production_id = min(
                (row_id for _, row_id in top_two),
                key=lambda row_id: (
                    abs(float(self.master.frame.loc[row_id, "delta_lambda_nm"])),
                    row_id,
                ),
            )
        else:
            raise ValueError(f"Unsupported reference variant: {mode}")

        source_row = self.master.frame.loc[source_id]
        production_row = self.master.frame.loc[production_id]
        return BindingResult(
            input_rgb=source_rgb,
            source_atlas_row_id=source_id,
            production_atlas_row_id=production_id,
            reference_variant=mode,
            source_rgb_distance_squared=source_distance,
            source_reference=str(source_row["reference"]),
            production_reference=str(production_row["reference"]),
            source_rgb=_rgb_tuple(source_row["rgb"]),
            production_rgb=_rgb_tuple(production_row["rgb"]),
            source_delta_lambda_nm=float(source_row["delta_lambda_nm"]),
            production_delta_lambda_nm=float(production_row["delta_lambda_nm"]),
            master_sha256=self.master.sha256,
        )
