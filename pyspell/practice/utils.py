import click
import random
import tempfile
import os
import time
from typing import List, Union
from pyspell.practice.models import Word
import contextlib

@contextlib.contextmanager
def audio(blob):
    f = tempfile.NamedTemporaryFile(mode="w+b", suffix=".mp3", delete=False)                
    f.write(blob)
    fname = f.name
    f.close()
    
    yield fname
    
    os.remove(fname)
    

def practice_on(words: List[Word]):
    def wrapper(indexes: List[int]) -> Union[float, bool, List[int]]:
        
        incorrect_indexes = []
        practice_force_complete = False
        cnt_correct_words = 0.0
        random_indexes = random.sample(indexes, len(indexes))
        
        click.clear()
        with click.progressbar(random_indexes, color="bright_white") as bar:
            for n, i in enumerate(bar):
                if practice_force_complete: # handle .q command
                    # exhaust unprocessed words
                    incorrect_indexes += random_indexes[n:]
                    break
                
                word = words[i]
                name, desc, audio_blob = word.word
                
                with audio(audio_blob) as fname:
                    while True:
                        click.echo(click.style(f"\n\nDESCRIPTION: \n\t{desc}", fg="bright_white"))
                        os.system("afplay " + fname)
                        answer = str.lower(str.strip(click.prompt(f"\nENTER YOUR ANSER")))
                        # hanlde command
                        if answer == ".r":
                            continue
                        elif answer == ".q":
                            practice_force_complete = True
                            break
                        
                        word.answer = answer
                        
                        if name == answer:
                            cnt_correct_words+=1
                            click.echo(click.style(f"\n {answer.upper()} = {name.upper()}", fg="green"))
                            time.sleep(1)
                        else:
                            click.echo(click.style(f"\n {answer.upper()} ≠ {name.upper()}", fg="red"))                
                            incorrect_indexes.append(i)
                            time.sleep(5)
                        break                
                click.clear()
        return cnt_correct_words, practice_force_complete, sorted(incorrect_indexes)
    return wrapper
