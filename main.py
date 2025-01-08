import click
import tempfile

from schemas import Note
from database import (
    add_note,
    create_table,
    open_table,
    get_notes,
    update_note,
    remove_note
)

@click.group()
def cli():
    pass


@cli.command()
def init():
    """
    Create the notes table in the database.
    """
    create_table()


@cli.command()
@click.argument('title', required=False)
def note(title=None):
    """
    Create a new note. Opens an editor for you to write content.
    """
    content = edit_note_content(('# ' + title) if title else '')

    new_note = Note(
        title=title,
        content=content,
    )

    table = open_table()
    add_note(table, new_note)
    click.echo("Note created successfully!")


@cli.command()
@click.argument('question', required=False)
@click.option('--k', default=10, help='Number of notes to display')
def list(question=None, k=10):
    """
    List all notes, and optionally edit one of them.
    """
    table = open_table()
    notes = get_notes(table, question, k)

    if not notes:
        click.echo("No notes found.")
        return

    while True:
        click.echo("\nAvailable notes:")
        for i, note in enumerate(notes):
            display = note.title if note.title else note.content[:50].replace('\n', ' ')
            click.echo(f"{i}. {display}")

        choice = click.prompt(
            "\nEnter the number of the note to edit, or 'q' to quit",
            default='q'
        )
        if choice.lower() == 'q':
            break

        try:
            index = int(choice)
        except ValueError:
            click.echo("Invalid input. Please enter a valid note index or 'q' to quit.")
            continue

        if index < 0 or index >= len(notes):
            click.echo("Invalid index. Please select a valid note.")
            continue

        selected_note = notes[index]
        edited_content = edit_note_content(selected_note.content)
        if edited_content != selected_note.content:
            selected_note.content = edited_content
            update_note(table, selected_note)
            click.echo("Note updated successfully!")
            notes = get_notes(table, question, k)
        else:
            click.echo("No changes detected; the note was not updated.")


@cli.command()
@click.argument('question', required=False)
@click.option('--k', default=10, help='Number of notes to display')
def remove(question=None, k=10):
    """
    Remove a note from the database.
    Shows a list of notes (optionally filtered by a query),
    then prompts for which one to remove.
    """
    table = open_table()
    notes = get_notes(table, question, k)

    if not notes:
        click.echo("No notes found.")
        return

    while True:
        click.echo("\nAvailable notes:")
        for i, note in enumerate(notes):
            display = note.title if note.title else note.content[:50].replace('\n', ' ')
            click.echo(f"{i}. {display}")

        choice = click.prompt(
            "\nEnter the number of the note to remove, or 'q' to quit",
            default='q'
        )
        if choice.lower() == 'q':
            break

        try:
            index = int(choice)
        except ValueError:
            click.echo("Invalid input. Please enter a valid note index or 'q' to quit.")
            continue

        if index < 0 or index >= len(notes):
            click.echo("Invalid index. Please select a valid note.")
            continue

        selected_note = notes[index]
        remove_note(table, selected_note)
        click.echo(f"Removed note: {selected_note.title or selected_note.content[:50]}")

        # Reload the list after removal
        notes = get_notes(table, question, k)
        if not notes:
            click.echo("No more notes found.")
            break

def edit_note_content(original_content):
    """
    Helper function to edit content in a temporary file and return the new content.
    """
    with tempfile.NamedTemporaryFile(suffix=".md") as tf:
        tf.write(original_content.encode("utf-8"))
        tf.flush()
        click.edit(filename=tf.name)
        tf.seek(0)
        edited_content = tf.read().decode("utf-8")

    return edited_content

def open(title=None):
    """
    Stub function to open a note by title (not yet implemented).
    """
    pass

def find(question=None, k=10):
    """
    Stub function for fuzzy-finding notes (not yet implemented).
    """
    pass

if __name__ == '__main__':
    cli()

