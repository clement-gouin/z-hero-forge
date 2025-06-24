# [Z] Hero Forge Documentation

See [README.txt](./README.txt) for CLI arguments.

## Basics

`forge.py` compute markdown files in the specified directory (not sub-directories).

Each file is called a **scene** and can have **sub-scenes**.

There are 5 line types in a scene files:

* Subscene key (defined by markdown level 2 title `##`)
* Actions definition: (defined by markdown list and sub list `*`)
* Commands: (defined by `/command`)
* Comments: (defined by markdown/html comments `<!-- comment -->`)
* (default) Markdown/HTML

```markdown
<!-- subscene key -->
## default

<!-- markdown/html -->
Click the button below to start the demo

<!-- command -->
/set myvar = 0

<!-- actions -->
* Start
  * [[forest]]
```