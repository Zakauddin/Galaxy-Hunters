import texts


class HighscoreFile:

    def __init__(self):
        super().__init__()
        self.file = open("highscore.csv", "r")
        self.fileInfo = []
        for i in self.file.readlines():
            self.fileInfo.append(i[:-1])
        self.file.close()
        self.labels = [texts.Text(self.fileInfo[0], 350, 150, 40), texts.Text(self.fileInfo[1], 850, 150, 40),
                       texts.Text(self.fileInfo[2], 350, 200, 40), texts.Text(self.fileInfo[3], 850, 200, 40),
                       texts.Text(self.fileInfo[4], 350, 250, 40), texts.Text(self.fileInfo[5], 850, 250, 40),
                       texts.Text(self.fileInfo[6], 350, 300, 40), texts.Text(self.fileInfo[7], 850, 300, 40),
                       texts.Text(self.fileInfo[8], 350, 350, 40), texts.Text(self.fileInfo[9], 850, 350, 40),
                       texts.Text(self.fileInfo[10], 350, 400, 40), texts.Text(self.fileInfo[11], 850, 400, 40),
                       texts.Text(self.fileInfo[12], 350, 450, 40), texts.Text(self.fileInfo[13], 850, 450, 40),
                       texts.Text(self.fileInfo[14], 350, 500, 40), texts.Text(self.fileInfo[15], 850, 500, 40),
                       texts.Text(self.fileInfo[16], 350, 550, 40), texts.Text(self.fileInfo[17], 850, 550, 40),
                       texts.Text(self.fileInfo[18], 350, 600, 40), texts.Text(self.fileInfo[19], 850, 600, 40)]
        for i in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]:
            self.fileInfo[i] = int(self.fileInfo[i])
        self.scores = []
        for i in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]:
            self.scores.append(self.fileInfo[i])

    def draw(self, screen, colour):
        for label in self.labels:
            label.draw(screen, colour)

    def newScore(self, score, username):
        if score > self.fileInfo[19]:
            self.scores.append(score)
            self.scores.sort(reverse=True)

            n = 0
            for i in range(0, len(self.scores)):
                if score == self.scores[i]:
                    n = i * 2
                    print(n)

            self.fileInfo.append("")
            self.fileInfo.append("")

            for j in range(21, n+1, -1):
                self.fileInfo[j] = self.fileInfo[j-2]

            self.fileInfo[n] = username
            self.fileInfo[n + 1] = score

            self.file = open("highscore.csv", "w")
            for value in range(0, 20):
                self.file.write(str(self.fileInfo[value]) + "\n")
            self.file.close()
