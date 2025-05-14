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

