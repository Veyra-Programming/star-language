"""
Star OmniEngine 2.0 GN — Unified Arena Allocator & Zero-Copy Borrowed Buffers
Authoritative Reference: STAR_OMNI_SPEC.md
"""

from typing import Dict, Any, Optional, List, Union


class BorrowedBuffer:
    """
    Zero-copy borrowed view into contiguous memory.
    Provides sub-slice slicing and SIMD alignment without copying underlying buffers.
    """
    def __init__(self, raw_data: Union[bytearray, bytes], offset: int = 0, length: Optional[int] = None):
        self._raw = raw_data
        self.offset = offset
        self.length = length if length is not None else (len(raw_data) - offset)
        if self.offset + self.length > len(self._raw):
            raise ValueError(f"Slice out of bounds: offset {self.offset} + length {self.length} > total {len(self._raw)}")

    def view(self) -> memoryview:
        return memoryview(self._raw)[self.offset : self.offset + self.length]

    def slice(self, start: int, end: Optional[int] = None) -> "BorrowedBuffer":
        if end is None:
            end = self.length
        if start < 0 or end > self.length or start > end:
            raise IndexError("Slice index out of bounds")
        return BorrowedBuffer(self._raw, offset=self.offset + start, length=end - start)

    def to_bytes(self) -> bytes:
        return bytes(self.view())

    def to_text(self, encoding: str = "utf-8") -> str:
        return self.to_bytes().decode(encoding, errors="replace")

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, idx: int) -> int:
        if idx < 0 or idx >= self.length:
            raise IndexError("Index out of bounds")
        return self._raw[self.offset + idx]

    def __setitem__(self, idx: int, val: int):
        if not isinstance(self._raw, bytearray):
            raise TypeError("Cannot mutate immutable BorrowedBuffer")
        if idx < 0 or idx >= self.length:
            raise IndexError("Index out of bounds")
        self._raw[self.offset + idx] = val & 0xFF


class ArenaAllocator:
    """
    High-performance bump-pointer Arena Allocator.
    Performs O(1) memory allocations with zero fragmentation and instant frame reset.
    Eliminates GC pressure for ephemeral requests, frame loops, and streaming pipelines.
    """
    def __init__(self, capacity_bytes: int = 1024 * 1024):  # Default 1MB
        self.capacity = capacity_bytes
        self._buffer = bytearray(self.capacity)
        self.cursor = 0
        self.high_watermark = 0
        self.allocation_count = 0

    def alloc(self, size: int) -> BorrowedBuffer:
        """Bump-pointer allocation. O(1) constant time."""
        # Align to 8-byte boundary for SIMD efficiency
        aligned_size = (size + 7) & ~7
        if self.cursor + aligned_size > self.capacity:
            raise MemoryError(f"Arena capacity exceeded: requested {aligned_size}B, remaining {self.capacity - self.cursor}B")

        alloc_offset = self.cursor
        self.cursor += aligned_size
        if self.cursor > self.high_watermark:
            self.high_watermark = self.cursor

        self.allocation_count += 1
        return BorrowedBuffer(self._buffer, offset=alloc_offset, length=size)

    def alloc_text(self, text: str, encoding: str = "utf-8") -> BorrowedBuffer:
        raw = text.encode(encoding)
        buf = self.alloc(len(raw))
        buf.view()[:] = raw
        return buf

    def reset(self):
        """Instant O(1) reset of entire arena without GC overhead."""
        self.cursor = 0
        self.allocation_count = 0

    def stats(self) -> Dict[str, Any]:
        return {
            "capacity_kb": self.capacity // 1024,
            "used_bytes": self.cursor,
            "high_watermark_bytes": self.high_watermark,
            "allocations": self.allocation_count,
            "utilization_pct": round((self.cursor / self.capacity) * 100, 2),
        }
