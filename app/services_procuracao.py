import os
import re
from docx import Document
from docx.shared import Pt

PLACEHOLDER_PATTERN = re.compile(r'{{(.*?)}}')

def substituir_placeholders_procuracao(paragraph, dados):
    """
    Substitui os placeholders no parágrafo.
    - Os valores inseridos (aqueles que substituem os placeholders) serão formatados em negrito;
    - Se o parágrafo for o do outorgante (ou seja, começar com "OUTORGANTE:"), todo o parágrafo ficará em negrito.
    """
    # Concatena o texto de todos os runs do parágrafo
    full_text = "".join(run.text for run in paragraph.runs)
    
    # Verifica se este é o parágrafo do outorgante
    outorgante_flag = full_text.strip().startswith("OUTORGANTE:")
    
    # Se não houver placeholder, e se for o parágrafo do outorgante, apenas aplica bold em todos os runs.
    if "{{" not in full_text:
        if outorgante_flag:
            for run in paragraph.runs:
                run.bold = True
        return

    # Divide o texto em partes; os tokens em posições ímpares correspondem aos nomes dos placeholders.
    parts = re.split(PLACEHOLDER_PATTERN, full_text)
    
    # Cria uma lista de tuplas (texto, is_placeholder)
    new_tokens = []
    is_placeholder = False
    for part in parts:
        if is_placeholder:
            valor = dados.get(part.strip(), "")
            new_tokens.append((valor, True))
        else:
            new_tokens.append((part, False))
        is_placeholder = not is_placeholder

    # Limpa o parágrafo e recria os runs
    paragraph.text = ""
    for token_text, is_bold in new_tokens:
        run = paragraph.add_run(token_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        # Se for o parágrafo do outorgante, força bold; caso contrário, apenas os placeholders ficam em bold.
        run.bold = True if outorgante_flag else is_bold

def preencher_procuracao(dados, base_dir):
    """
    Gera a procuração com base no modelo (arquivo1.docx).
    - Converte todos os valores para maiúsculas;
    - Apenas os valores inseridos (substituições dos placeholders) ficam em negrito, 
      exceto se o parágrafo for o do outorgante, que ficará todo em negrito.
    - O restante do documento permanece conforme o template original.
    """
    modelo_path = os.path.join(base_dir, "..", "templates", "arquivo1.docx")
    if not os.path.exists(modelo_path):
        raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")
    
    doc = Document(modelo_path)
    
    # Converter todos os valores para maiúsculas e remover espaços extras
    dados_processados = {chave: valor.strip().upper() if valor else "" for chave, valor in dados.items()}
    
    # Substituir placeholders nos parágrafos
    for para in doc.paragraphs:
        substituir_placeholders_procuracao(para, dados_processados)
    
    # Substituir placeholders nas células das tabelas (se existirem)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for para in celula.paragraphs:
                    substituir_placeholders_procuracao(para, dados_processados)
    
    output_dir = os.path.join(base_dir, "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    nome_cliente = dados_processados.get("nome", "SEM_NOME")
    doc_path = os.path.join(output_dir, f"PROCURACAO_{nome_cliente}.docx".replace(" ", "_"))
    doc.save(doc_path)
    return doc_path
