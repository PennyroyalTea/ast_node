def verbing(s):
    """
    Given a string, if its length is at least 3, adds 'ing' to its end.
    Unless it already ends in 'ing', in which case add 'ly' instead.
    If the string length is less than 3, leaves it unchanged.
    Returns the resulting string.

    >>> verbing('read')
    'reading'
    """
    return ''


def not_bad(s):
    """
    Given a string, finds the first appearance of the
    substring 'not' and 'bad'. If the 'bad' follows
    the 'not', replaces the whole 'not'...'bad' substring
    with 'good'.
    Returns the resulting string.

    >>> not_bad('This dinner is not that bad!')
    'This dinner is good!'
    """
    return ''


def front_back(a, b):
    """
    Consider dividing a string into two halves.
    If the length is even, the front and back halves are the same length.
    If the length is odd, we'll say that the extra char goes in the front half.
    e.g. 'abcde', the front half is 'abc', the back half 'de'.

    Given 2 strings, a and b, returns a string of the form
     a-front + b-front + a-back + b-back

    >>> front_back('abcd', 'xy')
    'abxcdy'
    """
    return ''
