
# design a Public API for the client's convenience

When writing a library routine that clients will call,
there is often a temptation to specify method
arguments that will make your life easier.

You're writing the implementation,
you know exactly what values it's going to to need.
So just throw them in the signature and we're done, right?
No.
A successful library will have many callers, many call sites.
And just one implementation.
Pity the poor caller.

Consider the caller's needs.

1. Are all the arguments readily available? Do they have dependencies?
2. Will the call site typically supply a few common args again and again?
3. Is it easy to correctly interpret the return value?
4. If something goes wrong, will caller typically want to handle it?

Let's tackle those one by one.
In all cases, being able to say "I have multiple callers" will aid the design process.

## 1. convenience of assembling args

I have seen a fair number of library methods where client must
populate variable `a` and from that sequentially derive
variables `b, c, & d`, ending up with a `foo(b, c, d)` call.
If there's limited variation in those sequential lookups,
prefer a `foo(a)` API, and let the library routine do the lookups
or other work to derive those three.

Failure modes matter.
Perhaps `a` is a DB connection, which can fail
for reasons like timeout during server maintenance.
It might be more convenient for the client to have the `__init__()` constructor
store a `self.a = a` attribute _before_ we get to the   foo  call.
Then we know we have a usable connection before we start,
and won't have to worry about some half-done work that will need cleanup.

## 2. common args

This should go without saying. A class offering e.g. this Public API:

- `foo(b, c, d)`
- `bar(b, c, e)`
- `baz(b, c, f)`

should probably have an `__init__` ctor that accepts and stores two args:

        self.b = b
        self.c = c

or produces them same way the client would.
Leaving us with three single-arg calls.
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)!

## 3. easily interpreted return value

Consider our old friend from System V Unix, `write(2)`.
We might call it in this way:

        n = write(file_desc, buf, buf_len)

And now we have the obligation to verify positive `n`
before proceding on our merry way.
But come on! You have read code. Who does that?
Code typically assumes `n == buf_len` and blithely carries on,
never inspecting `errno` and reporting "disk full" errors when they happen.

Don't design a Public API like that.
You have exceptions at your disposal.
Make it _easy_ for client to correctly call you;
`raise` upon exceptional circumstances, such as returning `n == -1`.

Avoid polymorphic `return`, that is,
avoid writing code like this:

        if c:
            return single_result
        else:
            return [result1, result2]

Prefer to _always_ offer a list with one or two elements:
`return [single_result]`

A thornier design issue arises when implementing a function like `lookup(key)`.
It might fail due to DB timeout, fine, just `raise` and be done with it, easy.
It might produce zero, one, or more matches. What to do?
Returning `None` in the zero case _might_ be appropriate, so consider it.
But often it will be preferrable to return a `list` of zero, one, or more elements.
Why? Think about the poor client, and whether de-referencing `None` would
cause an `AttributeError`. If the natural way to consume the result is
to iterate over it, definitely avoid returning `None`, when iterating
zero times does the right thing without any client conditionals.
Remember that each `if` test imposes the burden of implementing
two unit tests instead of just one,
in order to exercise both the `if` & `else` clauses.

If `lookup` returns exactly zero or one matches,
then `None` will sometimes be the best return value,
certainly it is easy to test for with `if result:`.
But consider inventing your own class to represent ValueNotFound.
For client convenience it may wish to override `__bool__()`.

Finally, it should be _hard_ for a client to misinterpret a return value.
For example if `lookup_phone_num(name)` can return `+1 000-000-0000`,
I predict some clients will direct people to call that number.
Returning `None` instead makes that less likely.

## 4. exceptions

If a library routine is unable to fulfill its promise,
unable to conform to its Public API,
then it shouldn't return anything at all, preferring to `raise`.
Or just let some underlying I/O library `raise` for you,
allowing the exception to bubble up the call stack.
Reserve `try` / `catch` for when you know of a strategy
that might still be able to make good on the API promises.
Or when the design decision was for caller to receive `None` upon error.

Pay attention to whether your callers ever have a Use Case
for dealing with different errors in different ways.
It's moderately rare, but when that happens you should probably
define app-specific Exceptions to **wrap** the original one.
Start out with e.g. FirstAppError + SecondAppError,
each inheriting from MyAppError.
Then a caller can catch the umbrella parent, or either of the children,
as its handler might only know how to cope with 1st or 2nd error.

## multiple callers

We covered several design issues you may need to
grapple with  while creating a new Public API.
How will you know if you got it right?

Create multiple callers, before you finish the implementation.

_Something_ forced you to write that library code,
so it's a fair bet you have certain client code in mind.
And you're going to have to test all that end to end anyway.
But take a moment to write an automated unit test for it, as well.
It will be your **2nd** caller.

You may be surprised that, when writing this new client code from scratch,
your favorite input variables are not so easy to produce.
Or there may be some other warts that become apparent.
If this happens, listen to the code,
listen to what it's telling you.
It wants one less argument,
it wants different exception handling, something like that.
Code smells will help improve the design,
if you stop to notice and fix them.

When coding that unit test,
if there was something needlessly repetitive or tedious about
interpreting a result or dealing with errors,
use that!
Accept it as criticism of the current API,
and offer a revised API that has fewer warts.
Your callers will thank you.
