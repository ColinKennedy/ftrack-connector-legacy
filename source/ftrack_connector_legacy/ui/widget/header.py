# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os

from QtExt import QtCore, QtWidgets, QtGui

import ftrack
from ftrack_connector_legacy.ui import resource
import thumbnail


# Cache of user names.
NAME_CACHE = dict()


class Header(QtWidgets.QFrame):
    '''Header widget with name and thumbnail.'''

    def __init__(self, username, parent=None):
        '''Instantiate the header widget for a user with *username*.'''

        super(Header, self).__init__(parent=parent)
        self.setObjectName('ftrack-header-widget')
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(
            QtCore.Qt.AlignTop
        )
        self.setLayout(self.main_layout)

        # Logo & User ID
        self.id_container = QtWidgets.QWidget(self)
        self.id_container_layout = QtWidgets.QHBoxLayout()
        self.id_container_layout.setContentsMargins(0, 0, 0, 0)
        self.id_container_layout.setSpacing(0)
        self.id_container_layout.setAlignment(
            QtCore.Qt.AlignTop
        )
        self.id_container.setLayout(self.id_container_layout)

        spacer = QtWidgets.QSpacerItem(
            0,
            0,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

        self.logo = Logo(self)
        self.user = User(username, self)

        self.id_container_layout.addWidget(self.logo)
        self.id_container_layout.addItem(spacer)
        self.id_container_layout.addWidget(self.user)

        # Message
        self.message_container = QtWidgets.QWidget(self)
        self.message_container.hide()
        self.message_container_layout = QtWidgets.QHBoxLayout()
        self.message_container_layout.setContentsMargins(0, 0, 0, 0)
        self.message_container_layout.setSpacing(0)
        self.message_container.setLayout(self.message_container_layout)

        self.message_box = MessageBox(self)
        self.message_container_layout.addWidget(self.message_box)

        # Add (Logo & User ID) & Message
        self.main_layout.addWidget(self.id_container)
        self.main_layout.addWidget(self.message_container)

    def setMessage(self, message, level='info'):
        '''Set *message* with severity *level*.'''
        self.message_container.show()
        self.message_box.setMessage(message, level)

    def dismissMessage(self):
        '''Dismiss message.'''
        self.message_container.hide()
        self.message_box.dismissMessage()


class Logo(QtWidgets.QLabel):
    '''Logo widget.'''

    def __init__(self, parent=None):
        '''Instantiate logo widget.'''
        super(Logo, self).__init__(parent=parent)

        self.setObjectName('ftrack-logo-widget')
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            QtCore.Qt.AlignTop
        )
        self.setLayout(self.main_layout)

        logoPixmap = QtGui.QPixmap(':ftrack/image/default/ftrackLogoLabel')
        self.setPixmap(
            logoPixmap.scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )


class User(QtWidgets.QWidget):
    '''User name and logo widget.'''

    def __init__(self, username, parent=None):
        '''Instantiate user name and logo widget using *username*.'''

        super(User, self).__init__(parent=parent)
        self.setObjectName('ftrack-userid-widget')
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(
            QtCore.Qt.AlignRight
        )
        self.setLayout(self.main_layout)

        self.label = QtWidgets.QLabel(self)
        self.image = thumbnail.User(self)
        self.image.setFixedSize(35, 35)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.image)

        self.image.load(username)

        if username not in NAME_CACHE:
            NAME_CACHE[username] = ftrack.User(username).getName().title()

        self.label.setText(NAME_CACHE[username])


class MessageBox(QtWidgets.QWidget):
    '''Message widget.'''

    def __init__(self, parent=None):
        '''Instantiate message widget.'''

        super(MessageBox, self).__init__(parent=parent)
        self.setObjectName('ftrack-message-box')
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            QtCore.Qt.AlignTop
        )
        self.setLayout(self.main_layout)

        self.label = QtWidgets.QLabel(parent=self)
        self.label.resize(QtCore.QSize(900, 80))

        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.label.hide()
        self.label.setObjectName('ftrack-header-message-info')

        self.main_layout.addWidget(self.label)

    def setMessage(self, message, level):
        '''Set *message* and *level*.'''
        message_types = ['info', 'warning', 'error']
        if level not in message_types:
            raise ValueError(
                'Message type should be one of: %s' % ', '.join(message_types)
            )

        class_type = 'ftrack-header-message-%s' % level

        self.label.setObjectName(class_type)

        self.setStyleSheet(self.styleSheet())
        self.label.setText(message)
        self.label.setVisible(True)

    def dismissMessage(self):
        '''Dismiss the message.'''
        self.label.setText('')
        self.label.setVisible(False)
