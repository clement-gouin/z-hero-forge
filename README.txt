usage: forge.py [-h] [-n NAMESPACE] [-p] [-d] [--output OUTPUT]
                [--force FORCE]
                DIR

creates a z-hero-quest adventure from markdown data (see sample directory or DOC.md)

positional arguments:
  DIR                   data file path (default: data.txt)

options:
  -h, --help            show this help message and exit
  -n NAMESPACE, --namespace NAMESPACE
                        hero quest namespace (default: random)
  -p, --preview         show links tree in a preview.png file
  -d, --dry             do not compute links
  --output OUTPUT       create a z-app linker file
  --force FORCE         force computation even with errors

Markdown syntax uses extensions defined in https://python-markdown.github.io/extensions/ and https://facelessuser.github.io/pymdown-extensions/ 
Active extensions:
* markdown.extensions.attr_list
* markdown.extensions.def_list
* markdown.extensions.tables
* pymdownx.b64
* pymdownx.betterem
* pymdownx.blocks.admonition
* pymdownx.blocks.definition
* pymdownx.blocks.details
* pymdownx.caret
* pymdownx.details
* pymdownx.emoji
* pymdownx.escapeall
* pymdownx.fancylists
* pymdownx.magiclink
* pymdownx.mark
* pymdownx.progressbar
* pymdownx.saneheaders
* pymdownx.smartsymbols
* pymdownx.tasklist
* pymdownx.tilde
