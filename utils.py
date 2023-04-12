def validate_weight(value: int) -> int:
    try:
        weight = float(value)
        if not 1 <= weight <= 10:
            raise ValueError(f"Invalid weight value: {value}. Weight should be between 1 and 10.")
        return weight
    except ValueError as e:
        raise ValueError(f"Invalid weight value: {value}. Weight should be a number between 1 and 10.") from e


def parse_search_string(search_string: str) -> tuple[dict[str, str], dict[str, int]]:
    search_terms = search_string.split()
    attributes = {}
    weights = {"color_weight": 1, "gender_weight": 1, "category_weight": 1, "brand_weight": 1}
    valid_genders = {"men", "women"}
    valid_keys = {"color", "gender", "category", "brand"}

    for term in search_terms:
        if ":" not in term:
            raise ValueError(f"Invalid syntax: {term}. Expected format: key:value")

        key, value = term.split(":", 1)

        if key not in valid_keys and not key.endswith("_weight"):
            raise ValueError(f"Invalid attribute key: {key}. Allowed keys: {', '.join(valid_keys)}")

        if key.endswith("_weight"):
            weights[key] = validate_weight(value)
        elif key == "gender":
            if value.lower() not in valid_genders:
                raise ValueError(f"Invalid gender value: {value}. Allowed values: {', '.join(valid_genders)}")
            attributes[key] = value.lower()
        else:
            attributes[key] = value

    return attributes, weights
