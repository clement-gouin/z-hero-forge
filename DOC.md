# [Z] Hero Forge Documentation <!-- omit in toc -->

`forge.py` compute markdown files in the specified directory (not sub-directories) into [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) playable links (using [z-app-linker](https://github.com/clement-gouin/z-app-linker/)).

See [README.txt](./README.txt) for CLI arguments.

- [Basics](#basics)
- [Scenes / Subscenes](#scenes--subscenes)
- [Actions](#actions)
- [Commands](#commands)
  - [`/include`](#include)
  - [`/show`](#show)
  - [`/set`](#set)
  - [`/start`](#start)
  - [`/end`](#end)
  - [`/color`](#color)
- [Comments](#comments)
- [Markdown / HTML](#markdown--html)
  - [Level 2 title (bypass default behavior)](#level-2-title-bypass-default-behavior)
  - [Lists (bypass default behavior)](#lists-bypass-default-behavior)
  - [Admonitions](#admonitions)
  - [Emojis](#emojis)
  - [Mark](#mark)
  - [Progress bar](#progress-bar)
  - [Quotes](#quotes)
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

### `/include`

TODO

### `/show`

TODO

### `/set`

TODO

### `/start`

TODO

### `/end`

TODO

### `/color`

TODO

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

Classic markdown syntax is allowed (see lists for )

Some extensions are provided by [python-markdown](https://python-markdown.github.io/extensions/) and [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/).

### Level 2 title (bypass default behavior)

```markdown
<!-- subscene key -->
## default

<!-- level 2 title -->
<h2>default</h2>
```

### Lists (bypass default behavior)

```markdown
<!-- actions -->
* Start
  * [[forest]]

<!-- list -->
- Start
  - forest
```

### Admonitions

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/)

```markdown
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
:smile: :heart: :thumbsup:
```

### Mark

See [documentation](https://facelessuser.github.io/pymdown-extensions/extensions/mark/)

```markdown
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

### Quotes

```markdown
> quoted content
```

### Tables

See [documentation](https://python-markdown.github.io/extensions/tables/)

```txt
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```
