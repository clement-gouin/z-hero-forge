# [Z] Hero Forge Documentation <!-- omit in toc -->

`forge.py` compute markdown files in the specified directory (not sub-directories) into [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) playable links (using [z-app-linker](https://github.com/clement-gouin/z-app-linker/)).

See [README.txt](./README.txt) for CLI arguments.

- [Basics](#basics)
- [Scenes / Subscenes](#scenes--subscenes)
- [Actions](#actions)
- [Commands](#commands)
  - [`/include path_1 path_2 ...`](#include-path_1-path_2-)
  - [`/show var, icon, default`](#show-var-icon-default)
  - [`/set var = value`](#set-var--value)
  - [`/start var`](#start-var)
  - [`/end var`](#end-var)
  - [`/color hue, saturation`](#color-hue-saturation)
- [Comments](#comments)
- [Markdown / HTML](#markdown--html)
  - [Icons](#icons)
  - [Colors](#colors)
  - [Level 2 title (bypass default behavior)](#level-2-title-bypass-default-behavior)
  - [Lists (bypass default behavior)](#lists-bypass-default-behavior)
  - [Admonitions](#admonitions)
  - [Emojis](#emojis)
  - [Mark](#mark)
  - [Progress bar](#progress-bar)
  - [Relative image](#relative-image)
  - [Tables](#tables)


## Basics

Each file is called a **scene** and can have **sub-scenes**.

There are 5 types of line in a scene files:

* [Subscene key](#scenes--subscenes) (defined by markdown level 2 title `##`)
* [Actions definition](#actions) (defined by markdown list and sub list `*`)
* [Commands](#commands) (defined by `/command`)
* [Comments](#comments) (defined by markdown/HTML comments `<!-- comment -->`)
* [Markdown/HTML](#markdown--html) (otherwise)

```markdown
<!-- subscene key -->
## default

<!-- markdown/html -->
Click the <b>button</b> below to start the *demo*

<!-- command -->
/set myvar = 0

<!-- actions -->
* Start
  * [[forest]]
```

## Scenes / Subscenes

TODO

## Actions

TODO

## Commands

### `/include path_1 path_2 ...`

Replace the line with the content of specified files.

Before:
```markdown
<!-- main.md -->
/include ./fragments/var1.md ./fragments/var2.md

<!-- fragments/var1.md -->
/set var1 = 0

<!-- fragments/var2.md -->
/set var2 = 0
/include ./var3.md

<!-- fragments/var3.md -->
/set var3 = 0
```

After:
```markdown
<!-- main.md -->
/set var1 = 0
/set var2 = 0
/set var3 = 0
```

### `/show var, icon, default`

Display variable as icon and value in the final page.

Extracted from [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) documentation:
```txt
Variable Name, Lucide Icon, Default value (js, default to 0)
```

Sample:
```markdown
/show health,heart,100
/show strength,sword,13
/show constitution,shield,13
/show agility,target,13
```

### `/set var = value`

Update variable in the background in the final page.

Extracted from [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) documentation:
```txt
Variable Name = Value change (js)
```

Sample:
```markdown
/set strength=strength+1
/set health=Math.max(health-20,0)
```

### `/start var`

Shortand command for `/set var=1`

### `/end var`

Shortand command for `/set var=2`

### `/color hue, saturation`

Set final page color.

Extracted from [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) documentation:
```txt
Hue, Saturation (optional, "180, 30%" by default)
```

Sample:
```markdown
/color 1.13,83.25%

It's so hot in here
```

## Comments

Markdown/HTML comments (and empty lines) are removed from final data to reduce space.

Before:
```markdown
<!-- subscene key -->
## default

<!-- markdown/html -->
Click the <b>button</b> below to start the *demo*

<!-- command -->
/set myvar = 0

<!-- actions -->
* Start
  * [[forest]] <!-- action target -->
```

After:
```markdown
## default

Click the <b>button</b> below to start the *demo*

/set myvar = 0

* Start
  * [[forest]]
```

## Markdown / HTML

Classic markdown syntax is allowed.

```markdown
# level 1 title
### level 3 title
#### level 4 title
##### level 5 title

Normal text

*italic text*

**bold text**

`inline code`

> quote

<!-- horizontal line -->
---

![image](url)

[link](url)
```

Some extensions are provided by [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/), [python-markdown](https://python-markdown.github.io/extensions/) and [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/).

### Icons

See [Lucide icons](https://lucide.dev/icons/)

```markdown
<!-- title text icon -->
# <i icon=house></i> This is my house

<!-- standard text icon -->
<i icon=house></i> This is my house

<!-- button text icon -->
* <i icon=house></i> This is my house
```

### Colors

See [Material colors](https://materialui.co/colors/)

```markdown
<!-- standard text color -->
This is <span class=red>red</span>

<!-- specific text color -->
This is <span class=red-600>red</span>

<!-- background color -->
<div class=bg-red-300>This is red background</div>

<!-- apply color to button with #color-name (background/foreground/hover) -->
* This is red #red
```

### Level 2 title (bypass default behavior)

```markdown
<!-- subscene key -->
## default

<!-- normal level 2 title -->
<h2>default</h2>
```

### Lists (bypass default behavior)

```markdown
<!-- actions -->
* Start
  * [[forest]]

<!-- normal markdown list -->
- Start
  - forest
```

### Admonitions

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/)

```markdown
<!-- will be converted to admonition blocks -->
/// note | Some title (note)

Some content
///

/// success | Some title (success)

Some content
///

/// warning | Some title (warning)

Some content
///

/// danger | Some title (danger)

Some content
///
```

### Emojis

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/emoji/)

```markdown
<!-- will be converted to image emojis -->
:smile: :heart: :thumbsup:
```

### Mark

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/mark/)

```markdown
<!-- will be highlighted -->
==mark me==

==smart==mark==
```

### Progress bar

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/progressbar/)

```markdown
[=0% "0%"]
[=5% "5%"]
[=25% "25%"]
[=45% "45%"]
[=65% "65%"]
[=85% "85%"]
[=100% "100%"]
```

### Relative image

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/b64/)

```markdown
<!-- will be converted to base64 image (no link) -->
![](./path/to/image)
```

### Tables

See [documentation](https://python-markdown.github.io/extensions/tables/)

```markdown
<!-- will be converted to HTML table -->
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

