from unittest import TestCase
from nappingcat import patterns
from nappingcat.exceptions import NappingCatUnhandled, NappingCatBadPatterns
import random

random_value = random.randint(1,100)
def test_fn(*args, **kwargs):
    return random_value

cmdpatterns = patterns.patterns('tests',
            (r'^anything', test_fn),
            (r'^something_else', patterns.include('tests.patterns_test')),
            (r'^something', 'test_fn'),
) 

class TestOfCommandPatterns(TestCase):
    def test_init_assigns_appropriately(self):
        random_map = random.randint(1,100)
        result = patterns.CommandPatterns('', random_map)
        self.assertEqual(result.path, '')
        self.assertEqual(result.map, random_map)

        results = patterns.CommandPatterns('tests.patterns_test', '')
        self.assertEqual(random.__class__, results.module.__class__)

        self.assertRaises(ImportError, patterns.CommandPatterns, 'dne', '')

    def test_match_raises_unhandled_if_no_match(self):
        test = patterns.CommandPatterns('', [])
        anything = 'random-%d' % random.randint(1,100)
        self.assertRaises(NappingCatUnhandled, test.match, anything)

    def test_delegates_to_included_patterns(self):
        random_result = random.randint(1,100)
        class TriggerCommandPatterns(patterns.CommandPatterns):
            def match(self, command):
                return random_result
        pat = patterns.CommandPatterns('', [('^hey', TriggerCommandPatterns('', []))])
        self.assertEqual(pat.match('hey'), random_result)

    def test_continues_to_next_match_if_delegate_raises_unhandled(self):
        random_result = random.randint(1,100)
        class TriggerCommandPatterns(patterns.CommandPatterns):
            def match(self, command):
                raise NappingCatUnhandled("OH no!")
        test_fn = lambda *args, **kwargs: random_result
        pat = patterns.CommandPatterns('', [('^hey', TriggerCommandPatterns('', [])), ('^hey', test_fn)])
        target, match = pat.match('hey')
        self.assertEqual(target, test_fn)
        self.assertTrue(hasattr(match, 'groupdict'))    # not a great way to test whether or not it's a regex match object...

    def test_attempts_to_grab_str_target_off_of_module(self):
        pat = patterns.CommandPatterns('tests.patterns', [
            ('^hey', 'test_fn'),
            ('^yo', 'dne'),
        ])
        target, match = pat.match('hey')
        self.assertEqual(target, test_fn)
        self.assertTrue(hasattr(match, 'groupdict'))    # not a great way to test whether or not it's a regex match object...
        self.assertRaises(AttributeError, pat.match, 'yo')

    def test_raises_nappingcat_exception_if_target_is_not_a_string_patterns_or_callable(self):
        pat = patterns.CommandPatterns('tests.patterns', [
            ('^hey', random.randint(1,100)),
        ])
        self.assertRaises(NappingCatBadPatterns, pat.match, 'hey')

    def test_add_returns_new_patterns(self):
        hey_value, yo_value = random.randint(1,100), random.randint(1,100)
        pat = patterns.CommandPatterns('tests.patterns', [
            ('^hey', lambda x: hey_value),
        ])
        rhs = patterns.CommandPatterns('tests.patterns', [
            ('^yo', lambda x: yo_value),
        ])
        newpat = pat + rhs
        for cmd, expected in (('hey', hey_value), ('yo', yo_value)):
            result, match = newpat.match(cmd) 
            self.assertEqual(result(random.randint(1,100)), expected)
        self.assertRaises(NappingCatUnhandled, newpat.match, 'notheyoryo')

    def test_add_raises_typeerror_on_non_patterns(self):
        pat = patterns.CommandPatterns('tests.patterns', [(r'^anything', lambda x: x)])
        self.assertRaises(TypeError, pat.__add__, random.randint(1,100))

    def test_addequal_returns_correct_patterns(self):
        hey_value, yo_value = random.randint(1,100), random.randint(1,100)
        pat = patterns.CommandPatterns('tests.patterns', [
            ('^hey', lambda x: hey_value),
        ])
        pat += patterns.CommandPatterns('tests.patterns', [
            ('^yo', lambda x: yo_value),
        ])
        for cmd, expected in (('hey', hey_value), ('yo', yo_value)):
            result, match = pat.match(cmd) 
            self.assertEqual(result(random.randint(1,100)), expected)
        self.assertRaises(NappingCatUnhandled, pat.match, 'notheyoryo')
