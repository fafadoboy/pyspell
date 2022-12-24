import click
from io import BytesIO
from gtts import gTTS
import os

def add_word(con, word, desc):
    cur = con.cursor()
    # generate mp3 audio
    mp3_fp = BytesIO()
    tts = gTTS(word, lang='en')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    blob = mp3_fp.read()
    cur.execute(f"INSERT INTO words (name, description, audio_file) VALUES('{word}', '{desc}', ?)", (blob,))
    con.commit()
    
    return cur.lastrowid

def add_word_to_set(con, setid, word, desc):
    click.echo(f"try to add {word} to set {setid}")
    
    cur = con.cursor()
    
    cur.execute(f"SELECT id FROM words WHERE name = '{word}'")
    con.commit()
    
    word_ids = [_[0] for _ in cur.fetchall()]

    if len(word_ids) == 0:
        # add new word
        if desc == "":
            click.echo(click.style("adding new word require description. empty description provided", fg="red"))
            return
        lastid = add_word(con, word, desc)
    else:
        # fetch all the sets contains the word
        cur.execute(f"SELECT DISTINCT(set_id) FROM set_words WHERE word_id = {word_ids[0]}")
        con.commit()        
        sets_id = [_[0] for _ in cur.fetchall()]
        
        # check if the word already if set
        if setid in sets_id:
            click.echo(click.style(f"skip adding new word. '{word}' already exists is set", fg="yellow"))
            return
        else:
            # add the word id to the set
            lastid = word_ids[0]
    
    # append the last id
    cur.execute(f"INSERT INTO set_words (set_id, word_id) VALUES ({setid}, {lastid})")
    con.commit()
    
    click.echo(f"#{lastid} created successfully")

def register_file(con, file, delimiter, setid):
    if not os.path.exists(file):
        click.echo(click.style(f"missing file={file}", fg="red"))
        return False
    
    with open(file) as f:
        for ll in f.readlines():
            try:
                f_word, f_desc = ll.split(delimiter)
                if f_word == "" or f_desc == "":
                    click.echo(click.style("skip adding new word. please provide non empty word and description", fg="yellow", bold=True))
                    continue                
                add_word_to_set(con, setid, str.strip(f_word), str.strip(f_desc))
            except Exception as e:
                click.echo(click.style(f"exception: {e}", fg="red"))
                click.echo(click.style(f"skip adding new word. invalid input line ({ll}) in file", fg="yellow", bold=True))                
    return True