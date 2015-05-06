"""
Utility methods we want to share across the app
"""


def round_to_ratings_half(full_rating):
    """Given a number, round it to the nearest half "rating" value.

    Raises ValueError if full_rating is < 0, returns 0 if full_rating is None.

    Use the same method that oreilly.com uses for rounding:
    i.1, i.2 == i
    i.3, i.4, i.5 i.6, i.7 == i.5
    i.8, i.9 == i + 1

    Note: This is a little overboard ... but I thought it has some interesting side issues so
    I flushed some edge cases out.
    """

    if full_rating is None:
        return 0

    # Careful ... True/False can also be numbers
    if isinstance(full_rating, bool) or not isinstance(full_rating, (int, float)):
        raise ValueError('Input must be an int or float')

    if full_rating < 0:
        raise ValueError('Input must be zero or greater')

    # Be obvious until profiling shows we need to be fast.
    base_rating_value = int(full_rating)
    rounded_to_tenth = round(full_rating, 1)
    tenth_value = int(rounded_to_tenth * 10 % 10)
    if tenth_value in (3, 4, 5, 6, 7):
        return base_rating_value + 0.5
    elif tenth_value in (0, 1, 2):
        return base_rating_value
    elif tenth_value in (8, 9):
        return base_rating_value + 1
    else:
        raise ValueError('round_to_ratings_half is broken')
