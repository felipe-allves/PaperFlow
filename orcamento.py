from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os

# ===============================
# CONFIGURAÇÕES MINIMALISTA
# ===============================

CONFIG = {
    'pagina': {'largura': A4[0], 'altura': A4[1]},
    'fontes': {
        'titulo': ("Helvetica-Bold", 24),
        'cabecalho': ("Helvetica-Bold", 12),
        'normal': ("Helvetica", 10),
        'total': ("Helvetica-Bold", 14),
        'rodape': ("Helvetica-Oblique", 8)
    },
    'cores': {
        'fundo': colors.white,
        'titulo': colors.HexColor("#1F2A38"),
        'empresa': colors.HexColor("#1F2A38"),
        'card_cliente_fundo': colors.HexColor("#F5F5F5"),
        'cabecalho_tabela': colors.HexColor("#2C3E50"),
        'texto_cabecalho_tabela': colors.white,
        'linha_alternada': colors.HexColor("#ECF0F1"),
        'total_fundo': colors.HexColor("#2C3E50"),
        'texto_total': colors.white,
        'rodape': colors.HexColor("#7F8C8D"),
        'divisoria': colors.HexColor("#BDC3C7")
    },
    'dimensoes': {
        'margem_horizontal': 50,
        'altura_logo': 60,
        'largura_logo': 100,
        'altura_card_cliente': 70,
        'raio_card': 8,
        'altura_linha_tabela': 18,
        'altura_total': 30,
        'raio_total': 6
    },
    'empresa': {
        'nome': "Minha Empresa LTDA - CNPJ: 00.000.000/0001-00",
        'endereco': "Rua Exemplo, 123 - Cidade/UF",
        'contato': "Tel: (00) 0000-0000  |  Email: contato@empresa.com",
        'logo': "logo.png"
    }
}

# ===============================
# COLETA DE DADOS
# ===============================

def coletar_dados_cliente():
    return {
        'name': input('Nome do Cliente: '),
        'cpf_cnpj': input('CPF/CNPJ: '),
        'endereco': input('Endereço: '),
        'telefone': input('Telefone: '),
        'email': input('E-mail: ')
    }

def coletar_itens():
    itens = []
    while True:
        descricao = input('Descrição do Item (ou "Enter" para terminar): ').strip()
        if not descricao:
            break
        qtd = int(input('Quantidade: '))
        valor_unitario = float(input('Valor Unitário: '))
        itens.append({
            'descricao': descricao,
            'quantidade': qtd,
            'valor_unitario': valor_unitario,
            'total': qtd * valor_unitario
        })
    return itens

# ===============================
# FUNÇÕES DE DESENHO
# ===============================

def desenhar_fundo(c):
    c.setFillColor(CONFIG['cores']['fundo'])
    c.rect(0, 0, CONFIG['pagina']['largura'], CONFIG['pagina']['altura'], fill=1)

def desenhar_titulo(c):
    fonte, tamanho = CONFIG['fontes']['titulo']
    c.setFont(fonte, tamanho)
    c.setFillColor(CONFIG['cores']['titulo'])
    c.drawCentredString(CONFIG['pagina']['largura']/2, CONFIG['pagina']['altura'] - 60, "ORÇAMENTO")

def desenhar_logo_e_empresa(c):
    conf = CONFIG
    try:
        c.drawImage(conf['empresa']['logo'], conf['dimensoes']['margem_horizontal'],
                    conf['pagina']['altura'] - 140, width=conf['dimensoes']['largura_logo'],
                    height=conf['dimensoes']['altura_logo'], preserveAspectRatio=True)
    except:
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.red)
        c.drawString(conf['dimensoes']['margem_horizontal'], conf['pagina']['altura'] - 100, "[Logo não encontrada]")
    c.setFillColor(conf['cores']['empresa'])
    c.setFont(*conf['fontes']['cabecalho'])
    c.drawString(conf['dimensoes']['margem_horizontal'], conf['pagina']['altura'] - 150, conf['empresa']['nome'])
    c.setFont(*conf['fontes']['normal'])
    c.drawString(conf['dimensoes']['margem_horizontal'], conf['pagina']['altura'] - 165, conf['empresa']['endereco'])
    c.drawString(conf['dimensoes']['margem_horizontal'], conf['pagina']['altura'] - 180, conf['empresa']['contato'])

def desenhar_divisoria(c, y_pos):
    c.setStrokeColor(CONFIG['cores']['divisoria'])
    c.setLineWidth(1)
    c.line(40, y_pos, CONFIG['pagina']['largura'] - 40, y_pos)

def desenhar_card_cliente(c, cliente, y_start):
    conf = CONFIG
    c.setFillColor(conf['cores']['card_cliente_fundo'])
    c.roundRect(45, y_start - conf['dimensoes']['altura_card_cliente'],
                conf['pagina']['largura'] - 90, conf['dimensoes']['altura_card_cliente'],
                radius=conf['dimensoes']['raio_card'], fill=1, stroke=0)
    c.setFont(*conf['fontes']['normal'])
    c.setFillColor(colors.black)
    c.drawString(60, y_start - 15, f"Nome: {cliente['name']}")
    c.drawString(60, y_start - 30, f"CPF/CNPJ: {cliente['cpf_cnpj']}")
    c.drawString(60, y_start - 45, f"Endereço: {cliente['endereco']}")
    c.drawString(60, y_start - 60, f"Telefone: {cliente['telefone']} | E-mail: {cliente['email']}")

def desenhar_cabecalho_tabela(c, y_start):
    conf = CONFIG
    c.setFillColor(conf['cores']['cabecalho_tabela'])
    c.rect(45, y_start - 15, conf['pagina']['largura'] - 90, 20, fill=1, stroke=0)
    c.setFont(*conf['fontes']['cabecalho'])
    c.setFillColor(conf['cores']['texto_cabecalho_tabela'])
    c.drawString(60, y_start - 10, "Descrição")
    c.drawString(280, y_start - 10, "Qtd")
    c.drawString(340, y_start - 10, "Unitário")
    c.drawString(430, y_start - 10, "Total")

def desenhar_itens(c, itens, y_start):
    conf = CONFIG
    y = y_start
    subtotal = 0
    for idx, item in enumerate(itens):
        if idx % 2 == 0:
            c.setFillColor(conf['cores']['linha_alternada'])
            c.rect(45, y - 5, conf['pagina']['largura'] - 90, conf['dimensoes']['altura_linha_tabela'], fill=1, stroke=0)
        c.setFont(*conf['fontes']['normal'])
        c.setFillColor(colors.black)
        c.drawString(60, y, item['descricao'])
        c.drawString(280, y, str(item['quantidade']))
        c.drawString(340, y, f"R${item['valor_unitario']:.2f}")
        c.drawString(430, y, f"R${item['total']:.2f}")
        subtotal += item['total']
        y -= 20
    return y, subtotal

def desenhar_total(c, total, y):
    conf = CONFIG
    c.setFillColor(conf['cores']['total_fundo'])
    c.roundRect(300, y-5, 200, conf['dimensoes']['altura_total'], radius=conf['dimensoes']['raio_total'], fill=1, stroke=0)
    c.setFont(*conf['fontes']['total'])
    c.setFillColor(conf['cores']['texto_total'])
    c.drawCentredString(400, y+5, f"TOTAL: R${total:.2f}")

def desenhar_rodape(c):
    conf = CONFIG
    c.setFont(*conf['fontes']['rodape'])
    c.setFillColor(conf['cores']['rodape'])
    c.drawCentredString(conf['pagina']['largura']/2, 30, "Documento gerado automaticamente - não possui valor fiscal.")

# ===============================
# GERAR PDF MINIMALISTA
# ===============================

def gerar_pdf_minimalista(cliente, itens, nome_arquivo):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    desenhar_fundo(c)
    desenhar_titulo(c)
    desenhar_logo_e_empresa(c)
    desenhar_divisoria(c, CONFIG['pagina']['altura'] - 190)
    desenhar_card_cliente(c, cliente, CONFIG['pagina']['altura'] - 220)
    y_tabela_start = CONFIG['pagina']['altura'] - 330
    c.setFont(*CONFIG['fontes']['cabecalho'])
    c.setFillColor(colors.black)
    c.drawString(50, y_tabela_start, "Itens do Orçamento")
    y_tabela_start -= 20
    desenhar_cabecalho_tabela(c, y_tabela_start)
    y_after_items, subtotal = desenhar_itens(c, itens, y_tabela_start - 35)
    desenhar_total(c, subtotal, y_after_items - 20)
    desenhar_rodape(c)
    c.save()
    print(f"PDF '{nome_arquivo}' gerado com sucesso! 💯 Minimalista.")

# ===============================
# EXECUÇÃO
# ===============================

def main():
    cliente = coletar_dados_cliente()
    itens = coletar_itens()
    if not os.path.exists("orcamentos"):
        os.makedirs("orcamentos")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    nome_arquivo = f"orcamentos/{cliente['name']}-orcamento-{timestamp}.pdf"
    gerar_pdf_minimalista(cliente, itens, nome_arquivo)

if __name__ == "__main__":
    main()
