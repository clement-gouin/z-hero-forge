usage: forge.py [-h] [-n NAMESPACE] [-c COLOR] [-s START] [-p] [-d] DIR

creates a z-hero-quest adventure from markdown data (see sample directory)

positional arguments:
  DIR                   data file path (default: data.txt)

options:
  -h, --help            show this help message and exit
  -n NAMESPACE, --namespace NAMESPACE
                        hero quest namespace (default: random)
  -c COLOR, --color COLOR
                        hero quest color as: Hue (number), Saturation
                        (percent) (default: 180, 30%)
  -s START, --start START
                        start scene (default: "start.md" or first file by
                        name)
  -p, --preview         show links tree in a preview.png file
  -d, --dry             do not compute links
