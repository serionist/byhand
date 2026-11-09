"""Plain Spanish work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. Spanish office mail runs on set phrases (Estimado/a, Le
adjunto, Quedo a la espera, No dude en contactarme, Sin otro particular, Un saludo, Atentamente), and people write what
the style guides correct: el mismo as a pronoun, en base a, de acuerdo a, a nivel de, realizar, the calques hacer
sentido and aplicar a un puesto, a gerund tacked on at the end. They are a person's, never a sign. A weak sign may
fire, but plain work text must not reach a cluster.

Spanish typography is how people write: ¿ and ¡ (left out in quick chat), the raya around an aside and before
dialogue, the short dash in a range, « » and curly quotes. The dashes and curly quotes are written as escapes, as ruff
refuses them in source; the first test holds that they are the real marks."""

import unicodedata

import pytest

from byhand import signs

RAYA, SHORT, LQ, RQ = "\u2014", "\u2013", "\u201c", "\u201d"
# What a Spanish draft loads: the `any` signs and Spanish's, never another language's.
SPANISH = ("any", "es")

MAIL = [
    "Estimado Sr. García:\n\nLe adjunto la factura n.º 2026-118 correspondiente a octubre. Le agradecería que "
    "realizara el pago antes del día 30.\n\nQuedo a la espera de sus noticias.\n\nUn saludo,\nLaura Martín",
    "Hola, Rodrigo:\n\nTe mandé el presupuesto ayer en la tarde. ¿Alcanzaste a revisarlo? Si te hace sentido, lo "
    "firmamos el lunes.\n\nSaludos,\nCamila",
    "Buenos días:\n\nLes informo que el próximo viernes la oficina cerrará a las 14:00 h por mantenimiento eléctrico. "
    "Disculpen las molestias.\n\nAtentamente,\nDepartamento de Administración",
    "Hola, Martín:\n\n¿Podés pasarme el informe de ventas antes del jueves? Lo necesito para la reunión con el "
    "directorio.\n\nGracias,\nFlorencia",
    "Estimada Lic. Hernández:\n\nPor medio de la presente le confirmo la recepción de los documentos. Una vez "
    "revisados los mismos, le enviaré el contrato. No dude en contactarme si tiene alguna duda.\n\nSin otro "
    "particular, reciba un cordial saludo.\nIng. Jorge Ramírez",
    "Don Álvaro, qué pena la demora: hoy mismo le mando la cuenta de cobro con el NIT bien puesto.\n\nCordialmente,"
    "\nPaola",
    "Buenas tardes:\n\nEn base a lo hablado en la reunión, les paso el calendario de entregas de acuerdo a lo "
    "acordado con el cliente. Cualquier cambio, me avisan.\n\nUn abrazo,\nNacho",
    "Estimados todos:\n\nOs recuerdo que el plazo para entregar las hojas de gastos termina el 15 de diciembre. Los "
    "justificantes son obligatorios.\n\nUn saludo,\nRRHH",
    "Hola, Sofía:\n\nTe escribo para aplicar al puesto de analista que vi en LinkedIn. Te adjunto mi CV y quedo atenta "
    "a tus comentarios.\n\nMuchas gracias,\nValentina Rojas",
    "Estimado cliente:\n\nLamentamos las molestias por el retraso de su pedido. El transportista lo entregará el "
    "martes 12. Agradecemos su paciencia.\n\nAtención al Cliente",
    "Buenos días, Pilar:\n\nHasta mi última actualización del inventario quedaban 12 cajas de folios. Pido otras 20 "
    "para enero.\n\nUn saludo,\nAndrés",
    "Hola equipo:\n\nAhorita les mando el link de la junta. Es por eso que la movimos a las 5, por el cierre de "
    "mes.\n\nSaludos,\nMariana",
    "Estimado Ing. Torres:\n\nLe comento que el material llegó incompleto: faltan 40 piezas del pedido 3312. Quedo "
    "atento a sus comentarios.\n\nSaludos cordiales,\nRicardo Fuentes",
    "Hola, Lucía:\n\nEl presupuesto de la reforma no lo tengo hasta el jueves, que el fontanero no ha pasado. ¿Te "
    "llamo el viernes y lo vemos?\n\nUn beso,\nEva",
]
REPLIES = [
    "¡Claro! Aquí tienes la versión corregida del presupuesto:",
    "Claro, aquí tienes mi borrador del anuncio:",
    "¡Por supuesto! Aquí tiene una versión corregida de su factura, con el IVA bien calculado:",
    "¡Claro! Aquí tienes una versión más corta de mi texto de ayer:",
    "Con gusto. Aquí está el informe revisado:",
    "Por supuesto, aquí tiene el contrato firmado:",
    "Como responsable de IA, no puedo aprobar ese gasto sin el visto bueno de Dirección.",
    "Como asistente virtual, no trabajo los domingos, pero el lunes a primera hora lo tienes.",
    "Como asistente de dirección, no tengo acceso a esa agenda; pregúntale a Inés.",
    "Como IA lead del proyecto, te confirmo la fecha del piloto.",
    "Según mi última actualización del Excel, faltan tres facturas por cobrar.",
    "Hasta mi última actualización en junio de 2026, la lista de proveedores estaba completa.",
    # a person's contrast, near the model's role and its first person (#53's review, F1)
    "Usamos Copilot como asistente de IA, no como sustituto del criterio de cada técnico.",
    "Lo venden como inteligencia artificial, no como un programa de gestión.",
    "Como modelo de lenguaje, no está mal, pero se inventa las fechas.",
    "Lo venden como IA, no puedo creer que sea solo un buscador.",
    "Nos lo vendieron como inteligencia artificial, no tengo claro qué hace de verdad.",
    "La contratamos como asistente de IA, no tengo queja de ella.",
]
CHAT = [
    "ok, lo veo y te digo",
    "Llego 10 min tarde, empiecen sin mí 🙏",
    "Buena pregunta, lo reviso y te contesto",
    "Tienes toda la razón, me equivoqué de fecha. Es el 14.",
    "alguien tiene el link del Drive del proyecto?",
    "¿Alguien sabe si mañana hay reunión?",
    "dale, quedamos así 👍",
    "Gracias!! Mañana te paso lo del cliente",
    "jajaja sí, el café de la máquina está imposible",
    "Ya salió el envío de la tienda, llega mañana antes de las 12.",
    "Che, la planilla te la paso mañana, no te hagas drama.",
    "Porfa, ¿me pasas el número de pedido?",
    "Vale, lo hablamos el martes en la reunión.",
    "Listo, quedó subido a la carpeta compartida.",
    "Está bien padre la presentación, nomás súbele la letra a la gráfica.",
]
NOTES = [
    "Acta de la Reunión de Coordinación " + SHORT + " 6 de noviembre\nAsistentes: A. Pérez, B. Gómez, C. Ruiz"
    "\n- Presupuesto 2027 aprobado\n- Contratación: 2 plazas abiertas\n- Próxima reunión: 4 de diciembre",
    "Notas:\n- llamar al notario\n- enviar el contrato a Pablo [pendiente]\n- revisar la fecha de entrega "
    "[por confirmar]",
    "Parte de guardia, noche del 3 al 4\n\nSin novedades. Sin incidencias en el aparcamiento.",
    "Pendientes de la semana:\n1. Cerrar el mes\n2. Pagar a proveedores\n3. Revisar el contrato de alquiler",
    "Horario de atención: lunes a viernes, de 9" + SHORT + "14 h y de 16" + SHORT + "19 h.",
    "Plantilla de recordatorio: «Buenos días, le escribo en relación a la factura del mes pasado.»",
    "**Importante**: a partir del lunes, la tarjeta de acceso es obligatoria.",
]
REPORTS = [
    "Informe mensual de octubre\n\nLa facturación alcanzó 1,2 M€, un 4 % más que en septiembre. La empresa cerró el "
    "trimestre con pérdidas en la tienda de Zaragoza, siendo el segundo trimestre consecutivo.\n\nA nivel de "
    "personal, se incorporaron dos técnicos. Cabe señalar que el alquiler sube en enero.",
    "Resumen del proyecto Atlas\n\nEl proveedor entregó con dos semanas de retraso. A día de hoy, la migración está al "
    "80 %. La puesta en producción sigue fijada para el 15 de enero.\n\nEn resumen, mantenemos el calendario y "
    "pedimos un segundo entorno de pruebas.",
    "Memoria anual de la asociación\n\nEl cierre de la fábrica en 2019 fue un punto de inflexión para el barrio: "
    "perdimos 300 empleos y la mitad de los comercios. Este año abrimos el centro de día.",
    "Informe de la comisión\n\nNo se trata de un fallo de la báscula, sino de una tara mal anotada en el "
    "albarán. Se ha corregido el mismo y se ha avisado al cliente.",
    "Conclusiones de la auditoría\n\nLa auditoría no es solo para el departamento financiero: afecta también a "
    "compras y a logística. Las tres áreas deben entregar sus datos antes del 20.",
]
SPEECHES = [
    "Queridos socios:\n\nEn un mundo cada vez más acelerado, nuestra cooperativa sigue abriendo el mercado los "
    "sábados. Este año hemos sido 212 socios. Gracias a todos.",
    "Querido Antonio:\n\nHoy más que nunca te vamos a echar de menos en contabilidad. Treinta y dos años dan para "
    "mucho. Disfruta de la huerta.",
]
POSTS = [
    "Después de seis años en Logística Levante, me despido. Gracias a Inés y a Pablo por los inventarios de los "
    "domingos. Empiezo en Ruta Verde el 2 de diciembre. #Valencia #logística",
    "Este sábado abrimos la tienda nueva en la calle Mayor, 14. Habrá café y bizcocho para todos de 10 a 13 h. "
    "¡Os esperamos!",
]
TYPOGRAPHY = [
    "El proveedor " + RAYA + "o, mejor dicho, su comercial" + RAYA + " nos llama mañana.",
    RAYA + "¿Has visto el correo de Luis?\n" + RAYA + "Sí, pide una semana más " + RAYA + "contestó Marta" + RAYA + ".",
    "El cliente dijo: «Firmamos la semana que viene». Prefiero no adelantarme.",
    "Me contestó " + LQ + "no antes de marzo" + RQ + ", lo que nos viene bien.",
    "¿Te viene bien a las cinco? ¡Perfecto, nos vemos allí!",
    "Precio: 1.250,50 € (IVA incluido). Plazo: 3" + SHORT + "5 días hábiles.",
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
    assert sum(RAYA in text for text in OFFICE) >= 2
    assert sum("¿" in text for text in OFFICE) >= 6
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_spanish_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_no_spanish_check_counts_alone(counted_alone):
    # Until a native speaker reads them, every Spanish sign with a pattern is weak (#49): a Spanish sign with a pattern
    # that counts alone needs its lines in MACHINE below, a line per branch of its check.
    assert [sign.id for sign in counted_alone if sign.language == "es"] == []


def test_every_spanish_sign_is_weak_until_a_native_review(catalogue):
    # stricter than the plan, which lets a usual or strong sign with no pattern in: none of these sources settles one
    assert [sign.id for sign in catalogue.signs.values() if sign.language == "es" and sign.strength != "weak"] == []


# What each sign that counts alone exists to catch, inside Spanish text: a line per Spanish branch of its check, and one
# for each artefact, which is the same string in every language, so silence above can't come from a sign that finds
# nothing. Branches that read other languages' words have their lines in the other office tests.
MACHINE = [
    ("any-ai-self-reference", "Como modelo de lenguaje, no tengo opinión sobre el proveedor."),
    ("any-ai-self-reference", "Como IA, no puedo firmar este documento."),
    ("any-ai-self-reference", "Como una inteligencia artificial, no dispongo de tus cifras."),
    ("any-ai-self-reference", "Como asistente de IA, no tengo acceso a tu calendario."),
    ("any-ai-self-reference", "Como gran modelo de lenguaje, yo no puedo comprobar ese enlace."),
    ("any-ai-self-reference", "Lo siento, pero como modelo de lenguaje de IA, no poseo datos de tu empresa."),
    ("any-ai-self-reference", "¿La fusión? Como IA no me es posible predecirla."),
    ("any-ai-self-reference", "Como inteligencia artificial, no cuento con acceso a internet."),
    ("any-knowledge-cutoff", "Hasta mi última actualización de conocimientos, la empresa no se había fusionado."),
    ("any-assistant-preamble", "¡Claro! Aquí tienes una versión mejorada de tu correo:"),
    ("any-assistant-preamble", "¡Por supuesto! Aquí tienes una versión más formal de tu mensaje:"),
    ("any-assistant-preamble", "Claro que sí. Aquí tiene una versión revisada de su carta de presentación:"),
    ("any-assistant-preamble", "¡Con gusto! Aquí está tu publicación reescrita, lista para LinkedIn:"),
    ("any-assistant-preamble", "¡Claro! Aquí tienes la versión corregida de tu texto:"),
    ("any-assistant-preamble", "Desde luego. Aquí tienes una versión más profesional de tu currículum:"),
    ("any-assistant-preamble", "¡Por supuesto! Aquí tienes tu correo reformulado:"),
    ("any-assistant-closing-offer", "¿Quieres que lo amplíe con una tabla de costes?"),
    ("any-assistant-closing-offer", "¿Quieres que amplíe algún apartado?"),
    ("any-assistant-closing-offer", "¿Te gustaría que lo resuma en cinco puntos?"),
    ("any-unfilled-placeholder", "Un saludo,\n[Tu nombre]"),
    ("any-unfilled-placeholder", "Estimado [Nombre del cliente]:"),
    ("any-unfilled-placeholder", "Trabajo en [Tu empresa] desde 2020."),
    ("any-unfilled-placeholder", "Atentamente,\n[Su nombre]"),
    ("any-unfilled-placeholder", "Más información: [Insertar enlace]"),
    ("any-unfilled-placeholder", "Inscripciones: insert_link_here"),
    ("any-emoji-markers", "- 🚀 Nueva oferta de formación"),
    ("any-emoji-markers", "## 📊 Las cifras del mes"),
    ("any-chatgpt-citation-markup", "La facturación creció. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "La facturación creció. turn0search4"),
    ("any-chatbot-url-tag", "Fuente: https://ejemplo.es/informe?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "La fábrica abrió en 1998 [cite: 3]."),
    ("any-grok-citation-markup", "La fábrica abrió en 1998. grok_card"),
    ("any-deepseek-citation-markup", "La fábrica abrió en 1998【4†source】."),
    ("any-chat-tool-markup", "Según el documento adjunto[attached_file:1], el margen baja."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_spanish(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_spanish_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, SPANISH) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak phrases in one paragraph of a post
    text = "En el mundo actual, cabe destacar que nuestro equipo vive una sinergia única con el barrio."
    assert weak_hits(text, "post", SPANISH) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "Una ciudad vibrante, un mercado vibrante y unas noches vibrantes."
    assert weak_hits(text, "document", SPANISH) == 1


def test_the_spanish_checks_read_posts_and_documents_but_the_dash(catalogue):
    # the set phrases of mail and chat (no dude en contactarme, quedo atento, lamentamos las molestias) would add up in
    # mail: the Spanish signs that read mail have no pattern, and the dash is one habit however often it fires
    reading_mail = sorted(
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "es" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    )
    assert reading_mail == ["es-dash-pivots"]
    assert catalogue.signs["es-service-script"].pattern is None


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_spanish_typography_meets_no_formatting_check(catalogue, text):
    # of the files a Spanish draft reads: English's and Korean's dash signs fire here, and no Spanish draft loads them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in SPANISH and sign.category == "formatting" and sign.pattern and sign.pattern.search(text)
    ]
    assert fired == []


# Spanish inflects, and writes ¿ ¡ and the raya: the forms a weak check must still find, beyond its own `flags`, and
# the plain forms it must leave alone.
FORMS = [
    ("es-false-contrast", "Nuestro servicio no es simplemente una app, es un equipo a tu lado."),
    ("es-false-contrast", "Estas jornadas no son solo charlas; son el punto de encuentro del sector."),
    ("es-false-contrast", "No se trata de tener la tienda más grande, se trata de tener la que todos recuerdan."),
    ("es-false-contrast", "No se trata de abrir antes; se trata de no cerrar a mediodía."),
    ("es-false-contrast", "Sin colas. Sin papeleo. Solo tu café."),
    ("es-staged-reveal", "Cambiamos de proveedor. ¿La diferencia? Pedidos en 24 horas."),
    ("es-staged-reveal", "La buena noticia es que el local ya tiene licencia."),
    ("es-staged-reveal", "Lo que realmente importa es que el cliente vuelva."),
    ("es-filler-hinges", "Cabe mencionar que el curso es gratuito."),
    ("es-filler-hinges", "Es fundamental recalcar que la sala cierra a las 18 h."),
    ("es-filler-hinges", "Sin lugar a duda, la tienda nueva es la más luminosa."),
    ("es-filler-hinges", "Vale la pena señalar que el parking es gratis."),
    ("es-inflated-stakes", "En la era de la IA, la papelería de barrio sigue abierta."),
    ("es-inflated-stakes", "En un mundo en constante cambio, la coral ensaya los martes."),
    ("es-inflated-stakes", "Este acuerdo marcó un antes y un después para el polígono."),
    ("es-inflated-stakes", "Las jornadas sentaron las bases del nuevo plan."),
    ("es-inflated-stakes", "En el panorama actual, abrir una librería es un reto."),
    ("es-engagement-lines", "¿Y tú qué harías? Cuéntanos tu opinión en los comentarios."),
    ("es-engagement-lines", "Guarda esta publicación para tu próxima mudanza."),
    ("es-ai-vocabulary", "Adéntrate en la historia del puerto."),
    ("es-ai-vocabulary", "Tecnología de vanguardia para tu cocina."),
    ("es-ai-vocabulary", "Buscamos sinergias entre los dos equipos."),
    ("es-dash-pivots", "Lo probamos una semana" + RAYA + "y nadie volvió al sistema antiguo."),
    ("any-closing-summary", "En resumen, el proyecto llega a tiempo."),
    ("any-closing-summary", "En conclusión, mantenemos al proveedor."),
    ("any-flattering-agreement", "¡Excelente pregunta! Vamos por partes."),
]

LEFT_ALONE = [
    ("es-false-contrast", "No solo pagamos la luz, sino también el agua del local."),
    ("es-false-contrast", "No es solo cosa tuya: a mí tampoco me llegó el correo."),
    ("es-false-contrast", "No se trata de la reunión del jueves, que esa sigue igual."),
    ("es-false-contrast", "Lo enviamos sin factura. Sin embargo, llega el lunes."),
    ("es-staged-reveal", "¿El resultado del sondeo llega el lunes?"),
    ("es-staged-reveal", "¿La clave del wifi? Te la paso por privado."),
    ("es-filler-hinges", "Es importante que firmes las dos copias."),
    ("es-filler-hinges", "Sin duda el lunes lo cerramos."),
    ("es-inflated-stakes", "En el mundo de la hostelería, agosto es el mes fuerte."),
    ("es-inflated-stakes", "Hoy más tarde te llamo."),
    ("es-engagement-lines", "Te leo el informe esta tarde y te comento."),
    ("es-ai-vocabulary", "El móvil vibra cada vez que entra un pedido."),
    ("es-ai-vocabulary", "Los buzos se sumergen a las ocho para revisar el casco."),
    ("es-dash-pivots", "El proveedor " + RAYA + "o su comercial" + RAYA + " llama mañana."),
    ("es-dash-pivots", RAYA + "Ya voy " + RAYA + "dijo Marta" + RAYA + "."),
    ("es-dash-pivots", "La tienda abre de 10" + SHORT + "20 h los sábados."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_spanish_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_spanish_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
