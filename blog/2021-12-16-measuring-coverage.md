
# measuring test coverage

Automated tests are great,
from small unit tests up to bigger ones like integration tests.

Measuring coverage will help you understand

1. how good those tests are, and
2. how good the tested target code is.

A coverage report will sometimes point out we should write a currently "missing" test
to exercise a recently added function, that's simple.
But looking at uncovered target lines, e.g. in an exception handler,
can help with critiquing the Public API, can suggest Extract Helper
on deeply buried code so now it's exposed to unit tests.
Often there will be an `if` condition that is "hard" or nearly impossible
to make true, so tests never run the if clause, not till we break out a helper.

## concept

The approach to measurement is pretty simple,
and is available in many languages.
In C / C++ land, GNU gcov has been around for decades,
recently prettified by [gcovr](https://github.com/gcovr/gcovr),
and clang offers nice
[measurement support](https://logan.tw/posts/2015/04/28/check-code-coverage-with-clang-and-lcov/)
as well.
[Rust](https://vladfilippov.com/blog/rust-code-coverage-tools/)
and most other languages offer similar support.
Python programmers will want to rely on
[coverage](https://coverage.readthedocs.io/en/6.2/).

How does it work?
The coverage tool will expand your code
by mixing in a bunch of counter increments.
There's more than one measurement granularity.
Let's start with the coarsest level.

### granularity

To measure at "function" granularity,
imagine that an update of a global was added
just after each `def foo():` in your python source:

    def foo():
        counter[__file__ + get_line_num()] += 1
        ...

The inspect module offers convenient
[access](https://stackoverflow.com/a/6811020/8431111)
to the current source code line number.

Now during any run, such as unit tests, we can easily tell
whether `foo()` executed or not.
The excellent `coverage` module updates a `defaultdict(int)`
global in this way, and then produces a pretty report
showing covered functions in green while uncovered is red.

We can easily move to "line" granularity
