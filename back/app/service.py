"""
Module for global service.
"""

from typing import Dict

from beanie import PydanticObjectId


def parse_query_params(query_params: Dict) -> Dict:
    """Parse common query parameters."""
    parsed_params = {}
    for key, value in query_params.items():
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif "," in value:
            value = value.split(",")
        elif "," in value:
            value = [
                float(v) if v.replace(".", "", 1).isdigit() else v
                for v in value.split(",")
            ]
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        elif key.endswith("_id"):
            value = PydanticObjectId(value)

        #  fastapi-pagination compatibility
        if key in ["page", "size"]:
            continue
        if "__" in key:
            parts = key.split("__")
            if parts[-1] in ["eq", "gt", "gte", "in", "lt", "lte", "ne", "nin"]:
                field = "__".join(parts[:-1])
                op = "$" + parts[-1]
                parsed_params[field] = {op: value}
            else:
                parsed_params[key] = value
        else:
            parsed_params[key] = value
    return parsed_params
