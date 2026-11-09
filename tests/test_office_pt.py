"""Plain Portuguese work text, invented, from Brazil and Portugal, against the real catalogue. A strong or usual sign
counts alone, so one that fires on any of these accuses a person of writing like a machine. Portuguese office mail runs
on set phrases (Atenciosamente, Com os melhores cumprimentos, Exmo. Senhor, Fico à disposição, Prezado, Qualquer
dúvida, é só dizer, Respeitosamente, Segue em anexo, Sem mais para o momento, Venho por este meio), which
evitar-escrita-ia lists among chatbot artefacts and every office writes. Formal registers keep their formulas: a
funding application's no âmbito do projeto and de forma transversal, a contract's ao abrigo da cláusula and salvo
acordo em contrário, a manual's poderá and por defeito, a paper's passive and its além disso, ademais and é importante
destacar que (evitar-escrita-ia's list of false positives, and Andrade et al.'s own prose). People write no que diz
respeito a, a verdade é que, cada vez mais and vale lembrar (humanizer-pt-br says so of each), a gerund in Brazil (fico
aguardando, estou enviando), the calque fazer sentido, and either variety's words and spelling (wikipedia-pt: no
variety is a sign). They are a person's, never a sign. A weak sign may fire, but plain work text must not reach a
cluster.

Portuguese typography is how people write: a spaced travessão on each side of an aside and before a line of dialogue,
the short dash in a range, « » and curly quotes. The dashes and curly quotes are written as escapes, as ruff refuses
them in source; the first test holds that they are the real marks."""

import unicodedata

import pytest

from byhand import signs

RAYA, SHORT, LQ, RQ = "\u2014", "\u2013", "\u201c", "\u201d"
# What a Portuguese draft loads: the `any` signs and Portuguese's, never another language's.
PORTUGUESE = ("any", "pt")

MAIL = [
    "Prezado Sr. Almeida,\n\nSegue em anexo a nota fiscal nº 4521, referente aos serviços de outubro. Peço a "
    "gentileza de efetuar o pagamento até o dia 30.\n\nFico à disposição para quaisquer esclarecimentos.\n\n"
    "Atenciosamente,\nJuliana Costa",
    "Exmo. Senhor Eng. Sousa,\n\nVenho por este meio enviar o orçamento pedido na reunião de terça-feira. Qualquer "
    "dúvida, é só dizer.\n\nCom os melhores cumprimentos,\nRita Fonseca",
    "Oi, Rafa! Te mandei a planilha ontem à noite. Conseguiu dar uma olhada? Se fizer sentido, a gente fecha na "
    "segunda.\n\nAbs,\nBia",
    "Bom dia, pessoal,\n\nInformo que na próxima sexta o escritório fecha às 14h por causa da manutenção elétrica. "
    "Desculpem o transtorno.\n\nAtenciosamente,\nAdministração",
    "Olá Miguel,\n\nPodes enviar-me o relatório de vendas até quinta? Preciso dele para a reunião com a "
    "administração.\n\nObrigada,\nInês",
    "Senhor Diretor,\n\nEncaminho, em anexo, o relatório de atividades do primeiro semestre, para conhecimento e "
    "providências que julgar cabíveis.\n\nRespeitosamente,\nCarlos Eduardo Lima\nChefe de Divisão",
    "Boa tarde,\n\nNo que diz respeito ao contrato de manutenção, conforme conversado na reunião, a renovação fica "
    "para janeiro. Sendo assim, peço que confirmem as datas.\n\nAbraço,\nMarcelo",
    "Caros colegas,\n\nLembro que o prazo para entregar as despesas termina a 15 de dezembro. Os comprovativos são "
    "obrigatórios.\n\nCumprimentos,\nRecursos Humanos",
    "Olá, Fernanda,\n\nEstou enviando meu currículo para a vaga de analista que vi no LinkedIn. Fico no aguardo do seu "
    "retorno.\n\nMuito obrigado,\nLucas Pereira",
    "Prezado cliente,\n\nLamentamos o atraso na entrega do seu pedido. A transportadora fará a entrega na terça-feira, "
    "dia 12. Agradecemos a compreensão.\n\nSem mais para o momento,\nAtendimento ao Cliente",
    "Bom dia, Sandra,\n\nAté a minha última atualização do estoque havia 12 caixas de papel A4. Vou pedir mais 20 "
    "para janeiro.\n\nAbs,\nAndré",
    "Caros parceiros,\n\nNo âmbito do projeto, as ações de formação chegam aos três parceiros de forma transversal. "
    "Envio a versão final da candidatura até sexta.\n\nCom os melhores cumprimentos,\nTeresa Matos",
    "Exma. Senhora,\n\nInformamos que, ao abrigo da cláusula 12.ª do contrato e salvo acordo em contrário, o "
    "pré-aviso é de 60 dias.\n\nCom os melhores cumprimentos,\nDepartamento Jurídico",
    "Oi, Lu,\n\nO orçamento da reforma só sai na quinta, o encanador ainda não passou. Te ligo na sexta e a gente "
    "vê?\n\nBeijo,\nCarla",
    "Prezados condôminos,\n\nVale lembrar que a garagem será pintada na quarta, das 8h às 12h. Tirem os carros "
    "na terça.\n\nAtenciosamente,\nA Síndica",
    "Olá a todos,\n\nEspero que estejam bem. Junto envio a ata da reunião de ontem; além disso, a sala 3 fica "
    "reservada para sexta.\n\nBeijinhos,\nSofia",
]
REPLIES = [
    "Claro! Aqui está a versão corrigida do orçamento:",
    "Claro, aqui está o meu rascunho do anúncio:",
    "Com certeza! Aqui tem a fatura corrigida, com o IVA bem calculado:",
    "Claro! Aqui está uma versão mais curta do meu texto de ontem:",
    "Com certeza. Segue o relatório revisado:",
    "Claro! Segue seu currículo revisado:",
    "Certamente, aqui tem o contrato assinado:",
    "Como responsável de IA, não posso aprovar essa despesa sem o aval da direção.",
    "Como assistente virtual, não trabalho aos domingos, mas segunda cedo está pronto.",
    "Como assistente de direção, não tenho acesso a essa agenda; pergunte à Inês.",
    "Segundo a minha última atualização da planilha, faltam três faturas.",
    "Até a minha última atualização em junho de 2026, a lista de fornecedores estava completa.",
    "Até à minha última atualização do plano de treino, a corrida era no sábado.",
    "Até à minha última atualização de conhecimentos em suporte básico de vida, eram 30 compressões.",
    "Até minha última atualização de treinamento de NR-35, eu estava habilitado para altura.",
    "Até à minha última atualização de treino no relógio, ia nos 12 km.",
    # a person's contrast or verdict, near the model's role and its first person (#53's review, rounds 1 to 4)
    "Usamos o Copilot como modelo de linguagem, não como substituto do critério de cada técnico.",
    "Vendem-no como inteligência artificial, não como um programa de gestão.",
    "Como modelo de linguagem, não está mal, mas inventa as datas.",
    "Vendem como IA, não posso acreditar que seja só um buscador.",
    "Como IA, não tenho queixa dela: poupa-me horas.",
    "Como IA, não posso pedir-lhe mais.",
    "Como IA não tenho acesso a nenhuma no trabalho, faço tudo à mão.",
    "Como assistente de IA, não tenho acesso à versão Pro: a empresa só paga a básica.",
    "Como IA não tenho preferências, uso a que me derem.",
    "Enquanto modelo de negócio, não posso garantir margens maiores.",
    "Como assistente de IA, não consigo acessar o ChatGPT pela rede do escritório, está bloqueado.",
]
CHAT = [
    "ok, vejo e te falo",
    "Chego 10 min atrasado, comecem sem mim 🙏",
    "Boa pergunta, vou ver e já te respondo",
    "Tens toda a razão, enganei-me na data. É dia 14.",
    "alguém tem o link do Drive do projeto?",
    "Amanhã tem reunião?",
    "Fechado, combinado assim 👍",
    "Valeu!! Amanhã te passo o do cliente",
    "kkkkk sim, o café da máquina está horrível",
    "Com certeza! Mando já.",
    "Qualquer coisa, me chama.",
    "Tá, falamos na terça na reunião.",
    "Pronto, ficou na pasta partilhada.",
    "A apresentação ficou muito boa, só aumenta a letra do gráfico.",
    "Ótima pergunta, não faço ideia 😅",
    "Você tem toda a razão, mando hoje.",
]
NOTES = [
    "Ata da reunião de coordenação " + SHORT + " 6 de novembro\nPresentes: A. Pereira, B. Gomes, C. Ramos"
    "\n- Orçamento 2027 aprovado\n- Contratação: 2 vagas abertas\n- Próxima reunião: 4 de dezembro",
    "Notas:\n- ligar para o cartório\n- enviar o contrato ao Paulo [pendente]\n- rever a data de entrega [a confirmar]",
    "Pendências da semana:\n1. Fechar o mês\n2. Pagar fornecedores\n3. Rever o contrato de arrendamento",
    "Horário de atendimento: segunda a sexta, das 9h" + SHORT + "12h e das 14h" + SHORT + "18h.",
    "Modelo de lembrete: «Bom dia, escrevo a propósito da fatura do mês passado.»",
    "**Importante**: a partir de segunda, o crachá é obrigatório.",
    "Escala de plantão, noite de 3 para 4\n\nSem novidades. Sem ocorrências no estacionamento.",
]
REPORTS = [
    "Relatório mensal de outubro\n\nO faturamento chegou a R$ 1,2 milhão, 4% acima de setembro. A loja de Campinas "
    "fechou o trimestre no prejuízo, pelo segundo trimestre seguido.\n\nEm relação ao pessoal, entraram dois "
    "técnicos. Vale ressaltar que o aluguel sobe em janeiro.",
    "Resumo do projeto Atlas\n\nO fornecedor entregou com duas semanas de atraso. Neste momento a migração está a 80%. "
    "A entrada em produção mantém-se a 15 de janeiro.\n\nEm resumo, mantemos o calendário e pedimos um segundo "
    "ambiente de testes.",
    "Resultados\n\nOs textos foram etiquetados automaticamente. Além disso, as sentenças foram analisadas por um "
    "parser de dependências. É importante destacar que os erros de anotação são pontuais.",
    "Relatório da comissão\n\nNão se trata de uma avaria da balança, mas de uma tara mal registada na guia de "
    "remessa. A guia foi corrigida e o cliente foi avisado.",
    "Conclusões da auditoria\n\nA auditoria não é só para o departamento financeiro: abrange também compras e "
    "logística. As três áreas entregam os dados até dia 20.",
    "Relatório anual da associação\n\nO fecho da fábrica em 2019 foi um divisor de águas para o bairro: perdemos 300 "
    "empregos e metade do comércio. Este ano abrimos o centro de dia.",
    "Manual do utilizador\n\nNo editor, clique em [Inserir] e escolha Tabela. O sistema poderá, opcionalmente, enviar "
    "um alerta por e-mail. Por defeito, os relatórios são gerados à segunda-feira e guardados durante 90 dias.",
    "Artigo, secção 4\n\nÉ importante destacar que o estimador é robusto à heterocedasticidade. Os erros-padrão foram "
    "agrupados por município, o que é crucial quando as observações não são independentes. A amostra é abrangente: "
    "cobre os 27 estados.",
    "Relatório de inspeção\n\nA estrutura é robusta e cumpre o Eurocódigo 8. Importa referir que a inspeção de 2019 "
    "não detetou fissuras. Mais do que nunca, a manutenção preventiva é crucial para a ponte.",
    "Resultado do trimestre\n\nNo cenário atual de juros altos, as vendas caíram 8%. Vale ressaltar que a "
    "inadimplência ficou estável. O papel da diretoria é crucial na renegociação com os bancos.",
    "Avaliação da horta escolar\n\nEm suma, a horta aumentou o consumo de verduras na merenda. Vale destacar que a "
    "adesão foi maior no 6º ano. É importante ressaltar que o estudo durou um semestre.",
    "Relatório final da obra\n\nEm conclusão, a obra cumpre o projeto aprovado pela câmara. É fundamental sublinhar "
    "que a fiscalização foi diária. Importa realçar que não houve acidentes de trabalho.",
    "Conclusão\n\nEm suma, a abordagem holística do paciente reduziu as reinternações em 12%. Cabe ressaltar que a "
    "amostra foi pequena.",
    "Mercado\n\nEm resumo, a fusão deve gerar sinergias de R$ 400 milhões por ano. Vale ressaltar que o negócio "
    "ainda depende do Cade.",
    "Relatório do polo tecnológico\n\nEm resumo, o ecossistema de inovação de Recife já reúne 400 empresas. A criação "
    "do parque, em 2000, foi um divisor de águas para o centro histórico.",
    "Recensão\n\nEm suma, a obra discute a proteção de dados na era digital, enfatizando o papel da autoridade "
    "nacional.",
    "Resumo da dissertação\n\nEm suma, a dissertação analisa o ensino da escrita na era da inteligência artificial, "
    "enfatizando o papel do professor.",
    "Nota de política\n\nEm conclusão, a diretiva reforça a concorrência no ecossistema digital europeu, enfatizando "
    "as plataformas de grande dimensão.",
    "Acórdão, súmula\n\nEm suma, o relator entendeu que a cláusula não é apenas abusiva, é ainda nula de pleno "
    "direito, enfatizando o art. 51 do CDC.",
    "Assembleia municipal\n\nEm suma, o problema da linha não é só o dinheiro, é que ninguém decide. O autarca "
    "falou na assembleia, enfatizando os prazos.",
    "Guião de atendimento\n\nEncerramento:\n- Confirmar o número do pedido\n"
    "- Há mais alguma coisa em que possa ajudar?",
    "Parecer técnico\n\nA ponte precisa de reforço. A verdade é que a obra de 2015 não resolveu as infiltrações, e "
    "cada vez mais camiões usam a estrada. Ademais, o orçamento só chega em março.",
]
SPEECHES = [
    "Caros sócios,\n\nNum mundo cada vez mais apressado, a nossa cooperativa continua a abrir o mercado aos sábados. "
    "Este ano fomos 212 sócios. Obrigado a todos.",
    "Querido Antônio,\n\nMais do que nunca vamos sentir sua falta na contabilidade. Trinta e dois anos não são pouca "
    "coisa. Aproveite a chácara.",
]
POSTS = [
    "Depois de seis anos na Logística Atlântico, despeço-me. Obrigado à Inês e ao Pedro pelos inventários de domingo. "
    "Começo na Rota Verde a 2 de dezembro. #Porto #logística",
    "Neste sábado abrimos a loja nova na Rua Augusta, 14. Vai ter café e bolo para todo mundo, das 10h às 13h. "
    "Esperamos vocês!",
    "A verdade é que o mutirão de sábado deu certo: 40 voluntários e 300 mudas plantadas. Obrigada a todos!",
]
TYPOGRAPHY = [
    "O fornecedor " + RAYA + " ou melhor, o comercial dele " + RAYA + " liga amanhã.",
    RAYA + " Viste o e-mail do Luís?\n" + RAYA + " Vi, pede mais uma semana " + RAYA + " respondeu a Marta.",
    "O cliente disse: «Assinamos para a semana». Prefiro não me adiantar.",
    "Ele respondeu " + LQ + "não antes de março" + RQ + ", o que nos dá jeito.",
    "Às cinco dá-te jeito? Perfeito, vemo-nos lá!",
    "Preço: R$ 1.250,50 (com impostos). Prazo: 3" + SHORT + "5 dias úteis.",
    "Valor: 1250,50 € (IVA incluído). A obra " + RAYA + " a segunda fase " + RAYA + " começa em abril.",
]

OFFICE = MAIL + REPLIES + CHAT + NOTES + REPORTS + SPEECHES + POSTS + TYPOGRAPHY

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS + SPEECHES + TYPOGRAPHY),
    *((text, "post") for text in POSTS),
]


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name(RAYA) == "EM DASH"
    assert unicodedata.name(SHORT) == "EN DASH"
    assert unicodedata.name(LQ) == "LEFT DOUBLE QUOTATION MARK"
    assert unicodedata.name(RQ) == "RIGHT DOUBLE QUOTATION MARK"
    assert sum(RAYA in text for text in OFFICE) >= 3
    assert sum("«" in text for text in OFFICE) >= 2
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_portuguese_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_no_portuguese_check_counts_alone(counted_alone):
    # Until a native speaker reads them, every Portuguese sign with a pattern is weak (#49): a Portuguese sign with a
    # pattern that counts alone needs its lines in MACHINE below, a line per branch of its check.
    assert [sign.id for sign in counted_alone if sign.language == "pt"] == []


def test_every_portuguese_sign_is_weak_until_a_native_review(catalogue):
    # stricter than the plan, which lets a usual or strong sign with no pattern in: none of these sources settles one
    assert [sign.id for sign in catalogue.signs.values() if sign.language == "pt" and sign.strength != "weak"] == []


# What each sign that counts alone exists to catch, inside Portuguese text: a line per Portuguese branch of its check,
# and one for each artefact, which is the same string in every language, so silence above can't come from a sign that
# finds nothing. Branches that read other languages' words have their lines in the other office tests.
MACHINE = [
    ("any-ai-self-reference", "Como modelo de linguagem, não tenho opinião sobre o fornecedor."),
    ("any-ai-self-reference", "Como modelo de linguagem, não posso assinar este documento."),
    ("any-ai-self-reference", "Como um modelo de linguagem, não disponho dos seus números."),
    ("any-ai-self-reference", "Como modelo de linguagem, não tenho acesso ao seu calendário."),
    ("any-ai-self-reference", "Como grande modelo de linguagem, eu não posso verificar esse link."),
    ("any-ai-self-reference", "Lamento, mas como modelo de linguagem de IA, não possuo dados da sua empresa."),
    ("any-ai-self-reference", "A fusão? Como modelo de linguagem não me é possível prevê-la."),
    ("any-ai-self-reference", "Enquanto modelo de linguagem, não tenho emoções."),
    ("any-ai-self-reference", "Como modelo de linguagem treinado pela Google, não tenho acesso ao seu e-mail."),
    ("any-ai-self-reference", "Como modelo de linguagem desenvolvido pela OpenAI, não tenho opiniões políticas."),
    ("any-ai-self-reference", "No entanto, como modelo de linguagem, não consigo aceder a esse ficheiro."),
    ("any-ai-self-reference", "Devo esclarecer que como modelo de linguagem não tenho sentimentos."),
    ("any-ai-self-reference", "Como modelo de linguagem de IA, não posso fornecer aconselhamento jurídico."),
    ("any-ai-self-reference", "Como modelo de linguagem, não tenho experiências pessoais."),
    ("any-ai-self-reference", "Como modelo de linguagem, não posso garantir que o número esteja certo."),
    ("any-ai-self-reference", "Como modelo de linguagem, não tenho crenças religiosas."),
    ("any-ai-self-reference", "Como modelo de linguagem, não tenho um corpo físico."),
    ("any-ai-self-reference", "Porém, como modelo de linguagem, não sou capaz de navegar na internet."),
    ("any-ai-self-reference", "Como modelo de linguagem, não posso acessar a internet."),
    ("any-ai-self-reference", "Como modelo de linguagem, não posso acrescentar datas à sua agenda."),
    ("any-knowledge-cutoff", "Até a minha última atualização de conhecimento, a empresa não se tinha fundido."),
    ("any-knowledge-cutoff", "Até à minha última atualização de treino, não havia dados sobre esse evento."),
    ("any-knowledge-cutoff", "Até minha última atualização de treinamento, em março de 2023, não havia registo disso."),
    (
        "any-knowledge-cutoff",
        "Até minha última atualização de conhecimento em outubro de 2023 não havia notícia disso.",
    ),
    ("any-knowledge-cutoff", "Até minha última atualização de conhecimento em 2023, a fábrica ainda não tinha aberto."),
    ("any-knowledge-cutoff", "Até à minha última atualização de conhecimentos (abril de 2024), o cargo estava vago."),
    (
        "any-knowledge-cutoff",
        "Não sei se já abriu: a loja não existia até à minha última atualização de conhecimentos.",
    ),
    (
        "any-knowledge-cutoff",
        "Até minha última atualização de conhecimento "
        + RAYA
        + " em abril de 2024 "
        + RAYA
        + " esse modelo não existia.",
    ),
    ("any-knowledge-cutoff", "Até minha última atualização de treinamento no início de 2024, não havia esse produto."),
    ("any-assistant-preamble", "Claro! Aqui está uma versão melhorada do seu e-mail:"),
    ("any-assistant-preamble", "Com certeza! Aqui está uma versão mais formal da sua mensagem:"),
    ("any-assistant-preamble", "Claro que sim. Aqui tem uma versão revista da sua carta de apresentação:"),
    ("any-assistant-preamble", "Certamente! Aqui está o seu post reescrito, pronto para o LinkedIn:"),
    ("any-assistant-preamble", "Claro! Aqui tens a versão corrigida do teu texto:"),
    ("any-assistant-preamble", "Com certeza. Eis uma versão mais profissional do seu currículo:"),
    ("any-assistant-preamble", "Claro! Aqui está a sua mensagem reformulada:"),
    ("any-assistant-preamble", "Claro! Aqui está uma versão mais clara e concisa do seu texto:"),
    ("any-assistant-closing-offer", "Quer que eu expanda com uma tabela de custos?"),
    ("any-assistant-closing-offer", "Queres que eu o resuma em cinco pontos?"),
    ("any-assistant-closing-offer", "Gostaria que eu detalhasse alguma secção?"),
    ("any-unfilled-placeholder", "Atenciosamente,\n[Seu nome]"),
    ("any-unfilled-placeholder", "Prezado [Nome do cliente],"),
    ("any-unfilled-placeholder", "Trabalho na [Sua empresa] desde 2020."),
    ("any-unfilled-placeholder", "Com os melhores cumprimentos,\n[O teu nome]"),
    ("any-unfilled-placeholder", "Mais informações: [Inserir link]"),
    ("any-unfilled-placeholder", "Morada: [Inserir: morada completa]"),
    ("any-unfilled-placeholder", "Cliente: [Insira: nome da empresa]"),
    ("any-unfilled-placeholder", "Escreva para [Seu endereço de e-mail]."),
    ("any-unfilled-placeholder", "[Descreva a secção a editar]"),
    ("any-unfilled-placeholder", "Inscrições: insert_link_here"),
    ("any-emoji-markers", "- 🚀 Nova oferta de formação"),
    ("any-emoji-markers", "## 📊 Os números do mês"),
    ("any-chatgpt-citation-markup", "O faturamento cresceu. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "O faturamento cresceu. turn0search4"),
    ("any-chatbot-url-tag", "Fonte: https://exemplo.pt/relatorio?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "A fábrica abriu em 1998 [cite: 3]."),
    ("any-grok-citation-markup", "A fábrica abriu em 1998. grok_card"),
    ("any-deepseek-citation-markup", "A fábrica abriu em 1998【4†source】."),
    ("any-chat-tool-markup", "Segundo o documento anexo[attached_file:1], a margem desce."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_portuguese(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_portuguese_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, PORTUGUESE) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak phrases in one paragraph of a post
    text = "Num mundo cada vez mais digital, vamos mergulhar no bairro, enfatizando as lojas."
    assert weak_hits(text, "post", PORTUGUESE) == signs.WEAK_CLUSTER


def test_a_dash_pivot_takes_no_other_sign_s_phrase(weak_hits):
    # the dash's match runs from the line's start over both phrases, but Grep runs each sign on its own: three (#56)
    text = "Num mundo cada vez mais digital, a feira volta no domingo — e desta vez enfatizando as lojas."
    assert weak_hits(text, "post", PORTUGUESE) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "Vamos mergulhar no orçamento, vamos mergulhar nas contas e vamos mergulhar outra vez."
    assert weak_hits(text, "document", PORTUGUESE) == 1


def test_the_portuguese_checks_read_posts_and_documents_but_the_dash(catalogue):
    # the set phrases of mail and chat (fico à disposição, qualquer dúvida, sem mais para o momento) would add up in
    # mail: no Portuguese sign that reads mail has a pattern but the dash, which is one habit however often it fires
    reading_mail = sorted(
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "pt" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    )
    assert reading_mail == ["pt-dash-pivots"]


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_portuguese_typography_meets_no_formatting_check(catalogue, text):
    # of the files a Portuguese draft reads: English's and Korean's dash signs fire here, and no Portuguese draft loads
    # them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in PORTUGUESE and sign.category == "formatting" and sign.pattern and sign.pattern.search(text)
    ]
    assert fired == []


# Portuguese inflects, writes enclisis in Portugal and proclisis in Brazil, and sets asides between spaced travessões:
# the forms a weak check must still find, beyond its own `flags`, and the plain forms it must leave alone.
FORMS = [
    ("pt-staged-reveal", "Mudámos de fornecedor. O detalhe? Encomendas em 24 horas."),
    ("pt-staged-reveal", "Já parou para pensar quanto custa uma reunião?"),
    ("pt-staged-reveal", "Já paraste para pensar quanto custa uma reunião?"),
    ("pt-staged-reveal", "E a melhor parte? É grátis."),
    ("pt-inflated-stakes", "A feira faz 30 anos em um mundo cada vez mais apressado."),
    ("pt-closing-cheer", "O melhor ainda está por vir!"),
    ("pt-closing-cheer", "Só o tempo dirá."),
    ("pt-ai-vocabulary", "Estamos enfatizando a entrega no prazo."),
    ("pt-ai-vocabulary", "Vamos mergulhar no orçamento de 2027."),
    ("pt-dash-pivots", "Testámos durante uma semana" + RAYA + "e ninguém voltou ao sistema antigo."),
    ("pt-dash-pivots", "O mercado volta no domingo " + RAYA + " com pastéis."),
    (
        "pt-dash-pivots",
        "A feira " + RAYA + " a de agosto " + RAYA + " volta. O mercado abre no domingo " + RAYA + " e com pastéis.",
    ),
    ("pt-dash-pivots", RAYA + " Já vou " + RAYA + " disse a Marta. Depois saiu " + RAYA + " e não voltou."),
    ("any-closing-summary", "Em suma, o projeto chega a tempo."),
    ("any-closing-summary", "Em conclusão, mantemos o fornecedor."),
    ("any-flattering-agreement", "Ótima pergunta! Vamos por partes."),
    ("any-flattering-agreement", "Excelente questão! Começo pelo orçamento."),
]

LEFT_ALONE = [
    ("pt-staged-reveal", "O resultado da sondagem sai na segunda?"),
    ("pt-staged-reveal", "A senha do wifi? Mando-te por mensagem."),
    ("pt-staged-reveal", "Já parou de chover?"),
    ("pt-staged-reveal", "O resultado? Ainda não saiu."),
    ("pt-inflated-stakes", "No mundo da restauração, agosto é o mês forte."),
    ("pt-inflated-stakes", "Cada vez mais clientes pagam com Pix."),
    ("pt-inflated-stakes", "Mais do que nunca precisamos de voluntários."),
    ("pt-inflated-stakes", "Em 2000, o parque tecnológico foi um divisor de águas para o centro."),
    ("pt-inflated-stakes", "A obra discute a proteção de dados na era digital."),
    ("pt-inflated-stakes", "O congresso debate o jornalismo na era da inteligência artificial."),
    ("pt-inflated-stakes", "No cenário atual de juros, ninguém compra casa."),
    ("pt-closing-cheer", "O futuro da loja depende do aluguel."),
    ("pt-ai-vocabulary", "O ecossistema do rio está a recuperar."),
    ("pt-ai-vocabulary", "O telemóvel vibra sempre que entra um pedido."),
    ("pt-ai-vocabulary", "Mergulhamos às oito para ver o casco."),
    ("pt-ai-vocabulary", "A abordagem holística do paciente reduziu as reinternações."),
    ("pt-ai-vocabulary", "A fusão deve gerar sinergias de R$ 400 milhões por ano."),
    ("pt-ai-vocabulary", "O ecossistema de inovação de Recife reúne 400 empresas."),
    ("pt-ai-vocabulary", "A diretiva reforça a concorrência no ecossistema digital europeu."),
    ("pt-ai-vocabulary", "A estrutura é robusta e o plano é abrangente; o prazo é crucial."),
    ("pt-dash-pivots", "O fornecedor " + RAYA + " ou o comercial dele " + RAYA + " liga amanhã."),
    ("pt-dash-pivots", RAYA + " Já vou " + RAYA + " disse a Marta."),
    ("pt-dash-pivots", RAYA + " Já vou. Espera só um bocadinho " + RAYA + " disse a Marta."),
    ("pt-dash-pivots", "A loja abre das 10" + SHORT + "20h aos sábados."),
    ("pt-dash-pivots", "A reunião " + RAYA + " lembras-te? " + RAYA + " passou para quinta."),
    ("pt-dash-pivots", "A obra " + RAYA + " a cargo da Construções Silva, Lda. " + RAYA + " acaba em junho."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_portuguese_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_portuguese_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
