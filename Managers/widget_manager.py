from typing import List, Optional, Any
from textual.screen import Screen
from textual.widgets import DataTable


def populate_table(screen: Screen, table_id: str, data: List[List[str]]):
    table = screen.query_one(f'#{table_id}', DataTable)
    table.clear()
    table.columns.clear()
    table.add_columns(*data[0])
    table.add_rows(data[1:])

def get_selected_table_row(screen: Screen, table_id: str) -> Optional[List[str]]:
    table = screen.query_one(f'#{table_id}', DataTable)
    coordinate = table.cursor_coordinate
    if coordinate:
        row, _ = coordinate
        return table.get_row_at(row)
    return None

def get_selected_table_cell(screen: Screen, table_id: str) -> Optional[str]:
    table = screen.query_one(f'#{table_id}', DataTable)
    coordinate = table.cursor_coordinate
    if coordinate:
        return table.get_cell_at(coordinate)
    return None

def add_table_row(screen: Screen, table_id: str, data: List[List[str]]) -> None:
    table = screen.query_one(f'#{table_id}', DataTable)
    table.add_rows(data)


def remove_table_row(screen: Screen, table_id: str) -> None:
    table = screen.query_one(f'#{table_id}', DataTable)
    coordinate = table.cursor_coordinate

    if coordinate:
        row_index, _ = coordinate
        row_keys = list(table.rows.keys())
        if 0 <= row_index < len(row_keys):
            row_key = row_keys[row_index]
            table.remove_row(row_key)
        else:
            raise IndexError("Row index out of range.")

def read_table_rows(screen: Screen, table_id: str) -> List[List[Any]]:
    table = screen.query_one(f'#{table_id}', DataTable)
    rows = []
    for index in range(len(table.rows)):
        rows.append(table.get_row_at(index))
    return rows





