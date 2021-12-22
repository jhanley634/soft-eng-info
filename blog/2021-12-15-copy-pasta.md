
# copy-pasta

Don't do it.

Just don't. Once you see the same code appear three or four times,
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
it up. Name the concept, find the parameters, call that new helper a few times.

Copy-n-pasting similar code a few times may _seem_ expedient,
but it's accummulating technical debt.
Code is written once but read many times,
and a properly named helper function will help your Readers, too.

And since that helper has
a [contract](https://en.wikipedia.org/wiki/Design_by_contract),
it is a convenient target for a new unit test.
