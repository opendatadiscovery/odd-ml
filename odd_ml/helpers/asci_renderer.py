from pprint import pprint
from typing import List, Optional

from prettytable import PrettyTable


def show_table(
    field_names: List[str], rows: List[List[str]], title: Optional[str] = None
) -> None:
    tbl = PrettyTable(title=title)
    tbl.field_names = field_names
    tbl.align = "l"
    tbl.add_rows(rows)
    pprint(tbl)
