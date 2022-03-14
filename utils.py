DEFAULT_PLAYER_SET = {
    10: 1,
    9: 1,
    8: 2,
    7: 3,
    6: 4,
    5: 4,
    4: 4,
    3: 5,
    2: 8,
    1: 1,
    50: 6,
    0: 1
}


def get_rank_translation(rank: str):

    pawn_rank_translation = {
            "1": 10,
            "2": 9,
            "3": 8,
            "4": 7,
            "5": 6,
            "6": 5,
            "7": 4,
            "8": 3,
            "9": 2,
            "S": 1,
            "B": 50,
            "F": 0
    }

    translated_rank = pawn_rank_translation[rank]

    return translated_rank


color = {
    "green": "#86b300",
    "font_1": "#f1f1f1",
    "background_1": "#3b3d41",
    "background_2": "#646568",
    "cell_highlight": "#595959",
    "widget_border": "#717273",
    "table_headers_border": "#646568"
    }

main_style = f"""

    QWidget{{
        background: {color["background_1"]};
        font-size: 20px;
        }}
        
    QFrame{{
        background: {color["background_2"]};
        border-radius: 3px;
        }}
    
    QLabel{{
        color: {color["font_1"]};
        }}
        
    QLineEdit{{
        color: {color["font_1"]};
        border: 2px solid {color["widget_border"]};
        border-radius: 3px;
        padding: 1px 0px 1px 3px;
        }}
        
    QPushButton{{
        background-color: {color["background_1"]};
        color: {color["font_1"]};
        border: 2px solid {color["widget_border"]};
        border-radius: 3px;
        padding: 2px;
        }}
    
    QPushButton:hover{{
        background: #2F3032;
        color: {color["background_2"]};
        }}
        
    QTableWidget{{
        color: {color["font_1"]};
        font: 26px;
        background: {color["background_2"]};
        border: none;
        }}
    """

detailed_style = {

    "table_style": {
        "main": f"""
            QAbstractButton::section{{
                background-color: {color["background_2"]};
                font: {color["font_1"]};
            }}
            QHeaderView::section{{
                background-color: {color["background_2"]};
                border: 1px solid {color["table_headers_border"]};
                font: {color["font_1"]};
            }}
        """,

        "headers": f"::section{{color: {color['font_1']};}}"
    },

    "label_after_submitting": f"""border-width: 2px;
                              border-style: solid none;
                              border-color: {color['green']};
                              border-radius: 0px;
                              padding: 5px;
    """,

    "pawn_img_border": f"""border-radius: 3px;
                       border: 2px solid {color['green']};
    """,

    "cell_highlighting": f"background-color: {color['cell_highlight']}"
}
