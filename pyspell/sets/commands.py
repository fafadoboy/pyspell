from io import BytesIO
from gtts import gTTS
from pyspell.utils import *
from pyspell.sets.utils import *
from tabulate import tabulate

import click

@click.group("set", help="sub-command")
def practice_set():
    pass

@practice_set.command("ls", help="list words in practice set")
@click.argument("set_id", type=click.INT)
def ls(set_id):
    query = f" \
    SELECT w.id, w.name, w.description FROM words w \
    INNER JOIN set_words pw \
    ON w.id = pw.word_id \
    WHERE pw.set_id = {set_id}"
    
    con = initdb()
    cur = con.cursor()
    
    table = [["#"] + list(get_schema(con, cur, "sets"))]
        
    cur.execute(query)
    con.commit()
    
    for n, row in enumerate(cur, start=1):
        table.append([n] + list(row))
        
    click.echo(click.style(tabulate(table, headers="firstrow", tablefmt="fancy_grid"), fg="bright_white"))
    
    con.close()

@practice_set.command("add", help="add word to set")
@click.option("--id", "-i", "_setid", type = click.INT, help="id of the set for the word to be added into")
@click.option("--file", "-f", "_file", is_flag=True, show_default=False, default=False, help="flag to signal that INPUT is a file. Otherwise INPUT is treated as full self-contained word and descrip")
@click.option("--delimiter", default="|")
@click.argument("input", nargs=-1)
def add(_setid, _file, delimiter, input):
    con = initdb()
    
    if _file:
        [register_file(con, _, delimiter, _setid) for _ in input]
        con.close()
        return
    
    word, desc = input
    if word == "":
        click.echo(click.style(f"invalid input {input}. first argument expected should not be empty", fg="red"))
    
    add_word_to_set(con, _setid, str.strip(word).lower(), str.strip(desc).lower())
    con.close()
    
    
