from textwrap3 import wrap

from utils.formatting import make_line, bold

import matplotlib.pyplot as plt
import numpy as np # Math
import ast         # Literal evaluation

# For the ease of use, please DO NOT change these.
# Dynamic rendering has not been implemented, so it's easier to leave it
# the way it is now. Maybe sometimes in the future it gets coded.

SCREEN_WIDTH = 120 # Must be greater than 10, for other rendering reasons

# Must not be negative
PADDING_TOP    = 1 
PADDING_BOTTOM = 1
PADDING_LEFT   = 4
PADDING_RIGHT  = 4

HORIZONTAL_LENGTH = SCREEN_WIDTH + PADDING_LEFT + PADDING_RIGHT

class Article:
    def __init__(self, 
                 id:           int = 0, 
                 author_id:    int = 0,
                 title:        str = "", 
                 tags:         list = [],
                 content:      str = "",
                 likes:        int = 0,
                 dislikes:     int = 0,
                 views:        int = 0,
                 reading_time: int = 0,
                 formatted:    bool = False):
        """
        Returns an instance of Article class.
        """
        
        # Setting the relevant data
        self.id           = id
        self.author_id    = author_id
        self.title        = title
        self.tags         = tags
        self.content      = content
        self.likes        = likes
        self.dislikes     = dislikes
        self.views        = views
        self.reading_time = reading_time
        self.formatted    = formatted
        
        # If reading time is not calculated - calculate it
        if self.reading_time == 0:
            words = self.content.split(" ")
            cnt = 0
            for word in words:
                if len(word) > 1:
                    cnt += 1
            
            self.reading_time = cnt / 300 # 300 wpm
        
        
        # Literal-evaluate some useful properties in case they are strings
        if isinstance(self.tags, str):
            self.tags = ast.literal_eval(self.tags)  
        
        if isinstance(self.likes, str):
            self.likes    = ast.literal_eval(likes)
        
        if isinstance(self.dislikes, str):
            self.dislikes = ast.literal_eval(dislikes)
        
        if isinstance(self.views, str):
            self.views    = ast.literal_eval(views)
        
        # Check if article is properly formatted
        self.well_formatted = self.check_formatting()
        
        self.radio_selection      = 0 # Starting index of radio selection
        self.radio_selection_size = 4 # Like, dislike, recommend, save
        
        self.button_names = ["Like", "Dislike", "Recommend", "Save"]
        
        
    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            Unique representation of an article (its id).                                               
        """
        
        return str(self.id)


    def __str__(self) -> str:
        """
        Returns
        -------
        str
            Short representation of an article that can be used for printing.

        """
        
        return f"[{self.id}]: {self.title}\n{self.content}"
    
    
    def to_metadata_row(self) -> str:
        """
        Returns
        -------
        str
            Complete description of an article, ready to be stored inside a
            metadata .csv file.

        """
        
        return (f"{self.id},"
                f"{self.author_id},"
                f"{self.title},"
                f'"{self.tags}",'
                f'"{self.likes}",'
                f'"{self.dislikes}",'
                f'"{self.views}",'
                f"{self.reading_time:.2f},"
                f"{self.formatted}\n")
    
    
    def check_formatting(self) -> bool:
        """
        Checks whether the formatting of the article can be presented the way
        author created it.
        It can be presented in such way if and only if every line ought to be 
        shown is shorter than `SCREEN_WIDTH`, otherwise it would overlow.
        
        If yes, the article remains the way it is.
        If no,  the article will get auto-formatted to fit the screen.

        Returns
        -------
        bool
            Whether the article's formatting can be presented, 
            as described above.
        """
        
        lines = self.content.split("\n")
            
        return all(len(line) <= SCREEN_WIDTH for line in lines)
        

    def show(self):
        """
        Renders the article in the console - both the body and the buttons.
        """
        
        self.show_article()
        self.show_buttons()
        
        
    def show_article(self):
        """
        Renders the article's body / the main part inside the console.
        """
        
        text = None
        
        if self.formatted and self.well_formatted:
            text = self.content.split("\n")
            
        else:
            text = wrap(self.content, 
                        width=SCREEN_WIDTH)
            
        
        horizontal_border_line = make_line("═", HORIZONTAL_LENGTH)
        empty_row = (" " * HORIZONTAL_LENGTH)
        
        border_line_top     = f"╔{horizontal_border_line}╗"
        border_line_bottom  = f"╚{horizontal_border_line}╝"
        
        # Draw top border (title)
        left_padding_title  = " " * PADDING_LEFT
        right_padding_title = " " * (HORIZONTAL_LENGTH - PADDING_RIGHT - len(self.title))
        
        print(border_line_top)
        print(f"║{left_padding_title}{self.title}{right_padding_title}║")
        
        
        # Draw top border (body)
        print(f"╠{horizontal_border_line}╣")
        
        # Draw top padding
        for _ in range(PADDING_TOP):
            print(f"║{empty_row}║")
        
        
        # Draw central part (text)
        for line in text:
            # Left border
            print("║", end=(" " * PADDING_LEFT))
            
            # Printing text line
            leftover_padding = " " * (HORIZONTAL_LENGTH - PADDING_RIGHT - len(line))
            print(line, end=leftover_padding)
            
            
            # Right border
            print("║")
        
        
        # Draw bottom padding
        for _ in range(PADDING_TOP):
            print(f"║{empty_row}║")
        
        # Draw bottom border
        print(border_line_bottom)
        
        
    def show_buttons(self):
        """
        Renders following:
            (1) Like button
            (2) Dislike button
            (3) Save button
            (4) Comments button
            (5) Recommend similar button (or just press DOWN)
        
        The idea is to create something like TikTok and similar "short content"
        media - if you like what you are reading, you are going to like 
        something similar to it, most likely.
        """
        
        LIKE_BUTTON      = (f"╔═══════════╗\n"
                            f"║ LIKE ({self.likes:2}) ║\n"
                            f"╚═══════════╝")
        
        
        DISLIKE_BUTTON   = (f"╔══════════════╗\n"
                            f"║ DISLIKE ({self.dislikes:2}) ║\n"
                            f"╚══════════════╝")
        
        RECOMMEND_BUTTON = ("╔═══════════╗\n"
                            "║ RECOMMEND ║\n"
                            "╚═══════════╝")
        
        SAVE_BUTTON      = ("╔══════╗\n"
                            "║ SAVE ║\n"
                            "╚══════╝")
        
        
        buttons = [LIKE_BUTTON, 
                   DISLIKE_BUTTON,
                   RECOMMEND_BUTTON,
                   SAVE_BUTTON]
        
        
        buttons_lines = [button.splitlines() for button in buttons]
            
        # print(buttons_lines[self.radio_selection])
        buttons_lines[self.radio_selection] = list(map(bold, 
                                                       buttons_lines[self.radio_selection])
                                                   )
        
        # Concatenate the lines horizontally using zip and join
        result_lines = [f"{a}   {b}   {c}   {d}" 
                        for a, b, c, d in zip(*buttons_lines)]
        
        # Join the lines back into a multiline string
        buttons = "\n".join(result_lines)
        
        print(buttons) # Show buttons     
        
    
    def show_article_as_list_element(self, 
                                     show_delete:    bool = False,
                                     show_stats:     bool = False,
                                     bolded_article: bool = False,
                                     bolded_delete:  bool = False,
                                     bolded_stats:   bool = False):
        """
        Renders article as an ArticleList element.

        Parameters
        ----------
        show_delete : bool, optional
            If set to `True`, will render "Delete" button.
        show_stats : bool, optional
            If set to `True`, will render "Statistics" button. 
        bolded_article : bool, optional
            If set to `True`, the "article" button is selected.
        bolded_delete : bool, optional
            If set to `True`, the "delete" button is selected.
        bolded_stats : bool, optional
            IF set to `True`, the "statistics" button is selected.
        """
        
        horizontal_border_line = make_line("═", 140)
        border_line_top     = f"╔{horizontal_border_line}╗"
        border_line_bottom  = f"╚{horizontal_border_line}╝"
       
        article_widget = (f"{border_line_top}\n"
                          f"║{self.id:^5}║ {self.title:^132} ║\n"
                          f"{border_line_bottom}"
                          )
       
        widgets = [article_widget]
        
        if show_delete:
            delete_widget = ("╔══════════╗\n"
                             "║  DELETE  ║\n"
                             "╚══════════╝")
            
            widgets.append(delete_widget)
            
        if show_stats:
            stats_widget  = ("╔══════════════╗\n"
                             "║  STATISTICS  ║\n"
                             "╚══════════════╝")
            
            widgets.append(stats_widget)
        
        
        widgets_lines = [widget.splitlines() for widget in widgets]
        
        
        if bolded_article:
            widgets_lines[0] = list(map(bold, 
                                        widgets_lines[0])
                                   )      
            
        elif show_delete and bolded_delete:
            widgets_lines[1] = list(map(bold, 
                                        widgets_lines[1])
                                   ) 
            
        elif show_stats and bolded_stats:
            widgets_lines[2] = list(map(bold, 
                                        widgets_lines[2])
                                   )
        
        
        if show_delete and show_stats: 
            representation_lines = [f"{a}   {b}   {c}" for a, b, c in zip(*widgets_lines)]
            representation = "\n".join(representation_lines)
        
        elif show_delete:
            representation_lines = [f"{a}   {b}" for a, b in zip(*widgets_lines)]
            representation = "\n".join(representation_lines)
        
        else:
            representation = "\n".join(widgets_lines[0])       
            
            
        print(representation) # Show widgets
        
    
    def show_statistics(self):
        """
        Create a bar plot for likes, dislikes, and views
        """
        
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.5
        bar_positions = np.arange(3)

        ax.bar(bar_positions, [self.likes, self.dislikes, self.views],
               bar_width,
               color=["green", "red", "blue"])

        ax.set_xticks(bar_positions)
        ax.set_xticklabels(["Likes", "Dislikes", "Views"])
        ax.set_ylabel("Count")
        top_tags_str = ', '.join(self.tags)
        ax.set_title(f"Article #{self.id}: [{top_tags_str}]")

        plt.tight_layout()
        plt.show()
        
        
    def parse_keypress(self, key: str) -> str:
        """
        Parse keypress hit while the Article was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the Article was present - to be parsed.
        
        Returns
        -------
        str:
            Response to the main loop.
        """
        response = "" # Default response

        if key == "left": 
            if self.radio_selection > 0:
                self.radio_selection -= 1 # Move radio selection for one to the left
            
        elif key == "right": # Similar to the "left" case
            if self.radio_selection + 1 < self.radio_selection_size:    
                self.radio_selection += 1

        elif key == "enter": # Perform action of desired button
            button_name = self.button_names[self.radio_selection]
            response    = button_name
            
        elif key == "escape" or key == "esc":
            response = "load user profile"
            
            
        return response
    
        
    def increment_views(self):
        """
        Increments views of given article by one.
        """
        self.views += 1