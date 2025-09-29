from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple, Any
import pathlib
import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

def _to_ndarray(x: Any) -> np.ndarray:
    a = np.array(x, dtype=int)
    if a.ndim != 2:
        raise ValueError("matrix must be 2D")
    return a

def _fmt_array(a: np.ndarray) -> str:
    return "\n".join(" ".join(str(int(v)) for v in row) for row in a)

@dataclass(frozen=True)
class MatrixSimple:
    data: np.ndarray

    @classmethod
    def from_iter(cls, it: Iterable[Iterable[int]]) -> "MatrixSimple":
        return cls(_to_ndarray(it))

    @property
    def shape(self) -> Tuple[int, int]:
        return tuple(self.data.shape)

    def __add__(self, other: "MatrixSimple") -> "MatrixSimple":
        if self.shape != other.shape:
            raise ValueError("shape mismatch for +")
        return MatrixSimple(self.data + other.data)

    def __mul__(self, other: "MatrixSimple") -> "MatrixSimple":
        if self.shape != other.shape:
            raise ValueError("shape mismatch for * (elementwise)")
        return MatrixSimple(self.data * other.data)

    def __matmul__(self, other: "MatrixSimple") -> "MatrixSimple":
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("inner dimensions mismatch for @")
        return MatrixSimple(self.data @ other.data)

    def to_text(self) -> str:
        return _fmt_array(self.data)

    def __str__(self) -> str:
        return f"MatrixSimple(shape={self.shape})\n" + self.to_text()

class FileMixin:
    def save_txt(self, path: str | pathlib.Path) -> None:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(_fmt_array(self._data), encoding="utf-8")

class StrMixin:
    def __str__(self) -> str:
        return _fmt_array(self._data)

class PropertiesMixin:
    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, value):
        self._data = _to_ndarray(value)

    @property
    def shape(self) -> Tuple[int, int]:
        return tuple(self._data.shape)

class NumMatrix(NDArrayOperatorsMixin, FileMixin, StrMixin, PropertiesMixin):
    __array_priority__ = 1000

    def __init__(self, data):
        self._data = _to_ndarray(data)

    def __array__(self, dtype=None):
        return self._data if dtype is None else self._data.astype(dtype)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        conv = lambda x: x._data if isinstance(x, NumMatrix) else x
        out = getattr(ufunc, method)(*(conv(x) for x in inputs), **kwargs)
        if isinstance(out, tuple):
            return tuple(self.__class__(x) if isinstance(x, np.ndarray) else x for x in out)
        return self.__class__(out) if isinstance(out, np.ndarray) else out

    def __matmul__(self, other):
        other_arr = other._data if isinstance(other, NumMatrix) else _to_ndarray(other)
        return self.__class__(self._data @ other_arr)

_MATMUL_CACHE: dict[tuple[int, int], "HashMatrix"] = {}

class HashMixin:
    def __hash__(self) -> int:
        # Простейшая хэш‑функция для матрицы:
        # сумма всех элементов по модулю 97.
        # Намеренно слабая (легко получить коллизии),
        # но не константная, что удовлетворяет условию задания.
        return int(self._data.sum()) % 97

class HashMatrix(HashMixin, NumMatrix):
    def __matmul__(self, other):
        other_arr = other._data if isinstance(other, NumMatrix) else _to_ndarray(other)
        key = (hash(self), int(other_arr.sum()) % 97 if not isinstance(other, HashMatrix) else hash(other))
        if key in _MATMUL_CACHE:
            return _MATMUL_CACHE[key]
        result = self.__class__(self._data @ other_arr)
        _MATMUL_CACHE[key] = result
        return result

    def true_matmul(self, other):
        other_arr = other._data if isinstance(other, NumMatrix) else _to_ndarray(other)
        return self.__class__(self._data @ other_arr)