# WHY WOULD YOU DO THIS?

I miss the old "create event" in Google Calendar, so I wanted to make something like that, and ultimately plug it in to Alfred (which is why it's written in Python 2.7, because [alfred-workflow](https://github.com/deanishe/alfred-workflow) uses system python only).

The parsing is only as good as dateparser can produce (so-so), and my terrible date parsing code too.

# in use

    python gcollinder.py "party 23:41 23rd feb in the place"
    <some gnarly google calendar URL in return"

or with no arguments, it will read one line in. (so you can not worry about quoting and frens)
