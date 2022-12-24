from pyspell.practice import practice_session
from pyspell.sets import practice_set
from pyspell.utils import *
from pyspell.sets.utils import *
from tabulate import tabulate
import re

import click

@click.group()
def cli():
    """Spelling Master"""

# RUN CIRCULAR EXECUTION EXAMPLE from https://stackoverflow.com/questions/40091347/call-another-click-command-from-a-click-command
    # @click.command()
    # @click.argument('content', required=False)
    # @click.option('--to_stdout', default=False)
    # @click.pass_context
    # def add_name_and_surname(ctx, content, to_stdout=False):
    #     result = ctx.invoke(add_surname, content=ctx.forward(add_name))
    #     if to_stdout is True:
    #         sys.stdout.writelines(result)
    #     return result

@cli.command("init", help="initialize the application (a mandatory)")
@click.argument("db")
def init_db(db):
    click.echo(click.style("RUN COMMAND:", fg="yellow", bold=True))
    click.echo(click.style(f"echo 'export PYSPELL_DB={db}' >> ~/.zshrc && source ~/zshrc"))

@cli.command(help="remove existing practice session or practice set")
@click.argument("src", type=click.Choice(["sets", "practices"], case_sensitive=True))
@click.option("--id", "-i", type=click.STRING)
def rm(src, id):
    con = initdb()
    cur = con.cursor()
    query = f"DELETE from {src} WHERE ({ids_to_sql('id', id)})"
    print(query)
    cur.execute(query)
    con.commit()
    if src == "sets":
        query = f"DELETE from set_words WHERE ({ids_to_sql('set_id', id)})"
        print(query)
        cur.execute(query)
        con.commit()        
    con.close()
    
    click.echo(f"{src}'s #{id} removed successfully")

@cli.command(help="list the available sets and practices")
@click.argument("src", type=click.Choice(["sets", "practices", "words"], case_sensitive=True))
def ls(src):
    con = initdb()
    cur = con.cursor()
    
    table = [get_schema(con, cur, src)]
    
    query = f"SELECT * FROM {src}"
    cur.execute(query)
    con.commit()

    for row in cur:
        _row = []
        for col in row:
            if isinstance(col, str):
                col = f"{col[:100]}..." if len(col) > 100 else col
            elif isinstance(col, bytearray) or isinstance(col, bytes):
                col = "..."
            _row.append(col)
        table.append(_row)
    
    click.echo(click.style(tabulate(table, headers="firstrow", tablefmt="fancy_grid"), fg="bright_white"))
    con.close()
    
@cli.command(help="create new practice set")
@click.argument("src", type=click.Choice(["sets", "words"], case_sensitive=True))
@click.option("--name", "-n", type=click.STRING)
@click.option("--description", "-desc", "desc", default="", type=click.STRING)
def add(src, name, desc):
    con = initdb()
    cur = con.cursor()
    # check if already exists
    query = f"SELECT id FROM {src} WHERE name = '{name}'"
    cur.execute(query)
    con.commit()
    
    if cur.fetchone():
        click.echo(click.style(f"skip creating new {name}, already exists", fg="yellow"))
        return
    # insert
    if src == "sets":
        query = f"INSERT INTO {src} (name, description) VALUES ('{name}', '{desc}')"
        cur.execute(query)
        con.commit()
        
        lastid = cur.lastrowid        
    elif src == "words":
        if desc == "":
            click.echo(click.style("adding new word require description. empty description provided", fg="red"))
            return
        lastid = add_word(con, name, desc)
        
    con.close()
    
    click.echo(f"{src}'s #{lastid} created successfully")

cli.add_command(practice_session)
cli.add_command(practice_set)
    
if __name__ == "__main__":
    cli()