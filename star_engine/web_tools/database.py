"""
Star Web Tools — Fluent Database ORM & Query Builder (PDO / Eloquent style)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional, Union


class QueryBuilder:
    """Fluent SQL & In-Memory Query Builder."""

    def __init__(self, db: "Database", table_name: str):
        self.db = db
        self.table_name = table_name
        self._select_cols = ["*"]
        self._wheres: List[Dict[str, Any]] = []
        self._order_by: Optional[str] = None
        self._limit_val: Optional[int] = None
        self._offset_val: Optional[int] = None

    def _clone(self) -> "QueryBuilder":
        qb = QueryBuilder(self.db, self.table_name)
        qb._select_cols = list(self._select_cols)
        qb._wheres = list(self._wheres)
        qb._order_by = self._order_by
        qb._limit_val = self._limit_val
        qb._offset_val = self._offset_val
        return qb

    def select(self, *cols: str) -> "QueryBuilder":
        qb = self._clone()
        qb._select_cols = list(cols) if cols else ["*"]
        return qb

    def where(self, col: str, *args) -> "QueryBuilder":
        qb = self._clone()
        if len(args) == 1:
            op = "="
            val = args[0]
        elif len(args) >= 2:
            op = args[0]
            val = args[1]
        else:
            op = "="
            val = None
        qb._wheres.append({"col": col, "op": op, "val": val})
        return qb

    def order_by(self, col: str, direction: str = "asc") -> "QueryBuilder":
        qb = self._clone()
        qb._order_by = f"{col} {direction.upper()}"
        return qb

    def limit(self, n: int) -> "QueryBuilder":
        qb = self._clone()
        qb._limit_val = n
        return qb

    def offset(self, n: int) -> "QueryBuilder":
        qb = self._clone()
        qb._offset_val = n
        return qb

    def get(self) -> List[Dict[str, Any]]:
        # Check if in-memory driver
        if self.db.is_in_memory:
            return self._execute_memory_query()

        # Build SQLite query
        cols = ", ".join(self._select_cols)
        query = f"SELECT {cols} FROM {self.table_name}"
        params: List[Any] = []

        if self._wheres:
            conds = []
            for w in self._wheres:
                conds.append(f"{w['col']} {w['op']} ?")
                params.append(w["val"])
            query += " WHERE " + " AND ".join(conds)

        if self._order_by:
            query += f" ORDER BY {self._order_by}"

        if self._limit_val is not None:
            query += f" LIMIT {self._limit_val}"
            if self._offset_val is not None:
                query += f" OFFSET {self._offset_val}"

        cursor = self.db.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        return [dict(zip(col_names, row)) for row in rows]

    def first(self) -> Optional[Dict[str, Any]]:
        old_limit = self._limit_val
        self._limit_val = 1
        res = self.get()
        self._limit_val = old_limit
        return res[0] if res else None

    def count(self) -> int:
        if self.db.is_in_memory:
            return len(self._execute_memory_query())
        res = self.select("COUNT(*) as c").first()
        return res["c"] if res and "c" in res else 0

    def insert(self, record: Dict[str, Any]) -> int:
        if self.db.is_in_memory:
            table = self.db.memory_tables.setdefault(self.table_name, [])
            rec = dict(record)
            if "id" not in rec:
                rec["id"] = len(table) + 1
            table.append(rec)
            return rec["id"]

        cols = list(record.keys())
        placeholders = ", ".join(["?"] * len(cols))
        query = f"INSERT INTO {self.table_name} ({', '.join(cols)}) VALUES ({placeholders})"
        cursor = self.db.connection.cursor()
        cursor.execute(query, list(record.values()))
        self.db.connection.commit()
        return cursor.lastrowid or 1

    def update(self, updates: Dict[str, Any]) -> int:
        if self.db.is_in_memory:
            count = 0
            for row in self._execute_memory_query():
                row.update(updates)
                count += 1
            return count

        sets = [f"{k} = ?" for k in updates.keys()]
        query = f"UPDATE {self.table_name} SET {', '.join(sets)}"
        params = list(updates.values())

        if self._wheres:
            conds = []
            for w in self._wheres:
                conds.append(f"{w['col']} {w['op']} ?")
                params.append(w["val"])
            query += " WHERE " + " AND ".join(conds)

        cursor = self.db.connection.cursor()
        cursor.execute(query, params)
        self.db.connection.commit()
        return cursor.rowcount

    def delete(self) -> int:
        if self.db.is_in_memory:
            matched = self._execute_memory_query()
            table = self.db.memory_tables.setdefault(self.table_name, [])
            for r in matched:
                if r in table:
                    table.remove(r)
            return len(matched)

        query = f"DELETE FROM {self.table_name}"
        params: List[Any] = []
        if self._wheres:
            conds = []
            for w in self._wheres:
                conds.append(f"{w['col']} {w['op']} ?")
                params.append(w["val"])
            query += " WHERE " + " AND ".join(conds)

        cursor = self.db.connection.cursor()
        cursor.execute(query, params)
        self.db.connection.commit()
        return cursor.rowcount

    def _execute_memory_query(self) -> List[Dict[str, Any]]:
        rows = self.db.memory_tables.get(self.table_name, [])
        filtered = []
        for r in rows:
            match = True
            for w in self._wheres:
                val = r.get(w["col"])
                target = w["val"]
                op = w["op"]
                if op == "=" and val != target:
                    match = False
                elif op == "!=" and val == target:
                    match = False
                elif op == ">" and not (val is not None and val > target):
                    match = False
                elif op == "<" and not (val is not None and val < target):
                    match = False
                elif op == ">=" and not (val is not None and val >= target):
                    match = False
                elif op == "<=" and not (val is not None and val <= target):
                    match = False
            if match:
                filtered.append(r)

        if self._order_by:
            parts = self._order_by.split()
            col = parts[0]
            reverse = len(parts) > 1 and parts[1].lower() == "desc"
            filtered.sort(key=lambda x: x.get(col, 0), reverse=reverse)

        if self._offset_val is not None:
            filtered = filtered[self._offset_val:]
        if self._limit_val is not None:
            filtered = filtered[:self._limit_val]

        return filtered


class Database:
    """Universal Database Manager supporting in-memory and SQLite backends."""

    def __init__(self, connection_string: str = ":memory:"):
        self.connection_string = connection_string
        self.is_in_memory = (connection_string == ":memory:")
        self.memory_tables: Dict[str, List[Dict[str, Any]]] = {}
        if not self.is_in_memory:
            self.connection = sqlite3.connect(connection_string, check_same_thread=False)
        else:
            self.connection = sqlite3.connect(":memory:", check_same_thread=False)

    def table(self, table_name: str) -> QueryBuilder:
        return QueryBuilder(self, table_name)

    def raw(self, sql: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor()
        cursor.execute(sql, params or [])
        if sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP")):
            self.connection.commit()
            return [{"affected_rows": cursor.rowcount}]
        rows = cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        return [dict(zip(col_names, row)) for row in rows]

    def close(self):
        self.connection.close()
