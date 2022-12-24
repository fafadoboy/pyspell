from dataclasses import dataclass
from pyspell.utils import initdb
import os
import click
import tempfile
import random
import time
from datetime import datetime

@dataclass
class Result:
    word: str
    answer: str
    correct: bool
    

SQL_SELECT_WORDS = " \
    SELECT w.name, w.description, w.audio_file FROM words w \
    INNER JOIN set_words pw \
    ON w.id = pw.word_id \
    WHERE pw.set_id = {setid}"

SQL_INSERT_PRACTICE = "INSERT INTO practices \
        (practice_set_id, wrong_words, success_ratio, practice_date) \
        VALUES ({setid}, '{bad_words_blob}', {success_ratio}, '{now}')"

@click.group("practice", help="sub-command")
def practice_session():
    pass

@practice_session.command("start")
@click.argument("setid", type=click.INT)
def start(setid):    
    now = datetime.now().strftime("%d/%m/%y %H:%M")
    results = []
        
    con = initdb()
    cur = con.cursor()

    # collect words from set
    query = SQL_SELECT_WORDS.format(setid=setid)
    cur.execute(query)
    con.commit()
    
    words = cur.fetchall()    
    set_length = len(words)
    # validate
    if set_length == 0:
        click.echo(click.style(f"invalid practice. set {setid} is empty", fg='red'))
        return
    
    correct_words = 0.0
    forloop_break = False
    click.clear()
    with click.progressbar(random.sample(range(set_length), set_length), color="bright_white") as bar:
        for i in bar:        
            if forloop_break: # handle .quit command
                break
            
            name, desc, audio = words[i]
            f = tempfile.NamedTemporaryFile(mode="w+b", suffix=".mp3", delete=False)                
            f.write(audio)        
            fname = f.name
            f.close()
            
            while True:
                # click.clear()
                click.echo(click.style(f"\n\nDESCRIPTION: \n\t{desc}", fg="blue"))
                os.system("afplay " + fname)
                answer = str.lower(str.strip(click.prompt(f"\nENTER YOUR ANSER")))
                # hanlde command
                if answer == ".r":
                    continue
                elif answer == ".q":
                    forloop_break = True
                    break
                
                r = Result(name, answer, name == answer)
                if r.correct:
                    correct_words+=1
                    click.echo(click.style(f"\n {r.answer.upper()} = {r.word.upper()}", fg="green"))
                else:
                    click.echo(click.style(f"\n {r.answer.upper()} ≠ {r.word.upper()}", fg="red"))
                
                results.append(r)
                time.sleep(3)
                break
            
            os.remove(fname)
            click.clear()
            
    # finalize the results
    incorect_words = [_.word for _ in results if not _.correct]
    success_ratio = correct_words/float(set_length) if set_length > 0 else 0.0
    bad_words_blob=','.join(incorect_words)    
    
    query = SQL_INSERT_PRACTICE.format(setid=setid, bad_words_blob=bad_words_blob,  success_ratio=success_ratio,now=now)    
    cur.execute(query)
    con.commit()
    
    click.echo(click.style(f"\nnew practice recorded. practice id = {cur.lastrowid}", fg="yellow", bold=True))
    con.close()
    
            
    
    
    