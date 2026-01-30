import re

# Input and output file names (you can change these)
input_file = "input.txt"
output_file = "Outputs/vars.json"

# Compile a regex pattern that matches lines without '='
pattern = re.compile(r'^[^=]+$', re.MULTILINE)

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all lines that don't contain '='
cleaned_text = re.sub(pattern, '', text)

# Remove any extra blank lines left over
cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(cleaned_text + '\n')

print(f"✅ Cleaned file written to: {output_file}")