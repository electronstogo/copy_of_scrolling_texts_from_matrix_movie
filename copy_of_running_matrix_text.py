# 2018 - electronstogo

from tkinter import *
import random
import string


# fit these constants to modify the screen size, which shows the effect.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# resolution of text gaps.
NUMBER_OF_TEXTS = int(SCREEN_WIDTH / 15)




# class that keeps the properties of a letter.
class Letter:
    def __init__(self, color, letter):
        self.color = color
        self.letter = letter




# class that keeps the properties of a running text.
class Text:
    def __init__(self, coord_x, velocity):
        self.letter_list = []

        # initialize some letters for text
        for index in range(random.randint(30, 80)):
            # white color gradient
            if index < 5:
                color = (255 - index * 60, 255, 255 - index * 60)
            else:
                color = (80, 255, 80)

            letter = Letter(color, random.choice(string.ascii_letters))
            self.letter_list.append(letter)

        self.coord_x = coord_x
        self.coord_y = 0
        self.active = False
        self.velocity = velocity


    # draws itself into the screen.
    def draw_text(self, canvas):
        # loop the whole letter list of a text
        for index, letter in enumerate(self.letter_list):
            # if text has reached screen height, do a black fading to the letters
            if self.coord_y >= SCREEN_HEIGHT:
                if index >= int(len(self.letter_list) - ((self.coord_y - SCREEN_HEIGHT) / 15)):
                    r, g, b = self.letter_list[index].color
                    gradient = 15
                    if r - gradient > 0:
                        r -= gradient
                    if g - gradient > 0:
                        g -= gradient
                    if b - gradient > 0:
                        b -= gradient
                    self.letter_list[index].color = (r, g, b)

            # get color and draw letter
            if self.coord_y - index * 15 > 0:
                color = '#%02x%02x%02x' % self.letter_list[index].color
                canvas.create_text(self.coord_x, self.coord_y - index * 15, text=self.letter_list[index].letter,
                                   font="Times 13 ", fill=color)


        # forward text
        self.coord_y += self.velocity

        # switch 2nd letter to the 1st
        if random.randint(0, 1):
            self.letter_list[1].letter = self.letter_list[0].letter
            self.letter_list[0].letter = random.choice(string.ascii_letters)

        # change some letters in text
        for index in range(4):
            self.letter_list[random.randint(3, len(self.letter_list) - 1)].letter = random.choice(string.ascii_letters)



# class that controls the copy of the matrix screen.
class Matrix:
    def __init__(self):
        self.root = Tk()
        self.root.title('Copy of the scrolling Matrix texts')
        self.root.after(100, self.update)
        self.canvas = Canvas(self.root, bg='black', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, name="canvas")
        self.canvas.pack()

        self.text_list = []

        # init some text lines for beginning
        for index in range(NUMBER_OF_TEXTS):
            if random.randint(0, 20) > 17:
                text = Text(index * 15, random.randint(12, 17))
                self.text_list.append(text)

        self.root.mainloop()


    def update(self):
        self.canvas.delete("all")

        # loop through all text lines.
        for text in self.text_list:
            # delete texts that have reached the defined end.
            if text.coord_y > 3/2 * SCREEN_HEIGHT:
                self.text_list.remove(text)
                del text

        # create new text
        if random.randint(0, 20) > 2:
            coord_x = 0
            loop_counter = 0

            # search for free text index by limited random search.
            while self.text_exists(coord_x) and loop_counter < 20:
                coord_x = random.randint(0, NUMBER_OF_TEXTS) * 15
                loop_counter += 1

            # in the case of a free index, generate a new text and add it to the matrix.
            if loop_counter < 20:
                text = Text(coord_x, random.randint(12, 17))
                self.text_list.append(text)

        for text in self.text_list:
            text.draw_text(self.canvas)

        self.root.after(40, self.update)


    # check if a text exists at the given x coordinate.
    def text_exists(self, coord_x):
        for text in self.text_list:
            if text.coord_x == coord_x:
                return True

        return False



if __name__ == '__main__':
    Matrix()
