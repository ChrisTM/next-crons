import re


"""
The parsers use membership testing against the class variable `allowed_vals`
to ensure field values are within appropriate bounds. This is default value for
`allowed_vals` will allow any value
"""
class AllValues(object):
    def __contains__(self, item):
        return True


"""
Generic parser for parsing cron job fields. The parse method takes a field
string and expands it into a list of numbers that are matched by the field.
Example: .parse("2-4,9") -> [2,3,4,9].
"""
class GenericParser(object):
    # if `_min` and `_max` are specified, they will be used to determine the
    # `allowed_vals`
    _min = None
    _max = None

    # mapping of lowercase alphabetical aliases to their integer meaning.
    # Eg: {..., 'feb': 2, ...}
    aliases = {}

    # list of all allowed values for this field
    allowed_vals = AllValues()

    def __init__(self):
        if None not in (self._min, self._max):
            self.allowed_vals = range(self._min, self._max + 1)

    """Parse a field, returning a list of values allowed by the field"""
    def parse(self, field):
        # a cron field is made up of multiple comma separated expressions.
        exps = field.split(',');
        # the values this field allows will be collected here
        vals = set();
        for exp in exps:
            tests_and_parsers = [
                [self.is_all, self.parse_all],
                #since skip expressions may contain ranges, we check this before ranges
                [self.is_skip, self.parse_skip],
                [self.is_range, self.parse_range],
                [self.is_single, self.parse_single],
            ]

            for is_type, parse_type in tests_and_parsers:
                if is_type(exp):
                    vals.update(parse_type(exp))
                    break

        return sorted(vals)


    """Return True if `exp` is '*'. Does not check bounds."""
    def is_all(self, exp):
        return exp == '*'

    """Return list of values matched by `*`"""
    def parse_all(self, exp):
        if isinstance(self.allowed_vals, AllValues):
            raise SyntaxError("This field does not support use of '*'")
        else:
            return self.allowed_vals


    """Return True if `exp` is a range-type expression. Does not check bounds."""
    def is_range(self, exp):
        return re.match(r'^(\w+)-(\w+)$', exp) is not None;

    """Return list of values matched by `exp`"""
    def parse_range(self, exp):
        _min, _max = map(self.parse_number, exp.split('-'));
        assert (_min in self.allowed_vals and _max + 1 in self.allowed_vals)
        assert (_min <= _max)
        return range(_min, _max + 1)


    """
    Return True if `exp` a skip-type expression. Does not check bounds or
    ensure the LHS of '/' is a valid expression itself.
    """
    def is_skip(self, exp):
        return re.match(r'^(.*)/(\d+)$', exp) is not None;

    """Return list of values matched by `exp`"""
    def parse_skip(self, exp):
        sub_exp, skip_num = exp.split('/');

        skip_num = int(skip_num)

        vals = []
        if self.is_all(sub_exp):
            vals = self.parse_all(sub_exp)
        elif self.is_range(sub_exp):
            vals = self.parse_range(sub_exp)
        else:
            raise SyntaxError("LHS of skip expression {0} is invalid" % (exp))

        # return `vals`, skipping every `skip_num`-indexed value
        return [val for idx, val in enumerate(vals) if idx % skip_num == 0]


    """Return True if `exp` a single-number expression. Does not check bounds."""
    def is_single(self, exp):
        return re.match(r'^(\w+)$', exp) is not None;

    """Return list of the single value matched by the number `exp`"""
    def parse_single(self, exp):
        assert (self.parse_number(exp) in self.allowed_vals)
        return [self.parse_number(exp)]

    """
    Given a fragment representing a number (either as an alphanumeric alias or
    otherwise), return the matching integer. This is not a field expression
    parser, but a parser for the parts of an expression that represent a
    number.
    """
    def parse_number(self, num_exp):
        lowered = num_exp.lower()
        if lowered in self.aliases:
            return self.aliases[lowered]
        try:
            return int(num_exp)
        except ValueError:
            raise ValueError('{0} is not a valid number or number alias' % (num_exp))


class MinutesParser(GenericParser):
    _min = 0
    _max = 59

class HoursParser(GenericParser):
    _min = 0
    _max = 23

class DaysOfMonthParser(GenericParser):
    _min = 1
    _max = 31

class MonthsParser(GenericParser):
    _min = 1
    _max = 12
    aliases = { 
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12,
    }

class DaysOfWeekParser(GenericParser):
    _min = 0
    _max = 6
    aliases = { 
        'sun': 0,
        'mon': 1,
        'tue': 2,
        'wed': 3,
        'thu': 4,
        'fri': 5,
        'sat': 6,
        '7': 0, #ATTN: 7, 0 both mean Sunday
    }


"""A convienence class that namespaces instances of the typed parsers"""
class Parse:
    minutes = MinutesParser().parse
    hours = HoursParser().parse
    days_of_month = DaysOfMonthParser().parse
    months = MonthsParser().parse
    days_of_week = DaysOfWeekParser().parse
