from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.run = 0
        with open("data.txt") as data:
            self.high_score = int(data.read())
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.run} High Score: {self.high_score}", align="center", font=("Arial", 24, "normal"))

    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write("Game Over", align="center", font=("Arial", 24, "normal"))

    def reset(self):
        if self.run > self.high_score:
            self.high_score = self.run
            with open("data.txt", "w") as data:
                data.write(f"{self.high_score}")

        self.run = 0
        self.update_score()

    def increase(self):
        self.run += 500
        self.clear()
        self.update_score()