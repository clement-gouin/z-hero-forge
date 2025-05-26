usage: forge.py [-h] [-n NAMESPACE] [-c COLOR] [-p] [-d] [--output OUTPUT] DIR

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
  -p, --preview         show links tree in a preview.png file
  -d, --dry             do not compute links
  --output OUTPUT       create a z-app linker file
