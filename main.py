from tkinter import *
from PIL import Image, ImageTk

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 5
SHORT_BREAK_MIN = 2
LONG_BREAK_MIN = 3

# REP is a counter to determine the count down time
# rep 1357 -> 25min work count donw,
# rep 246 -> 5min break countdown
# rep 8 -> 20min long break countdown
REP = 0  # total of 8 reps

# Var_name for window.after() inside "count_down" function,
# Refer to it later to cancel timer, in "reset_timer" function
TIMER = None

# saves the time when the timer is paused
TIMER_PAUSED_AT = None


# ---------------------------- TIMER PAUSE ------------------------------- #

def pause_timer():
    # First cancel the timer, then save the time when it is paused
    window.after_cancel(TIMER)

    global TIMER_PAUSED_AT
    TIMER_PAUSED_AT = canvas.itemcget(timer_text, option='text')  # -> str


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(TIMER)

    canvas.itemconfig(timer_text, text=f"00:00")  # reset time
    timer_label.config(text="Timer", fg=GREEN)  # reset timer label
    check_mark_label.config(text=f"")  # reset check marks

    # resets the global rep counter, and timer_paused_at (incase timer has been paused before)
    global REP, TIMER_PAUSED_AT
    REP = 0
    TIMER_PAUSED_AT = None


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REP, TIMER_PAUSED_AT

    # first check if timer has been paused, if so, don't update rep, just keep count_down at paused time
    if TIMER_PAUSED_AT != None:

        # split the TIME_PAUSED_AT (str) to count_min, and count_sec (int)
        time = TIMER_PAUSED_AT.split(":")
        count_min = int(time[0])
        count_sec = int(time[1])

        TIMER_PAUSED_AT = None  # reset after time resumed
        count = count_min * 60 + count_sec  # [sec]
        count_down(count)

    else:

        # The regular functionality of start_timer()
        REP += 1
        print(f"REP = {REP}")

        # Calculates num of work session done and show ✔
        work_session_completed = int(REP / 2)
        check_marks = "✔" * work_session_completed
        check_mark_label.config(text=f"{check_marks}")

        # Determine if it's a work/break count down
        if REP > 8:
            REP = 0  # reset and not call itself again
            timer_label.config(text="Timer", fg=GREEN)
        elif REP % 2 != 0:
            # This means rep 1357
            count_down(int(WORK_MIN * 60))
            timer_label.config(text="Work", fg=GREEN)
        elif REP == 8:
            count_down(int(LONG_BREAK_MIN * 60))
            timer_label.config(text="Breakkk", fg=RED)
        else:
            timer_label.config(text="Break", fg=PINK)
            count_down(int(SHORT_BREAK_MIN * 60))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    """Performs a count down in units of second, on the canvas"""
    count_min = int(count / 60)
    count_sec = count % 60

    # formatting the time to like a clock 06:21
    if count_min < 10:
        count_min = f"0{count_min}"
        # Note: this is known as dynamic typing (type as in var type)
        #       In this case, "count_min" switched from an int() to a str()
        #       not all programming language can do this (e.g. can't in C, Java, Swift)

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # time_text is the var_name of the canvas text when it's first created
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global TIMER
        TIMER = window.after(1000, count_down, count - 1)
        # window.after performs action (count_down) after x [ms]
        # the last input is *args which is for the function, in this case we pass in "count-1"
    else:
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=YELLOW)

# ----- Canvas
canvas = Canvas(width=205, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')  # PhotoImage is a class that opens a pic
canvas.create_image(102, 112, image=tomato_img)
# putting canvas into a var -> to change text later
timer_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=2)

# ----- Label
timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW, width=7)
timer_label.grid(row=1, column=2)

check_mark_label = Label(text="", font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
check_mark_label.grid(row=4, column=2)

# ----- Button
# loading an image to use for the button
button_image_file = Image.open("button_image.png")
button_image_file_resized = button_image_file.resize((45, 22))
button_img = ImageTk.PhotoImage(button_image_file_resized)

# create button using image and text (compound)
# then remove button bg
start_button = Button(text="Start", image=button_img, compound="center",
                      font=("arial", 10, "normal"), highlightthickness=0,
                      border=0, borderwidth=0, relief=FLAT, bg=YELLOW)
start_button.config(command=start_timer)
start_button.grid(row=3, column=1)

reset_button = Button(text="Reset", image=button_img, compound="center",
                      font=("arial", 10, "normal"), highlightthickness=0,
                      border=0, borderwidth=0, relief=FLAT, bg=YELLOW)
reset_button.config(command=reset_timer)
reset_button.grid(row=3, column=3)

pause_button = Button(text="Pause", image=button_img, compound="center",
                      font=("arial", 10, "normal"), highlightthickness=0,
                      border=0, borderwidth=0, relief=FLAT, bg=YELLOW)
pause_button.config(command=pause_timer)
pause_button.grid(row=3, column=2)

window.mainloop()
