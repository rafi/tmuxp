# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import os
import unittest
import logging
import kaptan
from .. import Window, config
from ..workspacebuilder import WorkspaceBuilder
from .helpers import TmuxTestCase

logger = logging.getLogger(__name__)


class WorkspaceBuilderTest(TmuxTestCase):

    yaml_config = '''
    session_name: sampleconfig
    start_directory: '~'
    windows:
    - layout: main-verticle
      panes:
      - shell_command:
        - vim
        start_directory: '~'
      - shell_command:
        - cowsay "hey"
      window_name: editor
    - panes:
      - shell_command:
        - tail -F /var/log/syslog
        start_directory: /var/log
      window_name: logging
    - automatic_rename: true
      panes:
      - shell_command:
        - htop
    '''

    def test_split_windows(self):
        s = self.session
        sconfig = kaptan.Kaptan(handler='yaml')
        sconfig = sconfig.import_config(self.yaml_config).get()

        builder = WorkspaceBuilder(sconf=sconfig)

        window_count = len(self.session._windows)  # current window count
        self.assertEqual(len(s.list_windows()), window_count)
        for w, wconf in builder.iter_create_windows(s):
            window_pane_count = len(w._panes)
            for p in builder.iter_create_panes(w, wconf):
                p = p
                self.assertEqual(len(s.list_windows()), window_count)
            self.assertIsInstance(w, Window)

            self.assertEqual(len(s.list_windows()), window_count)
            window_count += 1


class WorkspaceBuilderTestPane(TmuxTestCase):

    yaml_config = '''
    session_name: sampleconfig
    start_directory: '~'
    windows:
    - layout: main-horizontal
      panes:
      - shell_command:
        - vim
        start_directory: '~'
      - shell_command:
        - cowsay "hey"
      - shell_command:
        - cowsay "moo"
    '''

    def test_split_windows(self):
        s = self.session
        sconfig = kaptan.Kaptan(handler='yaml')
        sconfig = sconfig.import_config(self.yaml_config).get()

        builder = WorkspaceBuilder(sconf=sconfig)

        window_count = len(self.session._windows)  # current window count
        self.assertEqual(len(s.list_windows()), window_count)
        for w, wconf in builder.iter_create_windows(s):

            window_pane_count = len(w._panes)
            for p in builder.iter_create_panes(w, wconf):
                p = p
                self.assertEqual(len(s.list_windows()), window_count)
            self.assertIsInstance(w, Window)

            self.assertEqual(len(s.list_windows()), window_count)
            window_count += 1
            w.set_window_option('main-pane-height', 50)
            w.select_layout(wconf['layout'])


class NoSessionNameError(TmuxTestCase):
    '''sample config with no session name'''

    yaml_config = '''
    start_directory: '~'
    windows:
    - layout: main-verticle
      panes:
      - shell_command:
        - vim
        start_directory: '~'
      - shell_command:
        - cowsay "hey"
      window_name: editor
    - panes:
      - shell_command:
        - tail -F /var/log/syslog
        start_directory: /var/log
      window_name: logging
    - automatic_rename: true
      panes:
      - shell_command:
        - htop
    '''

    def test_no_session_name_raises(self):
        s = self.session
        sconfig = kaptan.Kaptan(handler='yaml')
        sconfig = sconfig.import_config(self.yaml_config).get()

        with self.assertRaises(ValueError):
            w = WorkspaceBuilder(sconf=sconfig)

        sconfig['session_name'] = 'give_a_session_name'
        w = WorkspaceBuilder(sconf=sconfig)  # shouldn't raise anything


class TestsToDo(object):

    def test_uses_first_window_if_exists(self):
        '''
        if the session is already on the first window, use that.

        this is useful if the user is already inside of a tmux session
        '''

    def test_same_session_already_exists_unclean(self):
        '''
        raise exception if session_name already exists and has multiple
        windows the user could potentially be offered to add a cli argument to
        override the session_name in config. Perhaps `-n` could be used to load
        a config from file with overridden session_name.
        '''

    def test_inside_tmux_same_session_already_exists(self):
        ''' same as above, but when the config file and the current $TMUX
        session are the same '''

    def test_inside_tmux_no_session_name_exists(self):
        '''
        if the session_name doesn't currently exist and the user is in tmux
        rename the current session by the config / -n and build there.
        '''

    def testPaneProportions(self):
        """
        todo. checking the proportions of a pane on a grid allows
        us to verify a window has been build correctly without
        needing to see the tmux session itself.

        we expect panes in a list to be ordered and show up to
        their corresponding pane_index.
        """
        pass


if __name__ == '__main__':
    #t.socket_name = 'tmuxp_test'
    unittest.main()
