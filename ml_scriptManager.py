import maya.cmds as cmds
import maya.mel as mel


class ml_scriptManager:

    """Main window class for ml_scriptManager"""

    def __init__(self):

        # Main initialisation method

        print 'Initialising ml_scriptManager'

    def create_window(self):

        # Creates the window

        self.window_name = 'Script Manager'
        self.sm_version = '2.0.0'
        self.maya_version = 2013

        self.maya_version = mel.eval('getApplicationVersionAsFloat()')

        script_position = []
        path_position = []
        pyscript_position = []
        pypath_position = []

        self.spacer = 3
        self.margin = 1
        self.width = 250

        if cmds.window('ml_scriptManagerUI', exists=True):
            cmds.deleteUI('ml_scriptManagerUI', wnd=True)
        if cmds.windowPref('ml_scriptManagerUI', exists=True):
            cmds.windowPref('ml_scriptManagerUI', r=True)

        if cmds.dockControl('ml_dockControl', exists=True):
            cmds.deleteUI('ml_dockControl', control=True)

        user_script_directory = cmds.internalVar(usd=True)

        # CREATE THE WINDOW

        cmds.window('ml_scriptManagerUI', s=1, menuBar=True,
                    title=self.window_name + ' v.' + self.sm_version,
                    widthHeight=(self.width, 65))
        self.create_menu()

        cmds.tabLayout('ml_tabs', innerMarginWidth=5,
                       innerMarginHeight=5)
        self.create_mel_tab()
        self.create_py_tab()

        cmds.tabLayout('ml_tabs',
            edit=True,
            tabLabel=[('mel_form_layout', 'Mel'),('py_form_layout', 'Python')])

        # SHOW THE WINDOW AND EDIT SIZE
        cmds.showWindow('ml_scriptManagerUI')
        # cmds.dockControl('ml_dockControl',
        #     w=self.width,
        #     allowedArea='all',
        #     area='right',
        #     l='Script Manager',
        #     content='ml_scriptManagerUI')
        
        cmds.window('ml_scriptManagerUI', e=True, wh=(self.width, 500))

        if cmds.optionVar(exists='ml_defaultTab'):
            tab = cmds.optionVar(q='ml_defaultTab')
            cmds.tabLayout('ml_tabs', e=True, st=tab)

    def create_menu(self):

        # Creates the menubar for the main ui

        cmds.menu(label='File', tearOff=False)
        cmds.menuItem(divider=True)
        cmds.menuItem(label='Reload Script', ann='Resources all scripts'
                      )
        cmds.menuItem(label='Quit' + self.window_name + ' '
                      + self.sm_version, ann='Quits Script Manager')
        cmds.menu(label='Settings', tearOff=False)
        cmds.menuItem(label='Add Mel Category',
                      ann='Adds a mel category to your config file')
        cmds.menuItem(label='Add Python Category',
                      ann='Adds a python category to your config file')
        cmds.menuItem(label='Delete Mel Category',
                      ann='Deletes selected category from your config file'
                      )
        cmds.menuItem(label='Delete Python Category',
                      ann='Deletes selected python category from your config file'
                      )
        cmds.menuItem(label='Set Default Tab',
                      ann='Set the current tab as default',
                      c=self.set_default_tab)
        cmds.menuItem(label='Set Editor Path',
                      ann='Set the path to your favorite script editor')
        cmds.menuItem(divider=True)
        cmds.menu(label='Help', tearOff=False)
        cmds.menuItem(label='About ' + self.window_name + ' '
                      + self.sm_version,
                      ann='Set the path to your favorite script editor')

    def create_mel_tab(self):

        # Main tab for the mel scripts

        cmds.formLayout('mel_form_layout', p='ml_tabs', nd=100)

        cmds.frameLayout(
            'mel_list_frame',
            p='mel_form_layout',
            label='Script List',
            mw=self.spacer,
            mh=self.spacer,
            borderStyle='etchedIn',
            )

        cmds.formLayout('mel_list_form', p='mel_list_frame', nd=100)

        cmds.formLayout('mel_button_form', p='mel_list_form', nd=100)

        cmds.iconTextButton(
            'source_mel_script',
            p='mel_button_form',
            bgc=(0.5, 0.8, 0.5),
            w=self.width / 3 - self.spacer - 5,
            ann='Sources the selected script',
            style='iconAndTextHorizontal',
            label='Source ',
            image1='sourceScript.png',
            )
        cmds.iconTextButton(
            'run_mel_script',
            p='mel_button_form',
            bgc=(0.8, 0.5, 0.5),
            w=self.width / 3 - self.spacer - 5,
            ann='Runs the selected script',
            style='iconAndTextHorizontal',
            label='Run ',
            image1='execute.png',
            )
        cmds.iconTextButton(
            'edit_mel_script',
            p='mel_button_form',
            bgc=(0.5, 0.5, 0.8),
            w=self.width / 3 - self.spacer - 5,
            ann='Edits the selected script',
            style='iconAndTextHorizontal',
            label='Edit ',
            image1='echoCommandsOff.png',
            )
        cmds.optionMenu('mel_category_switch', p='mel_list_form',
                        bgc=(0.2, 0.2, 0.2))

        cmds.formLayout('mel_button_form', edit=True, af=[
            ('source_mel_script', 'left', self.margin),
            ('source_mel_script', 'top', self.margin),
            ('source_mel_script', 'bottom', self.margin),
            ('run_mel_script', 'top', self.margin),
            ('run_mel_script', 'bottom', self.margin),
            ('edit_mel_script', 'top', self.margin),
            ('edit_mel_script', 'right', self.margin),
            ('edit_mel_script', 'bottom', self.margin),
            ], ac=[('run_mel_script', 'left', self.spacer,
                   'source_mel_script'), ('edit_mel_script', 'left',
                   self.spacer, 'run_mel_script')],
                an=[('source_mel_script', 'right'), ('run_mel_script',
                    'right')])

        cmds.textScrollList('mel_list', p='mel_list_form', ams=False)

        cmds.frameLayout(
            'mel_description_frame',
            p='mel_list_form',
            collapsable=True,
            borderStyle='etchedIn',
            label='Description',
            mw=self.spacer,
            mh=self.spacer,
            )

        cmds.columnLayout('mel_description_cl',
                          p='mel_description_frame', adj=True)

        cmds.scrollField(
            'mel_description_field',
            p='mel_description_cl',
            w=10,
            h=100,
            wordWrap=True,
            editable=True,
            bgc=(1.0, 1.0, 1.0),
            text='Add a description or instructions',
            )

        cmds.button('mel_description_button', p='mel_description_cl',
                    label='Save Description',
                    ann='Add descriptions to your scripts')

        cmds.formLayout('mel_list_form', edit=True, af=[
            ('mel_button_form', 'left', self.spacer),
            ('mel_button_form', 'right', self.spacer),
            ('mel_button_form', 'top', self.spacer),
            ('mel_category_switch', 'left', self.spacer),
            ('mel_category_switch', 'right', self.spacer),
            ('mel_list', 'left', self.spacer),
            ('mel_list', 'right', self.spacer),
            ('mel_description_frame', 'left', self.spacer),
            ('mel_description_frame', 'right', self.spacer),
            ('mel_description_frame', 'bottom', self.spacer),
            ], an=[('mel_category_switch', 'bottom'), ('mel_button_form'
                   , 'bottom'), ('mel_description_frame', 'top')],
                ac=[('mel_category_switch', 'top', self.spacer,
                    'mel_button_form'), ('mel_list', 'top',
                    self.spacer, 'mel_category_switch'), ('mel_list',
                    'bottom', self.spacer, 'mel_description_frame')])

        cmds.formLayout('mel_form_layout', edit=True,
                        af=[('mel_list_frame', 'left', self.spacer),
                        ('mel_list_frame', 'right', self.spacer),
                        ('mel_list_frame', 'bottom', self.spacer),
                        ('mel_list_frame', 'top', self.spacer)])

    def create_py_tab(self):

        # Main tab for the python scripts

        cmds.formLayout('py_form_layout', p='ml_tabs', nd=100)

        cmds.frameLayout(
            'py_list_frame',
            p='py_form_layout',
            label='Script List',
            mw=self.spacer,
            mh=self.spacer,
            borderStyle='etchedIn',
            )

        cmds.formLayout('py_list_form', p='py_list_frame', nd=100)

        cmds.formLayout('py_button_form', p='py_list_form', nd=100)

        cmds.iconTextButton(
            'source_py_script',
            p='py_button_form',
            bgc=(0.5, 0.8, 0.5),
            w=self.width / 2 - self.spacer - 5,
            ann='Sources the selected script',
            style='iconAndTextHorizontal',
            label='Execute ',
            image1='sourceScript.png',
            )

        cmds.iconTextButton(
            'edit_py_script',
            p='py_button_form',
            bgc=(0.5, 0.5, 0.8),
            w=self.width / 2 - self.spacer - 5,
            ann='Edits the selected script',
            style='iconAndTextHorizontal',
            label='Edit ',
            image1='echoCommandsOff.png',
            )
        cmds.optionMenu('py_category_switch', p='py_list_form',
                        bgc=(0.2, 0.2, 0.2))

        cmds.formLayout('py_button_form', edit=True, af=[
            ('source_py_script', 'left', self.margin),
            ('source_py_script', 'top', self.margin),
            ('source_py_script', 'bottom', self.margin),
            ('edit_py_script', 'top', self.margin),
            ('edit_py_script', 'right', self.margin),
            ('edit_py_script', 'bottom', self.margin),
            ], ac=[('edit_py_script', 'left',self.spacer, 'source_py_script')],
                an=[('source_py_script', 'right')])

        cmds.textScrollList('py_list', p='py_list_form', ams=False)

        cmds.frameLayout(
            'py_description_frame',
            p='py_list_form',
            collapsable=True,
            borderStyle='etchedIn',
            label='Description',
            mw=self.spacer,
            mh=self.spacer,
            )

        cmds.columnLayout('py_description_cl',
                          p='py_description_frame', adj=True)

        cmds.scrollField(
            'mel_description_field',
            p='py_description_cl',
            w=10,
            h=100,
            wordWrap=True,
            editable=True,
            bgc=(1.0, 1.0, 1.0),
            text='Add a description or instructions',
            )

        cmds.button('py_description_button', p='py_description_cl',
                    label='Save Description',
                    ann='Add descriptions to your scripts')

        cmds.formLayout('py_list_form', edit=True, af=[
            ('py_button_form', 'left', self.spacer),
            ('py_button_form', 'right', self.spacer),
            ('py_button_form', 'top', self.spacer),
            ('py_category_switch', 'left', self.spacer),
            ('py_category_switch', 'right', self.spacer),
            ('py_list', 'left', self.spacer),
            ('py_list', 'right', self.spacer),
            ('py_description_frame', 'left', self.spacer),
            ('py_description_frame', 'right', self.spacer),
            ('py_description_frame', 'bottom', self.spacer),
            ], an=[('py_category_switch', 'bottom'), ('py_button_form'
                   , 'bottom'), ('py_description_frame', 'top')],
                ac=[('py_category_switch', 'top', self.spacer,
                    'py_button_form'), ('py_list', 'top',
                    self.spacer, 'py_category_switch'), ('py_list',
                    'bottom', self.spacer, 'py_description_frame')])

        cmds.formLayout('py_form_layout', edit=True,
                        af=[('py_list_frame', 'left', self.spacer),
                        ('py_list_frame', 'right', self.spacer),
                        ('py_list_frame', 'bottom', self.spacer),
                        ('py_list_frame', 'top', self.spacer)])

    def set_default_tab(self, *args):
        if cmds.optionVar(exists='ml_defaultTab'):
            tab = cmds.tabLayout('ml_tabs', q=True, st=True)
            cmds.optionVar(sv=('ml_defaultTab',tab))
        else:
            tab = cmds.tabLayout('ml_tabs', q=True, st=True)
            cmds.optionVar(sv=('ml_defaultTab',tab))


test = ml_scriptManager()
test.create_window()
