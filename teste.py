import pdfkit

# Caminho do executável wkhtmltopdf
WKHTMLTOPDF_PATH = r"C:\Users\Samsung\Downloads\wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# Criar um HTML simples para teste
html_content = "<h1>Teste PDF</h1><p>Isso é um teste gerado via Python.</p>"
with open("teste.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Tentar converter o HTML em PDF
try:
    pdfkit.from_file("teste.html", "teste.pdf", configuration=config)
    print("✅ PDF gerado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao gerar PDF: {e}")
