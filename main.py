from tkinter import *
import random
import string as strg


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

NUMBER_OF_TEXTS = int(SCREEN_WIDTH / 15)



class Letter:
    def __init__(self, color, letter):
        self.color = color
        self.letter = letter


class Text:
    def __init__(self, coordX, velocity):

        self.letterList = []
        # initialize some letters for text
        for index in range(random.randint(30, 80)):
            # white color gradient
            if index < 5:
                color = (255 - index * 60, 255, 255 - index * 60)
            else:
                color = (80, 255, 80)
            letter = Letter(color, random.choice(strg.ascii_letters))
            self.letterList.append(letter)

        self.coordX = coordX
        self.coordY = 0
        self.active = False
        self.velocity = velocity

    def drawText(self, canvas):

        # loop the whole letter list of a text
        for index, letter in enumerate(self.letterList):

            #if text has reached screen height, do black fading to the letters
            if self.coordY >= SCREEN_HEIGHT:
                if index >= int(len(self.letterList) - ((self.coordY - SCREEN_HEIGHT) / 15)):
                    r, g, b = self.letterList[index].color
                    gradient = 15
                    if r - gradient > 0:
                        r -= gradient
                    if g - gradient > 0:
                        g -= gradient
                    if b - gradient > 0:
                        b -= gradient
                    self.letterList[index].color = (r, g, b)

            # get color and draw letter
            if self.coordY - index * 15 > 0:
                color = '#%02x%02x%02x' % self.letterList[index].color
                canvas.create_text(self.coordX, self.coordY - index * 15, text=self.letterList[index].letter, font="Times 13 ", fill=color)


        # forward text
        self.coordY += self.velocity

        # switch 2nd letter to the 1st
        if random.randint(0, 1):
            self.letterList[1].letter = self.letterList[0].letter
            self.letterList[0].letter = random.choice(strg.ascii_letters)

        # change some letters in text
        for index in range(4):
            self.letterList[random.randint(3, len(self.letterList) - 1)].letter = random.choice(strg.ascii_letters)




class Matrix:
    def __init__(self):
        self.root = Tk()
        self.root.after(100, self.update)
        self.canvas = Canvas(self.root, bg='black', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, name="canvas")
        self.canvas.pack()

        self.textList = []

        # init some text lines for beginning
        for index in range(NUMBER_OF_TEXTS):
            if random.randint(0, 20) > 17:
                text = Text(index * 15, random.randint(12, 17))
                self.textList.append(text)


        self.root.mainloop()

    def update(self):
        self.canvas.delete("all")

        for text in self.textList:
            if text.coordY > 3/2 * SCREEN_HEIGHT:
                self.textList.remove(text)
                del text

        # create new text
        if random.randint(0,20) > 2:
            xCoord = 0
            loopCounter = 0

            # check if this position is already taken
            while self.textExists(xCoord) and loopCounter < 20:
                xCoord = random.randint(0, NUMBER_OF_TEXTS) * 15
                loopCounter += 1
            if loopCounter < 20:
                text = Text(xCoord, random.randint(12, 17))
                self.textList.append(text)

        for text in self.textList:
            text.drawText(self.canvas)

        self.root.after(40, self.update)


    def textExists(self, coordX):
        for text in self.textList:
            if text.coordX == coordX:
                return True

        return False



if __name__ == '__main__':
    Matrix()