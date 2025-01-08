from schemas import Note
from lancedb.pydantic import pydantic_to_schema
from settings import DB_URI
import lancedb
from embeddings import embeddings

db = lancedb.connect(DB_URI)


def create_table():
    table_schema = pydantic_to_schema(Note)
    db.create_table("notes", schema=table_schema)


def open_table():
    return db.open_table("notes")


def add_note(table, note: Note):
    table.add([note.model_dump()])


def get_notes(table, question=None, k=10) -> list[Note]:
    if question is not None:
        vector = embeddings(question)
        results = table.search(vector).limit(k).to_list()
    else:
        results = table.search().to_list()
    return sorted([
        Note(**payload) for payload in results
    ], key=lambda x: x.updated_at, reverse=True)


def update_note(table, note: Note):
    table.update(where=f"id = '{note.id}'", values=note.model_dump())


def remove_note(table, note: Note):
    table.delete(where=f"id = '{note.id}'")
