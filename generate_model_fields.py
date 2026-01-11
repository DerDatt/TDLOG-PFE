# generate_model_fields.py
import pandas as pd

def generate_model_fields_from_csv(csv_path="djangotutorial/appPFE/field_data.csv", output_path="generated_fields.txt"):
    """
    Reads CSV and generates Django model field code for copy-pasting.
    """
    df = pd.read_csv(csv_path)
    
    lines = []
    lines.append("# --- Generated fields from CSV ---")
    lines.append("# --- These are to copy-paste into the model in the accounts-app")
    
    for _, row in df.iterrows():
        name = row["name"]
        field_type = row["field_type"]
        
        # Skip header if present
        if field_type == "field_type":
            continue
        
        # Generate code line based on field type
        if field_type == "CharField":
            max_len_texts = 255
            line = f'    {name} = models.CharField(max_length={max_len_texts}, blank=True)'
            
        elif field_type == "ImageField":
            line = f"    {name} = models.ImageField(upload_to='portraits/')"

        elif field_type == "ChoiceField":
            line = f"    {name} = models.CharField(max_length=100)"

        elif field_type == "BooleanField":
            line = f"    {name} = models.BooleanField(default=False)"

        else:
            line = f'    # WARNING: Unknown type "{field_type}" for field "{name}"'
        
        lines.append(line)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    return '\n'.join(lines)


# Execute
if __name__ == "__main__":
    generate_model_fields_from_csv(
        csv_path="djangotutorial/appPFE/field_data.csv",
        output_path="generated_fields.txt"
    )