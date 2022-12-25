from pyspell.utils import initdb
from pyspell.practice.utils import practice_on
from pyspell.practice.models import *
import click
from datetime import datetime

SQL_SELECT_WORDS = " \
    SELECT w.name, w.description, w.audio_file FROM words w \
    INNER JOIN set_words pw \
    ON w.id = pw.word_id \
    WHERE pw.set_id = {setid}"

SQL_INSERT_PRACTICE = "INSERT INTO practices \
        (practice_set_id, wrong_words, success_ratio, practice_date) \
        VALUES ({setid}, '{bad_words_blob}', {success_ratio}, '{now}')"

@click.group("practice")
def practice_session():
    pass

@practice_session.command("start")
@click.option("--exhausted", "-ex", is_flag=True, show_default=False, default=False, help="complete the practice once there are no incorrect words left")
@click.argument("setid", type=click.INT)
def start(exhausted, setid):
    now = datetime.now().strftime("%d/%m/%y %H:%M")
        
    con = initdb()
    cur = con.cursor()

    # collect words from set
    query = SQL_SELECT_WORDS.format(setid=setid)
    cur.execute(query)
    con.commit()
    
    words = cur.fetchall()
    set_length = len(words)
    # validate
    if len(words) == 0:
        click.echo(click.style(f"invalid practice. set {setid} is empty", fg='red'))
        return
    
    practice_run = practice_on([Word(_, None) for _ in words])    
    correct_words, force_complete, incorect_word_indexes = practice_run(range(len(words)))
    # TODO: finalize the logic
    while exhausted and not force_complete and len(incorect_word_indexes) > 0:
        _correct_words, force_complete, incorect_word_indexes = practice_run(incorect_word_indexes)
        correct_words += _correct_words
    
    success_ratio = correct_words/float(set_length) if set_length > 0 else 0.0
    bad_words_blob=','.join([words[_][WORD_ROW_NAME_LOC] for _ in incorect_word_indexes])
    
    query = SQL_INSERT_PRACTICE.format(setid=setid, bad_words_blob=bad_words_blob,  success_ratio=success_ratio,now=now)    
    cur.execute(query)
    con.commit()
    
    click.echo(click.style(f"\nnew practice recorded. practice id = {cur.lastrowid}", fg="yellow", bold=True))
    con.close()
    
            
    
    
    