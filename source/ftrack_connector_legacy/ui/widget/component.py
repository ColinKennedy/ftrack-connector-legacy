# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import os
import uuid

from QtExt import QtWidgets, QtCore, QtGui

import ftrack_connector_legacy.ui.widget.line_edit
import ftrack_connector_legacy.ui.widget.label


class Component(QtWidgets.QWidget):
    '''Represent a component.'''

    nameChanged = QtCore.Signal()

    def __init__(self, componentName=None, resourceIdentifier=None,
                 parent=None):
        '''Initialise widget with initial component *value* and *parent*.'''
        super(Component, self).__init__(parent=parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.componentNameEdit = ftrack_connector_legacy.ui.widget.line_edit.LineEdit()
        self.componentNameEdit.setPlaceholderText('Enter component name')
        self.componentNameEdit.textChanged.connect(self.nameChanged)

        self.layout().addWidget(self.componentNameEdit)

        # TODO: Add theme support.
        removeIcon = QtGui.QIcon(
            QtGui.QPixmap(':/ftrack/image/light/trash')
        )

        self.removeAction = QtWidgets.QAction(
            QtGui.QIcon(removeIcon), 'Remove', self.componentNameEdit
        )
        self.removeAction.setStatusTip('Remove component.')
        self.componentNameEdit.addAction(
            self.removeAction
        )

        self.resourceInformation = ftrack_connector_legacy.ui.widget.label.Label()
        self.layout().addWidget(self.resourceInformation)

        # Set initial values.
        self.setId(str(uuid.uuid4()))
        self.setComponentName(componentName)
        self.setResourceIdentifier(resourceIdentifier)

    def value(self):
        '''Return dictionary with component data.'''
        return {
            'id': self.id(),
            'componentName': self.componentName(),
            'resourceIdentifier': self.resourceIdentifier()
        }

    def computeComponentName(self, resourceIdentifier):
        '''Return a relevant component name using *resourceIdentifier*.'''
        name = os.path.basename(resourceIdentifier)
        if not name:
            name = resourceIdentifier
        else:
            name = name.split('.')[0]

        return name

    def id(self):
        '''Return current id.'''
        return self._id

    def setId(self, componentId):
        '''Set id to *componentId*.'''
        self._id = componentId

    def componentName(self):
        '''Return current component name.'''
        return self.componentNameEdit.text()

    def setComponentName(self, componentName):
        '''Set *componentName*.'''
        self.componentNameEdit.setText(componentName)

    def resourceIdentifier(self):
        '''Return current resource identifier.'''
        return self.resourceInformation.text()

    def setResourceIdentifier(self, resourceIdentifier):
        '''Set *resourceIdentifier*.'''
        self.resourceInformation.setText(resourceIdentifier)

        if not self.componentName():
            self.setComponentName(
                self.computeComponentName(resourceIdentifier)
            )
