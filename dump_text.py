import pdfplumber

with pdfplumber.open("samples/636483454-credit-card-statement.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Write to a text file so you can inspect it
with open("hdfc_text_dump.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Extracted text written to hdfc_text_dump.txt")
