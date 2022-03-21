
# use a mapping

Use a mapping where appropriate, rather than a giant `if` or `case` statement.

I continue to see this again and again in production code, in many languages.
Often we're dealing with `Enum` and a more complex task than spelling numbers.

        def _convert(a):
            if a == 1:
                return 'one'
            elif a == 2:
            ...
            elif a == 10:
                return 'ten'
            else raise ValueError(f'unknown input: {a}')

Or worse, no helper, and each `return` is a `result =` assignment.

There's no need for such code.
Take advantage of map datastructures.
They're fast!
And concise.
Fewer places for a one-off code change to creep into the middle of it.

        num_to_str = {
            1: 'one',
            2: 'two',
            ...
            10: 'ten',
        }
        def _convert(a):
            return num_to_str[a]

That's a `str`-valued mapping,
but we could manipulate functions or classes just as easily.
Leave out the usual `()` parentheses, so we have
the function rather than its evaluation.

        { '+': sum, '*': prod }

        {
            'too big': OverflowError,
            'no file': FileNotFoundError,
            'CTRL/C': InterruptedError,
        }
