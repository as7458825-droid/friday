import xml.etree.ElementTree as ET
from io import StringIO

import pandas as pd


def xml_to_dict(xml_string: str) -> dict:
    root = ET.fromstring(xml_string)

    def _parse(element):
        result = {}
        for child in element:
            child_data = _parse(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        if not result:
            return element.text or ""
        return result

    return {root.tag: _parse(root)}


def html_table_to_dataframe(html_string: str) -> list[pd.DataFrame]:
    try:
        tables = pd.read_html(StringIO(html_string))
        return tables
    except Exception as e:
        raise ValueError(f"Failed to parse HTML tables: {e}")
