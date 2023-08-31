from utils import load_data, load_template
import urllib
from utils import add_in_file, build_response, remove_in_file
from database import database

def erro(request):
    t =  load_template('404.html')
    return build_response(body=t)

def index(request):

    db = database.Database('GETIT')
    
    if request.startswith('POST'):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)

        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        name = corpo.split('=')[0]
        if name == 'titulo':
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
            for chave_valor in corpo.split('&'):
                o = chave_valor.split('=')
                params[o[0]]=urllib.parse.unquote_plus(o[1])
            add_in_file(params)
            return build_response(code=303, reason='See Other', headers='Location: /')
        
        elif name == 'id':
            for chave_valor in corpo.split('&'):
                o = chave_valor.split('=')
                params[o[0]]=urllib.parse.unquote_plus(o[1])
        
            # Assume que o ID é passado com a chave 'id'
            note_id = params.get('id')
            if note_id:
                remove_in_file(note_id)
                return build_response(code=303, reason='See Other', headers='Location: /')
            else:
                return build_response(code=400, reason='Bad Request', body='ID da nota não fornecido!')
    
    
    # O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO...
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')

    notes_li = [
        note_template.format(identificador = note.id, title=note.title, details=note.content)
        for note in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    t =  load_template('index.html').format(notes=notes)
    return build_response(body=t)


def edit(request):
    
    db = database.Database('GETIT')
    request = request.replace('\r', '')
    partes = request.split('/')
    corpo = partes[2].split('=')

    if request.startswith('POST'):
        corpo = partes[3].split(' ')
        if corpo[0] == 'update':
            conteudo = partes[len(partes)-1]
            conteudo = conteudo.split('&')

            l = conteudo[0].split(' ')
            l2 = ((l[0]).split("\n"))

            id = ((l2[0]).split("="))[1]
            titulo = conteudo[1].split('=')[1]
            detalhes = conteudo[2].split('=')[1]

            note = database.Note(int(id),titulo,detalhes)
            db.update(note)

            return build_response(code=303, reason='See Other', headers='Location: /')
          
    if corpo[0] == 'id':
            note_id = corpo[1].split(' ')[0]
        
            # Buscar a nota no banco de dados.
            print(note_id)
            note = db.get_by_id(int(note_id))  # Supondo que você tenha um método chamado get_note_by_id.

            if note:
                # Renderizar o template.
                edit_template = load_template('editnote.html')
                filled_template = edit_template.format(title=note.title, details=note.content, identificador=note.id)
                return build_response(body=filled_template)
            else:
                erro(request)
            
    t =  load_template('editnote.html')
    return build_response(body=t)

