from unittest import TestCase
from nappingcat import serve
from nappingcat import config
from nappingcat import request
from nappingcat.exceptions import NappingCatBadConfig
from nappingcat.patterns import patterns
import mox
import random
import sys
import ConfigParser
import StringIO
SIMPLE_COMMAND = "oh hai"
COMPLEX_COMMAND = r'^hey (?P<something>\w+)( (?P<optional>\w+))?'

def delegate(*args, **kwargs):
    return args, kwargs

cmdpatterns = patterns('',
        (COMPLEX_COMMAND, delegate),
        ('^'+SIMPLE_COMMAND, delegate),
)

def create_settings(string):
    cp = ConfigParser.ConfigParser()
    cp.readfp(StringIO.StringIO(string))
    return cp

class TestOfServeAppMain(TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_bad_config(self):
        self.mox.StubOutWithMock(config, 'build_settings')
        settings = """
[something]
this_does_not_matter=nope
        """.strip()        
        config.build_settings().AndReturn(create_settings(settings))
        self.mox.ReplayAll()
        self.assertRaises(NappingCatBadConfig, serve.ServeApp().main, random.randint(1,100), random.randint(1,100))

    def test_inserts_into_sys_path(self):
        self.mox.StubOutWithMock(config, 'build_settings')
        random_paths = ['rand-%d' for i in range(0,3)]
        settings = """
[%s]
paths = 
    %s
    %s
    %s
        """.strip() % (config.SECTION_NAME, random_paths[0], random_paths[1], random_paths[2]) 
        config.build_settings().AndReturn(create_settings(settings))
        self.mox.ReplayAll()

        # we don't really care about this assertion.
        self.assertRaises(Exception, serve.ServeApp().main, random.randint(1, 100), random.randint(1, 100))

        self.assertTrue(all([path in sys.path for path in random_paths]))

    def test_raises_importerror_on_bad_router(self):
        self.mox.StubOutWithMock(config, 'build_settings')
        settings = """
[%s]
routers=dne.dne.dne
        """.strip() % config.SECTION_NAME
        config.build_settings().AndReturn(create_settings(settings))
        self.mox.ReplayAll()

        # this time we care that things are broken.
        self.assertRaises(ImportError, serve.ServeApp().main, random.randint(1, 100), random.randint(1, 100))

    def test_delegates_properly(self):
        self.mox.StubOutWithMock(config, 'build_settings')
        settings = """
[%s]
routers=tests.serve
        """.strip() % config.SECTION_NAME
        config.build_settings().AndReturn(create_settings(settings))
        config.build_settings().AndReturn(create_settings(settings))
        config.build_settings().AndReturn(create_settings(settings))
        self.mox.ReplayAll()

        args, kwargs = serve.ServeApp().main(random.randint(1,100), SIMPLE_COMMAND)
        self.assertTrue(isinstance(args[0], request.Request))
        self.assertEqual(args[0].command, SIMPLE_COMMAND)
        
        args, kwargs = serve.ServeApp().main(random.randint(1,100), 'hey there')
        self.assertTrue(isinstance(args[0], request.Request))
        self.assertEqual(args[0].command, 'hey there')
        self.assertTrue('something' in kwargs)
        self.assertEqual(kwargs['something'], 'there')
        self.assertEqual(kwargs['optional'], None)
        
        args, kwargs = serve.ServeApp().main(random.randint(1,100), 'hey there girl')
        self.assertTrue(isinstance(args[0], request.Request))
        self.assertEqual(args[0].command, 'hey there girl')
        self.assertTrue('something' in kwargs)
        self.assertEqual(kwargs['something'], 'there')
        self.assertEqual(kwargs['optional'], 'girl')
