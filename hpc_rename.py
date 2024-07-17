# HPC rename tool v01
# zach jantz
# 06/21/2024



from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



class HpcRenameTool(MayaQWidgetDockableMixin, QtWidgets.QWidget):


    def __init__(self, parent=None):
        super(HpcRenameTool, self).__init__(parent=parent)
        self.setWindowTitle("HPC Rename Tool")
        #self.resize(300,700)

        # UI
        main_vlayout1 = QtWidgets.QVBoxLayout()
        self.setLayout(main_vlayout1)

        # Options
        options_group = QtWidgets.QGroupBox()
        main_vlayout1.addWidget(options_group)
        options_vlayout1 = QtWidgets.QVBoxLayout()
        options_group.setLayout(options_vlayout1)
        options_group.setTitle("Options")

        options_hlayout1 = QtWidgets.QHBoxLayout()
        options_vlayout1.addLayout(options_hlayout1)
        options_hlayout2 = QtWidgets.QHBoxLayout()
        options_vlayout1.addLayout(options_hlayout2)

        options_label1 = QtWidgets.QLabel("Padding:")
        options_hlayout1.addWidget(options_label1)
        self.padding_input = QtWidgets.QSpinBox()
        self.padding_input.setRange(2,8)
        options_hlayout1.addWidget(self.padding_input)
        self.padding_input.setToolTip("Set the padding ammount for any automated numbering")

        options_label2 = QtWidgets.QLabel("Start Number:")
        options_hlayout1.addWidget(options_label2)
        self.start_num = QtWidgets.QSpinBox()
        options_hlayout1.addWidget(self.start_num)
        self.start_num.setToolTip("Starting number for automated naming")
        self.start_num.setValue(1)

        # Scope Options
        self.scope_group = QtWidgets.QButtonGroup(self)
        self.scope_group.setExclusive(True)

        selected_scope = QtWidgets.QRadioButton("Selected")
        heirarchy_scope = QtWidgets.QRadioButton("Heirarchy")
        all_scope = QtWidgets.QRadioButton("All")
        selected_scope.setChecked(True)
        selected_scope.setToolTip("Perform actions on selected nodes")
        heirarchy_scope.setToolTip("Perform actions on nodes in the selected node's heirarchy")
        all_scope.setToolTip("Perform actions on all nodes.")

        self.scope_group.addButton(selected_scope, id=1)
        self.scope_group.addButton(heirarchy_scope, id=2)
        self.scope_group.addButton(all_scope, id=3)
        
        options_hlayout2.addWidget(selected_scope)
        options_hlayout2.addWidget(heirarchy_scope)
        options_hlayout2.addWidget(all_scope)

        # rename 
        rename_group = QtWidgets.QGroupBox()
        main_vlayout1.addWidget(rename_group)
        rename_vlayout1 = QtWidgets.QVBoxLayout()
        rename_group.setLayout(rename_vlayout1)
        rename_group.setTitle("Rename")

        rename_hlayout1 = QtWidgets.QHBoxLayout()
        rename_vlayout1.addLayout(rename_hlayout1)

        rename_label1 = QtWidgets.QLabel("Structured Rename")
        rename_hlayout1.addWidget(rename_label1)
        self.struct_input = QtWidgets.QLineEdit()
        rename_hlayout1.addWidget(self.struct_input)
        rename_button1 = QtWidgets.QPushButton("Rename")
        rename_button1.clicked.connect(self.structured_rename)
        rename_hlayout1.addWidget(rename_button1)
        rename_button1.setToolTip("Rename selected nodes with naming structure\nNumbering placement signified with a #")


    	# pfix and sfix
        append_group = QtWidgets.QGroupBox()
        main_vlayout1.addWidget(append_group)
        append_group.setTitle("Append")

        append_vlayout1 = QtWidgets.QVBoxLayout()
        append_group.setLayout(append_vlayout1)

        append_hlayout1 = QtWidgets.QHBoxLayout()                 
        append_vlayout1.addLayout(append_hlayout1)

        self.append_input = QtWidgets.QLineEdit()
        append_hlayout1.addWidget(self.append_input)

        pfx_button = QtWidgets.QPushButton("Prefix")
        pfx_button.clicked.connect(lambda x:self.append_node_name('pfx', self.append_input.text()))
        pfx_button.setToolTip("Append text as prefix")
        sfx_button = QtWidgets.QPushButton("Suffix")
        sfx_button.clicked.connect(lambda x:self.append_node_name('sfx', self.append_input.text()))
        sfx_button.setToolTip("Append text as suffix")

        # sfx presets
        append_hlayout1.addWidget(pfx_button)
        append_hlayout1.addWidget(sfx_button)
        append_hlayout2 = QtWidgets.QHBoxLayout()
        append_vlayout1.addLayout(append_hlayout2)

        geo_button = QtWidgets.QPushButton("GEO")
        grp_button = QtWidgets.QPushButton("GRP")
        ctrl_button = QtWidgets.QPushButton("CTRL")
        jnt_button = QtWidgets.QPushButton("JNT")

        append_hlayout2.addWidget(geo_button)
        append_hlayout2.addWidget(grp_button)
        append_hlayout2.addWidget(ctrl_button)
        append_hlayout2.addWidget(jnt_button)

        geo_button.clicked.connect(lambda x:self.append_node_name('sfx', "GEO"))
        grp_button.clicked.connect(lambda x:self.append_node_name('sfx', "GRP"))
        ctrl_button.clicked.connect(lambda x:self.append_node_name('sfx', "CTRL"))
        jnt_button.clicked.connect(lambda x:self.append_node_name('sfx', "JNT"))

        # search and replace
        sr_group = QtWidgets.QGroupBox()
        main_vlayout1.addWidget(sr_group)
        sr_vlayout1 = QtWidgets.QVBoxLayout()
        sr_group.setLayout(sr_vlayout1)
        sr_group.setTitle("Search and Replace")

        sr_hlayout1 = QtWidgets.QHBoxLayout()
        sr_vlayout1.addLayout(sr_hlayout1)        
        sr_hlayout2 = QtWidgets.QHBoxLayout()
        sr_vlayout1.addLayout(sr_hlayout2)


        self.search_input = QtWidgets.QLineEdit()
        sr_hlayout1.addWidget(self.search_input)
        self.replace_input = QtWidgets.QLineEdit()
        sr_hlayout2.addWidget(self.replace_input)

        search_button = QtWidgets.QPushButton("Search")
        sr_hlayout1.addWidget(search_button)
        search_button.clicked.connect(self.search)
        search_button.setToolTip("Select nodes containing specified string")
        replace_button = QtWidgets.QPushButton("Replace")
        sr_hlayout2.addWidget(replace_button)
        replace_button.clicked.connect(self.replace)
        replace_button.setToolTip("Replace specified string in nodes containing it with replacement string")

        propagate_button = QtWidgets.QPushButton("Propagate Group Name")
        main_vlayout1.addWidget(propagate_button)
        propagate_button.clicked.connect(self.parent_name_to_child)
        propagate_button.setToolTip("Rename the objects in a selected group based on the group name.")


    def check_for_suffix(self, items, suffix):
        missing_suffix = []
        nodes = self.get_nodes(self.scope_group.checkedId())
        if nodes != None:
            for node in nodes:
                if isinstance(node, str) is True:
                    if not node.endswith(suffix):
                        missing_suffix.append(node)

            return missing_suffix


    def is_group(self, node):
        """
        Returns True if a node is a group node
        """
        if not cmds.listRelatives(node, shapes=1):
            return True
        else:
            return False


    def rename_node(self, node_name, new_name):

        try:

            cmds.rename(node_name, new_name)
            return new_name

        except RuntimeError:

            return None


    def pad_num(self, num, padding_amount):
        """
        Converts an integer to a string with the given amount of 0 padding
        """
        num_str = str(num)
        padding = '0' * (padding_amount - len(num_str))
        padded_num = padding + num_str

        return padded_num


    def parent_name_to_child(self):
        """
        Name the objects in a selected group based on based on the group name.
        Assumes that the group has the '_GRP' suffix
        """
        parent_node = cmds.ls(sl=1, fl=1)[0]
        # Remove suffix
        p_name = parent_node.replace("_GRP", '')

        if self.is_group(parent_node):
            children = [node for node in cmds.listRelatives(parent_node) if not self.is_group(node)]
            for i in range(len(children)):
                child = children[i]
                c_name = p_name + "_" + self.pad_num(i + 1, self.padding_input.value()) + "_GEO"
                self.rename_node(child, c_name)


    def structured_rename(self):
        """
        Structured rename renames nodes based on a referenced # for padding input
        Structured rename works on selected only
        """

        nodes = self.get_nodes(1)
        count = self.start_num.value()
        name_struct = self.struct_input.text()

        if name_struct != '' and nodes != None:
            for node in nodes:

                new_name = name_struct.replace("#", self.pad_num(count, self.padding_input.value()))
                self.rename_node(node, new_name)

                count += 1


    def append_node_name(self, position, append_val):

        nodes = self.get_nodes(self.scope_group.checkedId())
        if append_val != '' and nodes != None:
            for node in nodes:

                if position == 'pfx':
                    name = append_val + "_" + node
                    self.rename_node(node, name)

                elif position == 'sfx':
                    name = node + "_" + append_val
                    self.rename_node(node, name)


    def walk_heirarchy(self, start):

        children = cmds.listRelatives(start, ad=1, type='transform')

        return children


    def get_nodes(self, mode):
        """
        Returns a list of nodes to opperate on depending on the scope option
        """
        # Scope is selected
        if mode == 1:

            return cmds.ls(sl=1)

        # Scope is heirarchy
        elif mode == 2:

            start_node = cmds.ls(sl=1)

            if len(start_node)==1 and self.is_group(start_node[0]):

                return self.walk_heirarchy(start_node[0])

        # Scope is all
        elif mode ==3:

            return cmds.ls(dag=1)

        else:
            return None


    def search(self):

        sval = self.search_input.text()
        found = []
        if sval != '':

            nodes = self.get_nodes(self.scope_group.checkedId())
            cmds.select(cl=1)
            if nodes != None:
                for node in nodes:
                    if sval in node:
                        cmds.select(node, add=True)
                        found.append(node)
                return found, sval


    def replace(self):

        rval = self.replace_input.text()
        found, sval = self.search()
        if rval != '' and found != None:
            for node in found:
                node_name = node.replace(sval, rval)
                cmds.rename(node, node_name)


# From maya devkit example for dockable window
def toolUIScript(restore=False):
  
  ''' When the control is restoring, the workspace control has already been created and
      all that needs to be done is restoring its UI.
  '''
  if restore == True:
	  # Grab the created workspace control with the following.
      restoredControl = omui.MQtUtil.getCurrentParent()

  customMixinWindow = HpcRenameTool()  
  if customMixinWindow is None:
	  # Create a custom mixin widget for the first time
      customMixinWindow.setObjectName('renameToolCustomWindow')
      
  if restore == True:
	  # Add custom mixin widget to the workspace control
      mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
      omui.MQtUtil.addWidgetToMayaLayout(mixinPtr, restoredControl)
  else:
	  # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
      customMixinWindow.show(dockable=True, uiScript='toolUIScript(restore=True)')
      
  return customMixinWindow


def main():
    ui = toolUIScript()
    return ui


if __name__ == '__main__':
    main()










