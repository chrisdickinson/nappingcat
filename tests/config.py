from unittest import TestCase
import mox
import os
import ConfigParser
import random
import shutil
from nappingcat import config

class TestOfConfig(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.filename = 'tests/.%d.conf' % random.randint(1,100)

    def tearDown(self):
        self.mox.UnsetStubs()
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_reads_from_appropriate_path_and_file(self):
        f = open(self.filename, 'w')
        print >>f,"""
[kittyconfig]
blah=3
        """.strip()
        f.flush()
        f.close()

        self.mox.StubOutWithMock(os.path, 'expanduser')
        os.path.expanduser(mox.IsA(str)).AndReturn(self.filename)
        self.mox.ReplayAll()
        results = config.build_settings()
        self.assertTrue(isinstance(results, ConfigParser.ConfigParser))
        self.mox.VerifyAll()

    def test_raises_parsingerror_with_bad_config(self):
        f = open(self.filename, 'w')
        print >>f,"""
[kittyconfig
blah=3
anrranl;faksdj
        """.strip()
        f.flush()
        f.close()

        self.mox.StubOutWithMock(os.path, 'expanduser')
        os.path.expanduser(mox.IsA(str)).AndReturn(self.filename)
        self.mox.ReplayAll()
        self.assertRaises(ConfigParser.Error, config.build_settings)
        self.mox.VerifyAll()
