# WHY WOULD YOU DO THIS?

I miss the old "create event" in Google Calendar, so I wanted to make something like that, and ultimately plug it in to Alfred (which is why it's written in Python 2.7, because [alfred-workflow](https://github.com/deanishe/alfred-workflow) uses system python only).

The parsing is only as good as dateparser can produce (so-so), and my terrible date parsing code too.

# in use

    python gcollinder.py "party 23:41 23rd feb in the place"
    <some gnarly google calendar URL in return"

or with no arguments, it will read one line in. (so you can not worry about quoting and frens)

# installing strange python packages. (I no longer get my eggs from the cheese shop)

I used [pipenv](https://github.com/pypa/pipenv) to do virtualenvs which are apparently a good idea? The follow is what I done did.

```bash
laptop:tmp% git clone https://github.com/barn/python-gcal-creator.git && cd python-gcal-creator
Cloning into 'python-gcal-creator'...
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 15 (delta 4), reused 10 (delta 2), pack-reused 0
Unpacking objects: 100% (15/15), 17.18 KiB | 733.00 KiB/s, done.

laptop:python-gcal-creator% pipenv install
Installing dependencies from Pipfile.lock (70c7ae)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 6/6 — 00:00:03
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.

laptop:python-gcal-creator% pipenv shell
Launching subshell in virtual environment…
 . /Users/bea/.virtualenvs/python-gcal-creator-1-ryXFoa/bin/activate

laptop:python-gcal-creator%  . /Users/bea/.virtualenvs/python-gcal-creator-1-ryXFoa/bin/activate

laptop:python-gcal-creator% python gcollinder.py 'party at 11am tomorrow'
https://calendar.google.com/calendar/render?action=TEMPLATE&text=party+&dates=20200226T211517%2F20200226T214517&location=&trp=True
```
