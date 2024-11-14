from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QMessageBox, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QRect
import sys

class PingPongGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.setWindowTitle("Ping Pong Game - Player vs. Computer")
        self.setGeometry(100, 100, 800, 400)
        self.setFixedSize(800, 400)
        
        # Game settings
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.paddle_speed = 20
        self.ai_speed = 4  # Speed of the AI paddle
        self.score_player = 0
        self.score_ai = 0
        self.game_time = 60  # Game duration in seconds
        
        # Ball and paddles
        self.ball = QRect(390, 190, 20, 20)
        self.player_paddle = QRect(30, 150, 10, 100)
        self.ai_paddle = QRect(760, 150, 10, 100)
        
        # Timer to update the game
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)  # Update every 30 ms
        
        # Game countdown timer
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update every 1 second
        
    def keyPressEvent(self, event):
        # Controls for player (W and S keys)
        if event.key() == Qt.Key_W and self.player_paddle.top() > 0:
            self.player_paddle.moveTop(self.player_paddle.top() - self.paddle_speed)
        elif event.key() == Qt.Key_S and self.player_paddle.bottom() < self.height():
            self.player_paddle.moveTop(self.player_paddle.top() + self.paddle_speed)
    
    def update_game(self):
        # Update the ball position
        self.ball.moveLeft(self.ball.left() + self.ball_speed_x)
        self.ball.moveTop(self.ball.top() + self.ball_speed_y)
        
        # Ball collision with top or bottom wall
        if self.ball.top() <= 0 or self.ball.bottom() >= self.height():
            self.ball_speed_y = -self.ball_speed_y
        
        # Ball collision with paddles
        if self.ball.intersects(self.player_paddle) or self.ball.intersects(self.ai_paddle):
            self.ball_speed_x = -self.ball_speed_x
            
        # Check if the ball goes out of bounds
        if self.ball.left() <= 0:  # AI scores
            self.score_ai += 1
            self.reset_ball()
        elif self.ball.right() >= self.width():  # Player scores
            self.score_player += 1
            self.reset_ball()
        
        # Move the AI paddle
        self.move_ai_paddle()
        
        # Redraw the window
        self.update()
    
    def reset_ball(self):
        # Reset ball to the center and reverse direction
        self.ball.moveTo(390, 190)
        self.ball_speed_x = -self.ball_speed_x  # Change direction
    
    def move_ai_paddle(self):
        # AI paddle follows the ball's vertical position with some speed limit
        if self.ball.center().y() > self.ai_paddle.center().y() and self.ai_paddle.bottom() < self.height():
            self.ai_paddle.moveTop(self.ai_paddle.top() + self.ai_speed)
        elif self.ball.center().y() < self.ai_paddle.center().y() and self.ai_paddle.top() > 0:
            self.ai_paddle.moveTop(self.ai_paddle.top() - self.ai_speed)
    
    def update_countdown(self):
        # Update game timer
        self.game_time -= 1
        if self.game_time <= 0:
            self.end_game()
    
    def end_game(self):
        # Stop the game timers
        self.timer.stop()
        self.countdown_timer.stop()
        
        # Determine the winner
        if self.score_player > self.score_ai:
            winner = "Player"
        elif self.score_ai > self.score_player:
            winner = "Computer"
        else:
            winner = "Draw"
        
        # Show the final score and winner
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"Time's up!\n\nPlayer Score: {self.score_player}\nComputer Score: {self.score_ai}\n\nWinner: {winner}")
        msg_box.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        
        # Show the dialog box and check if the player wants to play again or exit
        result = msg_box.exec()
        if result == QMessageBox.Retry:
            self.restart_game()
        else:
            self.close()
    
    def restart_game(self):
        # Reset scores, ball, paddles, and timer
        self.score_player = 0
        self.score_ai = 0
        self.game_time = 60
        self.reset_ball()
        self.timer.start(30)
        self.countdown_timer.start(1000)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Background color
        painter.setBrush(QBrush(QColor(30, 30, 30)))
        painter.drawRect(self.rect())
        
        # Draw paddles
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(self.player_paddle)
        painter.drawRect(self.ai_paddle)
        
        # Draw ball
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawEllipse(self.ball)
        
        # Draw score and timer
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(300, 50, f"Player: {self.score_player}")
        painter.drawText(450, 50, f"Computer: {self.score_ai}")
        painter.drawText(360, 20, f"Time: {self.game_time} s")

def main():
    app = QApplication(sys.argv)
    game = PingPongGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
