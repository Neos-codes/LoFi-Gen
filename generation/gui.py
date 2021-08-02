import tkinter as tk
from raters import TARGET_RATINGS
from generate import numInd, numBars, mutationRate, lazy_generate, dictyNotes

# Claves y valores del diccionario de pondeacion de raters
keys = list(TARGET_RATINGS.keys())
values = list(TARGET_RATINGS.values())

tonic_keys = list(dictyNotes.keys())

rate_names = ["Neighboring\nPitch\nRange", "Melody\nDirection", "Stability\nof\nMelody", "Pitch\nRange", "Continuos\nSilence", "Silences\nDensity", "Syncopaty\nin\nMelody", "Unique\nNote\nPitches", "Equal\nConsecutive", "Unique\nRythm\nValues"]

#print(TARGET_RATINGS.keys())
#print(TARGET_RATINGS.values())

def create_window():
    window = tk.Tk()
    window.title("LoF-AI")

    # Silders
    for i in range(10):
        slider = tk.Scale(window, from_ = 1, to = 0, resolution = 0.05, command = lambda val, rater = i: set_val(val, rater))
        slider.set(values[i])
        slider.grid(row = 1, column = i, padx = 5, pady = 5)
        label = tk.Label(window, text = rate_names[i])
        label.grid(row = 2, column = i)

    # Entries
    n_ind = tk.Entry(window, width = 5)
    n_bars = tk.Entry(window, width = 5)
    m_rate = tk.Entry(window, width = 5)
    n_iterations = tk.Entry(window, width = 5)
    n_ind.grid(row = 0, column = 1, pady = 10)
    n_bars.grid(row = 0, column = 3, pady = 10)
    m_rate.grid(row = 0, column = 5, pady = 10)
    n_iterations.grid(row = 0, column = 7, pady = 10)
    # Entries Labels
    l_ind = tk.Label(window, text = "Individuals")
    l_bars = tk.Label(window, text = "Bars")
    l_rate = tk.Label(window, text = "Mutation Rate")
    l_iterations = tk.Label(window, text = "Generations")
    l_ind.grid(row = 0, column = 0, padx = 5)
    l_bars.grid(row = 0, column = 2, padx = 5)
    l_rate.grid(row = 0, column = 4, padx = 5)
    l_iterations.grid(row = 0, column = 6, padx = 5)
    # Set text in Entries
    n_ind.insert(0, numInd)
    n_bars.insert(0, numBars)
    m_rate.insert(0, mutationRate)
    n_iterations.insert(0, "20")

    # Tonicas para las pistas (OptionMenu)
    clicked = tk.StringVar()
    clicked.set(tonic_keys[0])
    opt_menu = tk.OptionMenu(window, clicked, *tonic_keys)
    opt_menu.grid(row = 0, column = 9)
    
    # Label para el optionMenu de las tonicas
    l_optMenu = tk.Label(window, text = "Key")
    l_optMenu.grid(row = 0, column = 8)

    # Moods (OptionMenu)
    moods = ["Sad/Sentimental", "Contemplative/Dreamy", "Nostalgic/Emotional", "Abstract/Free"]
    mood = tk.StringVar()
    mood.set(moods[0])
    opt_moods = tk.OptionMenu(window, mood, *moods)
    opt_moods.grid(row = 0, column = 11, padx = 5)

    # Label para el optionMenu de las moods
    l_mood = tk.Label(window, text = "Mood")
    l_mood.grid(row = 0, column = 10)

    # Button to run
    button = tk.Button(window, text = "Generate!", command = lambda: generate(n_ind, n_bars, m_rate, n_iterations, clicked, mood, moods))
    button.grid(row = 3, column = 4, pady = 10)



# tk.optionmenu

    return window

    #slider = tk.Scale(window, from_ = 1, to = 0, resolution = 0.05)
    #slider.pack()

def set_val(val: float, rater: int):
    TARGET_RATINGS[keys[rater]] = float(val)
    print(keys[rater], val)

def generate(inds_: tk.Entry, bars_: tk.Entry, m_rate_: tk.Entry, n_iterations: tk.Entry, key: tk.StringVar, mood: tk.StringVar, moods: list):
    # Cast parameters
    numInd = int(inds_.get())
    numBars = int(bars_.get())
    mutationRate = float(m_rate_.get())
    mood_number = None
    # Change mood to number
    for i in range(4):
        if mood.get() == moods[i]:
            mood_number = i + 1

    lazy_generate(int(n_iterations.get()), key.get(), dictyNotes[key.get()], mood_number)


window = create_window()
window.mainloop()


#print(TARGET_RATINGS.keys())
#print(TARGET_RATINGS.values())
#window.mainloop()