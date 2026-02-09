# generate_model_fields.py
# Run from project root:  python backend/generate_model_fields.py
# Or from backend:       python generate_model_fields.py
import pandas as pd
from pathlib import Path

# Paths relative to this script's directory (backend/)
_BACKEND_DIR = Path(__file__).resolve().parent


def strip_name_of_underscores_begin_end(name: str) -> str:
    return name.lstrip("_").rstrip("_")


def generate_model_fields_from_csv(
    csv_path=None,
    output_path=None,
):
    """
    Reads CSV and generates Django model field code for copy-pasting.
    """
    csv_path = csv_path or _BACKEND_DIR / "appPFE" / "field_data.csv"
    output_path = output_path or _BACKEND_DIR / "generated_fields.txt"
    csv_path = Path(csv_path)
    output_path = Path(output_path)

    df = pd.read_csv(csv_path)

    lines = []
    lines.append("# --- Generated fields from CSV ---")
    lines.append("# --- Copy these into backend/accounts/models.py, class MyUser ---")

    max_len_texts = 255
    for _, row in df.iterrows():
        name = strip_name_of_underscores_begin_end(row["name"])
        field_type = row["field_type"]

        # Skip header if present
        if field_type == "field_type":
            continue

        # Generate code line based on field type
        if field_type == "CharField":
            line = f"    {name} = models.CharField(max_length={max_len_texts}, blank=True)"

        elif field_type == "ImageField":
            line = f"    {name} = models.CharField(max_length={max_len_texts}, blank=True)"
            # line = f"    {name} = models.ImageField(upload_to='images')"

        elif field_type == "ChoiceField":
            line = f"    {name} = models.CharField(max_length=100, default='not_chosen')"

        elif field_type == "BooleanField":
            line = f"    {name} = models.BooleanField(default=False)"

        else:
            line = f'    # WARNING: Unknown type "{field_type}" for field "{name}"'

        lines.append(line)

    # Used to indicate if the form is fully completed (for admin display)
    lines.append("    form_complete = models.BooleanField(default=False)")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


if __name__ == "__main__":
    generate_model_fields_from_csv()
