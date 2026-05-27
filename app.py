from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'aurarara_segredo_2026_v4'

# =========================================================================
# BANCO DE DADOS DISTRIBUÍDO SEM DEIXAR NENHUMA COLEÇÃO VAZIA
# =========================================================================
PRODUTOS = {
    # --- ANÉIS ---
    'anel_outono_ouro': {
        'id': 'anel_outono_ouro', 'nome': 'Anel Textura Outono Ouro', 'preco': 219.90,
        'imagem': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=600',
        'categoria': 'aneis', 'colecao': 'al-mare',
        'descricao': 'Com design orgânico e bordas marteladas, este anel reflete a luz de forma suave.'
    },
    'anel_solitario_luxo': {
        'id': 'anel_solitario_luxo', 'nome': 'Anel Solitário Aura Real', 'preco': 189.90,
        'imagem': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?q=80&w=600',
        'categoria': 'aneis', 'colecao': 'palace',
        'descricao': 'O clássico solitário com uma zircônia central lapidada em alta precisão.'
    },
    'anel_entrelacado': {
        'id': 'anel_entrelacado', 'nome': 'Anel Entrelaçado Infinito', 'preco': 149.90,
        'imagem': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?q=80&w=600',
        'categoria': 'aneis', 'colecao': 'amor-duo',
        'descricao': 'Fios de ouro que se cruzam de forma leve e fluida, ideal para o verão.'
    },
    'anel_ajustavel_minimal': {
        'id': 'anel_ajustavel_minimal', 'nome': 'Anel Ajustável Minimalista', 'preco': 129.90,
        'imagem': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=600',
        'categoria': 'aneis', 'colecao': 'soleil',
        'descricao': 'Conforto e sofisticação em uma peça regulável e moderna.'
    },
    'anel_alianca_cravejada': {
        'id': 'anel_alianca_cravejada', 'nome': 'Meia Aliança Cravejada', 'preco': 179.90,
        'imagem': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=600',
        'categoria': 'aneis', 'colecao': 'palace',
        'descricao': 'Uma fileira reluzente de microzircônias premium lapidadas.'
    },

    # --- BRINCOS ---
    'brinco_argola_folha': {
        'id': 'brinco_argola_folha', 'nome': 'Argola Botânica Vintage', 'preco': 159.90,
        'imagem': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=600',
        'categoria': 'brincos', 'colecao': 'al-mare',
        'descricao': 'Movimento fluido inspirado nas folhas de outono e na natureza.'
    },
    'brinco_perola_barroca': {
        'id': 'brinco_perola_barroca', 'nome': 'Brinco Pérola Barroca Rara', 'preco': 199.90,
        'imagem': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?q=80&w=600',
        'categoria': 'brincos', 'colecao': 'al-mare',
        'descricao': 'Pérolas naturais com formatos orgânicos e brilho perolado único.'
    },
    'brinco_argola_bold': {
        'id': 'brinco_argola_bold', 'nome': 'Argola Bold Click Premium', 'preco': 139.90,
        'imagem': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600',
        'categoria': 'brincos', 'colecao': 'soleil',
        'descricao': 'Uma argola grossa, robusta e polida em altíssimo brilho.'
    },
    'brinco_ear_cuff_luz': {
        'id': 'brinco_ear_cuff_luz', 'nome': 'Ear Cuff Degradê de Zircônias', 'preco': 169.90,
        'imagem': 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600',
        'categoria': 'brincos', 'colecao': 'amor-duo',
        'descricao': 'Sobe o contorno da orelha distribuindo pontos intensos de luz.'
    },
    'brinco_ponto_fixo': {
        'id': 'brinco_ponto_fixo', 'nome': 'Brinco Ponto de Luz Clássico', 'preco': 99.90,
        'imagem': 'https://images.unsplash.com/photo-1543294001-f7cbfe92237e?q=80&w=600',
        'categoria': 'brincos', 'colecao': 'palace',
        'descricao': 'Discreto, mas com uma lapidação brilhante essencial e atemporal.'
    },

    # --- COLARES ---
    'colar_choker_imponente': {
        'id': 'colar_choker_imponente', 'nome': 'Choker Malha Fita Inverno', 'preco': 289.90,
        'imagem': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600',
        'categoria': 'colares', 'colecao': 'palace',
        'descricao': 'Malha italiana espessa que se molda perfeitamente ao pescoço.'
    },
    'colar_ponto_de_luz': {
        'id': 'colar_ponto_de_luz', 'nome': 'Colar Ponto de Luz Raro', 'preco': 189.90,
        'imagem': 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600',
        'categoria': 'colares', 'colecao': 'soleil',
        'descricao': 'Corrente veneziana finíssima com uma zircônia translúcida.'
    },
    'colar_elo_portugues': {
        'id': 'colar_elo_portugues', 'nome': 'Corrente Elo Português', 'preco': 249.90,
        'imagem': 'https://images.unsplash.com/photo-1543294001-f7cbfe92237e?q=80&w=600',
        'categoria': 'colares', 'colecao': 'amor-duo',
        'descricao': 'Elos redondos marcantes e fecho boia de presença frontal.'
    },
    'colar_escapulario_fe': {
        'id': 'colar_escapulario_fe', 'nome': 'Escapulário Minimalista Fé', 'preco': 169.90,
        'imagem': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=600',
        'categoria': 'colares', 'colecao': 'al-mare',
        'descricao': 'Proteção, devoção e elegância em uma corrente geométrica.'
    },
    'colar_gravatinha_slim': {
        'id': 'colar_gravatinha_slim', 'nome': 'Colar Gravatinha Zircônias', 'preco': 199.90,
        'imagem': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?q=80&w=600',
        'categoria': 'colares', 'colecao': 'soleil',
        'descricao': 'Design vertical delicado que alonga sutilmente a silhueta.'
    }
}

@app.route('/')
def index():
    chaves_destaque = ['anel_outono_ouro', 'colar_choker_imponente', 'colar_ponto_de_luz', 'brinco_perola_barroca', 'anel_solitario_luxo', 'brinco_argola_bold']
    destaques = {k: PRODUTOS[k] for k in chaves_destaque if k in PRODUTOS}
    favoritos_lista = session.get('favoritos', [])
    return render_template('index.html', produtos=destaques, favoritos_lista=favoritos_lista)

@app.route('/categoria/<nome_categoria>')
def categoria(nome_categoria):
    produtos_filtrados = {k: v for k, v in PRODUTOS.items() if v.get('categoria') == nome_categoria}
    titulos = {
        'aneis': 'Galeria de Anéis — Design & Alta Lapidação',
        'brincos': 'Coleção de Brincos — Molduras de Brilho',
        'colares': 'Linha de Colares — Elos e Linhas Nobres'
    }
    titulo = titulos.get(nome_categoria, "Nossos Produtos")
    favoritos_lista = session.get('favoritos', [])
    return render_template('categoria.html', produtos=produtos_filtrados, titulo_categoria=titulo, favoritos_lista=favoritos_lista)

@app.route('/colecao/')
@app.route('/colecao/<nome_colecao>')
def colecao(nome_colecao='todas'):
    if nome_colecao == 'todas':
        produtos_filtrados = PRODUTOS
        titulo = "Todas as Coleções Aura Rara"
    else:
        produtos_filtrados = {k: v for k, v in PRODUTOS.items() if v.get('colecao') == nome_colecao}
        titulos = {
            'al-mare': 'Coleção Al Mare — Sensações e Brilho Marinho',
            'amor-duo': 'Coleção Amor Duo — Romantismo em Dose Dupla',
            'soleil': 'Coleção Soleil — Energia e Luz do Sol',
            'palace': 'Coleção Palace — Sofisticação e Realeza'
        }
        titulo = titulos.get(nome_colecao, "Coleção Exclusiva Aura Rara")
    return render_template('colecao.html', produtos=produtos_filtrados, titulo_colecao=titulo)

@app.route('/carrinho')
def carrinho():
    carrinho_sessao = session.get('carrinho', {})
    itens_carrinho = []
    subtotal = 0.0
    for prod_id, qtd in carrinho_sessao.items():
        if prod_id in PRODUTOS:
            info = PRODUTOS[prod_id]
            total_item = info['preco'] * qtd
            subtotal += total_item
            itens_carrinho.append({
                'id': prod_id, 'nome': info['nome'], 'preco': info['preco'],
                'imagem': info['imagem'], 'quantidade': qtd, 'total': total_item
            })
    return render_template('carrinho.html', carrinho=itens_carrinho, subtotal=subtotal, falta_frete=max(0.0, 199.90 - subtotal), frete_gratis=subtotal>=199.90)

@app.route('/adicionar/<produto_id>')
def adicionar_ao_carrinho(produto_id):
    if 'carrinho' not in session: session['carrinho'] = {}
    carrinho = dict(session['carrinho'])
    if produto_id in PRODUTOS: carrinho[produto_id] = carrinho.get(produto_id, 0) + 1
    session['carrinho'] = carrinho
    session.modified = True
    return redirect(url_for('carrinho'))

@app.route('/limpar_sacola')
def limpar_sacola():
    session.pop('carrinho', None)
    session.modified = True
    return redirect(url_for('carrinho'))

# --- ROTAS INSTITUCIONAIS ---
@app.route('/sobre')
def sobre(): 
    return render_template('sobre.html')

@app.route('/feedback')
def feedback(): 
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=False)