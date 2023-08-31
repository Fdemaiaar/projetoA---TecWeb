import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database():
    def __init__(self,bankName):
        self.conn = sqlite3.connect(bankName + '.db')
        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);'
            )
        
    def add(self,note):
        id = note.id
        title = note.title
        content = note.content
        comando = f"INSERT INTO note (title,content) VALUES ('{title}','{content}');"
        self.conn.execute(
            comando
            )
        self.conn.commit()

    def get_all(self):
        l = []
        cursor = self.conn.execute(
            "SELECT id, title, content FROM note;"
            )
        for linha in cursor:
            identificador = linha[0]
            titulo = linha[1]
            content = linha[2]
            l.append(Note(identificador,titulo,content))
        return l

    def update(self, entry):
        id = entry.id
        titulo = entry.title
        content = entry.content
        comando = f"UPDATE note SET title = '{titulo}', content = '{content}' WHERE id = {id};"
        cursor = self.conn.execute(
            comando
            )
        self.conn.commit()

    def delete(self, note_id):
        comando = f"DELETE FROM note WHERE id = {note_id};"
        cursor = self.conn.execute(
            comando
            )
        self.conn.commit()
    
    def get_by_id(self, id):
    # Seu código para retornar uma nota baseado no ID
        todos = self.get_all()
        for note in todos:
            if note.id == id:
                return note
    