
# pre-commit

Some "lint" warnings should be tolerated until a feature becomes ready,
such as a defined variable or import that we've not yet gotten around to using.
But some are just too silly, there's no excuse for them,
they should be stamped out immediately, each time you commit.
This includes trivial whitespace details, such as:

- no TABs (unless it's a Makefile)
- no invisible trailing blanks
- no CR/LFs, ever

![lint](https://web.archive.org/web/20211216195906if_/https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_47/f_auto,q_auto,w_1100/v1554931573/shape/mentalfloss/533979-istock-472032305.jpg)

When a Windows user joins your project,
that last one can become a huge issue right away,
replacing all LFs with CRLFs in edits to existing files.
Polluted diffs like that is _not_ a pretty sight.

The one-or-more editors which change a project's
source files should already be configured to do
sensible things with whitespace.
Pre-commit is sort of a "belt and suspenders"
approach, a last chance effort to ensure
the right thing happens.

## use

Right after a `$ git clone`,
`cd` into it and run `$ pre-commit install`
to activate the commit hooks.

Thereafter, just `$ git commit -a -m "Adds feature X"` as usual.
For a "clean" commit, you see a few green lines of output,
a half second of delay, and it commits in the normal way.
For a commit attempt that has issues
you will see a red line of output, followed by nothing happening.
That is, the commit did not succeed, git views it as if
you had never even requested the commit.

Most such attempts will have been auto-corrected by the hook,
e.g. trimming trailing blanks.
Simply hit up-arrow to repeat the commit command,
and this time it succeeds.
The tool was just giving you an opportunity to review
the changes it made, before you finally commit them.

Occasionally you will notice that a bigger issue is being flagged,
which requires your thought and attention.
Carefully read the diagnostic, make the needed edits,
repeat the commit command, and see it succeed.
Just be glad your colleages never saw that embarrassing "whoops!"
that you were about to commit and push.

## lenient settings

Tools are here to serve us, not the other way round.
Linters should do reasonable things rather than get in the way.

For routine commits and amends, which haven't been pushed to
a central server, I want to see diffs against previous commit.
I view it as completely reasonable that a WIP work in progress
will have unused imports and unused variable definitions.
So I don't ask my hooks to flag such issues at commit time.
We can worry about that later, when we're ready
and we choose to run `mypy` or similar linters,
or when a central CI/CD pipeline does so.

Once a new feature has matured a bit,
typically `$ make lint` will run the more stringent checks,
when you're ready for that.

## project settings

It is _possible_ to define commit hooks and linter prefs on a
per-user basis, for example at the time that we onboard new staff.

I prefer not to do that. Why?
Inevitably a project will change, or a team's expectations will change.
And then for team size N, you've got N edits to implement and audit.
No thank you. Better to acknowledge that prefs will change,
and to track them in source control. That's what git is good at.

Also, when checking out historic snapshots that pre-date a pref change,
ancient lint rules will _also_ be checked out, consistent with the ancient code.

Generally for lint, `.gitignore`, and similar, I recommend
imposing rules as per-project standards and recommendations,
rather than attempting to get per-user prefs to work consistently
across current and future team members.

## bypass

Is some picky lint rule more trouble than it's worth ATM,
just getting in the way?
Tell _this one commit_ to skip it:

    $ git commit --no-verify ...

The most common use case would be making a deliberate choice
to commit a "large" data file to a source repo.

You can skip individual checks on a
[finer grained](https://pre-commit.com/#temporarily-disabling-hooks)
basis if you like:

    $ SKIP=flake8 git commit ...

## install

On a Mac laptop just do

    $ brew install pre-commit

Or use `$ sudo apt install pre-commit`,
or add it as a dep in `environment.yml`.

## example

Here is a config file that I typically use.
```
# After cloning repo, install hooks with:
#
#     $ brew install pre-commit
#
#     $ pre-commit install


# This repo _does_ support WIP commits of e.g. unused import or assignment,
# preferring to defer `flake8` linting until Jenkins sees a push.


repos:

  - repo: https://github.com/pycqa/isort
    rev: 5.5.2
    hooks:
      - id: isort

  - repo: https://github.com/kynan/nbstripout
    rev: 0.6.0
    hooks:
      - id: nbstripout

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.4.0
    hooks:
      - id: check-added-large-files
        args: [ '--maxkb=100' ]
      - id: check-ast
      - id: check-builtin-literals
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-executables-have-shebangs
      - id: check-json
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-yaml
      - id: double-quote-string-fixer
      - id: end-of-file-fixer
      - id: mixed-line-ending
      - id: name-tests-test
      - id: trailing-whitespace

```
Clearly YMMV. Check for more recent version numbers before you lock in these.

### large files

Git is wonderful for many things,
but it is not a good fit for storing large data files
that frequently change, especially binary files.
For frequent edits, git really wants to find diffs to compress them,
and a line-oriented diff is not a good match for binary file formats.
That includes changing images, any compressed `.gz` files, and PDFs.

After a "whoops!" addition of a giant .mp4, a `$ git rm ...`
does not exactly make the error go away. The giant binary blob
of commit history will still live in your repo forever,
and will still consume bandwidth and disk space on each of
your colleagues' laptops when they do a `git pull`.
Git is the elephant that never forgets.

The proposed 100 KiB limit is frankly a bit draconian.
Feel free to adjust it.
The point is for a hook to gently _remind_ you of the
consequences of what you're about to do,
rather than to _prohibit_ you from thoughtfully taking such an action.
You can always bypass the check on a specific commit,
if you're sure that's what you really want.
