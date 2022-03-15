from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread

from copy import deepcopy

from utils import DEFAULT_PLAYER_SET, detailed_style
from worker import Worker


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.last_player_sets_tuple = None

        self.setGeometry(200, 200, 500, 250)
        self.setWindowTitle("Stratego pawn counter")
        self.initUI()


    def initUI(self) -> None:
        """
        INIT window's main layout.
        """

        # set upper frame with player hash
        self.upper_frame = QtWidgets.QFrame(self)
        self.init_upper_frame_ui()

        # set middle frame with players' names
        self.middle_frame = QtWidgets.QFrame(self)
        self.init_middle_frame_ui()

        # set lower frame which contains table
        self.lower_frame = QtWidgets.QFrame(self)
        self.init_table_ui()
        self.lower_frame.hide()

        # layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.upper_frame)
        self.main_layout.addWidget(self.middle_frame)
        self.main_layout.addWidget(self.lower_frame)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)


    def init_upper_frame_ui(self) -> None:
        """
        INIT graphical view of the frame collecting player_hash.
        """

        # label
        self.label = QtWidgets.QLabel()
        self.label.setText("Enter your player hash: ")

        # input field
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setMaxLength(6)
        self.input_field.setFrame(False)

        # submit button
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setText("  Submit  ")
        self.submit_button.clicked.connect(self.submit)

        # layout
        self.hash_player_layout = QtWidgets.QGridLayout(self.upper_frame)
        self.hash_player_layout.addWidget(self.label, 0, 0)
        self.hash_player_layout.addWidget(self.input_field, 0, 1)
        self.hash_player_layout.addWidget(self.submit_button, 0, 2)


    def init_middle_frame_ui(self) -> None:
        """
        INIT graphical view of the frame collecting data about players.
        """

        # label and input field for the user's name
        self.label_pl_user_name = QtWidgets.QLabel()
        self.label_pl_user_name.setText("Your name: ")
        self.input_pl_user_name = QtWidgets.QLineEdit()
        self.input_pl_user_name.setFrame(False)

        # label and input field for the user's opponent name
        self.label_pl_opponent_name = QtWidgets.QLabel()
        self.label_pl_opponent_name.setText("Your opponent's name: ")
        self.input_pl_opponent_name = QtWidgets.QLineEdit()
        self.input_pl_opponent_name.setFrame(False)

        # layout
        self.players_layout = QtWidgets.QGridLayout(self.middle_frame)
        self.players_layout.addWidget(self.label_pl_user_name, 0, 0)
        self.players_layout.addWidget(self.input_pl_user_name, 0, 1)
        self.players_layout.addWidget(self.label_pl_opponent_name, 1, 0)
        self.players_layout.addWidget(self.input_pl_opponent_name, 1, 1)


    def init_table_ui(self) -> None:
        """
        INIT graphical view of the table displaying players' pawn number.
        """

        # frame layout
        self.table_layout = QtWidgets.QGridLayout(self.lower_frame)
        self.table = QtWidgets.QTableWidget()
        self.table_layout.addWidget(self.table, 0, 0)

        # table - shape and columns and rows names
        self.table.setColumnCount(2)
        self.table.setRowCount(11)
        rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, "S", "B"]
        rows = [str(x) for x in rows]
        self.table.setVerticalHeaderLabels(rows)
        self.table.setStyleSheet(detailed_style["table_style"]["main"])

        # width and height - view style
        h_header = self.table.horizontalHeader()
        h_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        h_header.setDefaultAlignment(Qt.AlignCenter)
        h_header.setStyleSheet(detailed_style["table_style"]["headers"])
        v_header = self.table.verticalHeader()
        v_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        v_header.setDefaultAlignment(Qt.AlignCenter)
        v_header.setStyleSheet(detailed_style["table_style"]["headers"])

        # table settings - editing and selecting cells
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QTableView.NoSelection)
        h_header.setSectionsClickable(False)
        v_header.setSectionsClickable(False)
        self.table.setCornerButtonEnabled(False)

        # set default cells' values
        i = 0
        for current_value in DEFAULT_PLAYER_SET.values():
            cell_item_0 = self.create_cell_widget(current_value, current_value)
            self.table.setCellWidget(i, 0, cell_item_0)
            cell_item_1 = self.create_cell_widget(current_value, current_value)
            self.table.setCellWidget(i, 1, cell_item_1)
            i += 1

        pl_user = DEFAULT_PLAYER_SET.copy()
        pl_opponent = DEFAULT_PLAYER_SET.copy()
        self.last_player_sets_tuple = (pl_user, pl_opponent)


    def submit(self) -> None:
        """
        Changes graphical view of the table and run long running task.
        """
        player_hash = self.input_field.text()
        user_name = self.input_pl_user_name.text()
        opponent_name = self.input_pl_opponent_name.text()


        # main window graphical settings
        self.input_field.hide()
        self.submit_button.hide()
        self.middle_frame.hide()
        self.lower_frame.show()
        self.setGeometry(200, 200, 520, 600)

        # table settings
        self.table.setHorizontalHeaderLabels([user_name, opponent_name])
        self.label.setText(f"player: {player_hash}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(detailed_style["label_after_submitting"])

        self.long_running_task(player_hash)


    def long_running_task(self, player_hash: str) -> None:
        """
        Creates a separate thread and using it connects Worker with App. Runs the thread.

        Parameter:
            player_hash - variable that connects App with Worker
        """

        # create a QThread object
        self.thread = QThread()
        # create a worker object
        self.worker = Worker(player_hash)
        # move worker to the thread
        self.worker.moveToThread(self.thread)
        # connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_player_pawn_status)
        # start the thread
        self.thread.start()


    def update_player_pawn_status(self, player_sets_tuple: tuple) -> None:
        """
        Updates self.table view. Not every cell is changed every time, only the ones
        which values have changed since last time. The function also highlights cells if
        value equals 0 and all cells of a column if player has lost.

        Parameter:
            player_sets_tuple - tuple with dictionaries containing current players' pawn number
        """

        player_index = 0
        for player_current, player_last in zip(player_sets_tuple, self.last_player_sets_tuple):
            # loop over players
            row_index = 0
            for current_item, last_item, default_item in \
                    zip(player_current.values(), player_last.values(), DEFAULT_PLAYER_SET.values()):
                # loop over items in dictionaries, army units (type, number)
                if current_item != last_item:
                    # change in number condition
                    cell_widget = self.create_cell_widget(current_item, default_item)
                    if current_item == 0:
                        # highlighting
                        cell_widget.setStyleSheet(detailed_style["cell_highlighting"])
                    self.table.setCellWidget(row_index, player_index, cell_widget)
                    self.last_player_sets_tuple = deepcopy(player_sets_tuple)
                row_index += 1
            player_index += 1

        self.update_highlighting(player_sets_tuple)


    def update_highlighting(self, player_sets_tuple: tuple):
        """
        Changes background of cells in a column of a player how have lost (dict item: (100,0)).

        Parameter:
            player_sets_tuple - tuple with dictionaries containing current players' pawn number
        """

        ROW_NUM = self.table.rowCount()
        i = 0
        for player_current_set in player_sets_tuple:
            # loop over players
            if player_current_set[0] == 0:
                for row in range(ROW_NUM):
                    # loop over rows
                    current_widget = self.table.cellWidget(row, i)
                    current_widget.setStyleSheet(detailed_style["cell_highlighting"])
            i += 1


    def create_cell_widget(self, alive: int, default: int) -> QtWidgets.QFrame:
        """
        Creates a QFrame widget which is going to be put into table cells.

        Parameters:
            alive, default - number shows how many images of specific color should be put into frame.
            Firstly there are number of images represented by alive, then (default - alive) images
            in different color and after that (8 - default) empty images.

        Returns:
            QFrame with graphical representation of player pawns number.
        """

        pawn_img_path = "img_pawn.svg"
        empty_img_path = "img_empty.png"
        IMG_NUM = max(DEFAULT_PLAYER_SET.values())
        OPACITY = 0.4

        frame = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(frame)

        for i in range(IMG_NUM):
            label = QtWidgets.QLabel()
            if i < default:
                # create img for default number of pawns
                pixmap = QtGui.QPixmap(pawn_img_path)
                label.setStyleSheet(detailed_style["pawn_img_border"])
                if i >= alive:
                    # set opacity on img of dead pawns
                    opacity_effect = QtWidgets.QGraphicsOpacityEffect()
                    opacity_effect.setOpacity(OPACITY)
                    label.setGraphicsEffect(opacity_effect)
            else:
                pixmap = QtGui.QPixmap(empty_img_path)
            label.setPixmap(pixmap)
            layout.addWidget(label, i)

        return frame
