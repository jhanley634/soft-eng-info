
# import typer

![Archy](asset/2022-05-08/archy.jpg){ width=571, height=300 }

Once upon a time I would start each script with `import click`
at the insistence of my friend Andy Terrel.
And before that I would `import sys` to access `sys.argv`,
though without the self-documenting
automatic "`--help`" option being tacked on.

But libraries evolve, and the fine folks who brought us click
have a new and improved offering:
[typer](https://pypi.org/project/typer/).
Use it!

In recent years you have probably been taking advantage of
python's optional type annotation, leading to signatures like this:

        def main(
             start: datetime,
             in_file: Path,
             verbose: bool = True,
             n: int = 42):

To turn such a function into a self-documenting script,
just tack on this brief call:

    import typer
    ...
    if __name__ == '__main__':
        typer.run(main)

Note we are passing in a function reference.
Auto-complete in your IDE wants to make it `main()`
with `(` `)` parens, but don't
let it. Hand the un-evaluated `main` into `.run()`,
so it has a chance to introspect that function's signature,
making `--help` as helpful as possible.

No need to annotate with `@click` decorations,
no need to keep things in sync if you change the
number of args in the signature.
It just works.
I love it.
Use it good health.

----

## shebang

It might go without saying.
When creating a new script, you will want to

1. make it executable, ..and..
2. start with a shebang.

That means

1. `$ chmod a+x my_script.py`
2. first line should be: `#! /usr/bin/env python`

Strictly speaking you don't _have_ to start by running the `env` program.
But it doesn't hurt, and it is very portable.
It gives you the power of `$PATH` -- the python interpreter
will be looked up via `execlvp()` which respects the `PATH` env var.
You want that behavior, especially if you chose a new interpreter
with `$ conda activiate my_project`.

We will typically want a 1:1 relationship between "chmod a+x"
and "starts with shebang".
We expect that both are present, or both are absent.

## --help

A naïve invocation without mandatory args
will yield the following diagnostic message.
```
Usage: myapp.py [OPTIONS] START:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                IN_FILE
Try 'myapp.py --help' for help.

Error: Missing argument 'START:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]'.
```

<br />

----

<br />

And here is some of the `--help` output that you get "for free",
just because you annotated the signature.
```
Usage: myapp.py [OPTIONS] START:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                IN_FILE

Arguments:
  START:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  [required]
  IN_FILE                         [required]

Options:
  --verbose / --no-verbose  [default: verbose]
  --n INTEGER               [default: 42] ...
  --help                    Show this message and exit.
```
