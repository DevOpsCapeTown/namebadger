# Conference Name Badger

The principal goes like this:

1. Make/obtain a template PDF with blank name badges laid out
2. Download attendee list in CSV format
3. Wave magic wand
4. Email the resulting PDF to a print shop

The magic wand is this repo.

Clone it now.

The `.gitignore` includes pdf, psd, csv and other extensions so you can just work in your clone's working tree.

Open the `namebadger.py` script and start hacking. Look around for the following (line numbers not given as they are likely to change).

## Setting the template file

```python
PDF_TEMPLATE = 'A3-Layout-Attendee-Test.pdf'
```

## Setting the CSV input file and which columns to use for attendee names

```python
CSV_FILE = 'devopsdays-cape-town-2018_guestlist.csv'
FIRSTNAME_COLUMN = 30
LASTNAME_COLUMN = 31
```

## Setting positions of names on the page

How you format this depends on how many badges fit on a page. For double sided 110mm square badges, you should fit 3x2 on an A3 page - 3 badges with each name printed twice. This looks like this:

```python
POSITIONS = [
    [[112, 1026], [430, 1026]],
    [[112, 714], [430, 714]],
    [[112, 400], [430, 400]],
]
```

Where the first value of each tuple holds the left-right coordinates, and the second values hold the bottom-top coords. The coords start in the bottom left corner of a page, so higher numbers go *right* and *up*. You will have to experiment here.

## Text color

```python
TEXT_RGB = (16, 95, 89)
```

Where the R, G and B values can be lifted straight from your image editor of choice.

## Text size

Text size is a little complicated, because each name is printed with an initial maximum size, but scaled down progressively if the name is too long to fit at that size.

```python
TEXT_START_SIZE = 24

TEXT_SIZE_THRESHOLDS = (
    (220, 16),
    (210, 17),
    (195, 18),
    (180, 19),
    (170, 20),
    (160, 21),
    (150, 22),
    (140, 23),
)
```
Where `TEXT_START_SIZE` is the maximum starting size, and `TEXT_SIZE_THREHOLDS` is a table of lengths versus point sizes, used for deciding whether to scale down an individual name to fit in the space available.

## Changing the font

```python
FIRSTNAME_FONT = 'Avenir-Bold'
LASTNAME_FONT = 'Avenir'
```

You'll need this font to be present in the `fonts/` subdirectory and you'll need to register it using reportlab in the script (if it's not a standard system font).

## Output

The script blurts out a file called `out.pdf` each time it is run.


## Caveats

I have no idea what I am doing, so it's likely this script will break all over the place. It's also terrible because I am really lazy. Sorry about that. Contributions welcome.
