# [Z] Hero Forge Documentation

See [README.txt](./README.txt) for CLI arguments.

## Basics

`forge.py` compute markdown files in the specified directory (not sub-directories) into [z-hero-quest](https://github.com/clement-gouin/z-hero-quest/) playable links (using [z-app-linker](https://github.com/clement-gouin/z-app-linker/)).

Each file is called a **scene** and can have **sub-scenes**.

There are 5 types of line in a scene files:

* [Subscene key](#scenes--subscenes) (defined by markdown level 2 title `##`)
* [Actions definition](#actions) (defined by markdown list and sub list `*`)
* [Commands](#commands) (defined by `/command`)
* [Comments](#comments) (defined by markdown/html comments `<!-- comment -->`)
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

TODO

## Comments

TODO

## Markdown / HTML

TODO