import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from untitled import Ui_MainWindow


class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.work_dur = 25 * 60
        self.short_break_dur = 5 * 60
        self.long_break_dur = 15 * 60

        self.remaining_time = self.work_dur
        self.current_mode = "Pomodoro"
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.player = QMediaPlayer()
        self.player.setVolume(100)

        self.ui.btn_start.clicked.connect(self.start_timer)
        self.ui.btn_pause.clicked.connect(self.pause_timer)
        self.ui.pushButton_3.clicked.connect(self.reset_timer)
        self.ui.combo_mode.currentTextChanged.connect(self.change_mode)

        self.update_display()

    def start_timer(self):
        self.timer.start(1000)

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.change_mode()

    def change_mode(self):
        mode = self.ui.combo_mode.currentText()
        self.current_mode = mode

        if mode == "Pomodoro":
            self.remaining_time = self.work_dur
        elif mode == "Short Break":
            self.remaining_time = self.short_break_dur
        elif mode == "Long Break":
            self.remaining_time = self.long_break_dur

        self.update_display()

    def update_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.ui.label_timer.setText(f"{minutes:02}:{seconds:02}")


    def update_timer(self):
        self.remaining_time -= 1
        self.update_display()

        if self.remaining_time <= 0:
            self.timer.stop()


            if self.ui.checkbox_alert.isChecked():
                if self.current_mode == "Pomodoro":
                    self.show_notification("25 წუთი ამოიწურა, 5 წუთიანი შესვენების დროა!\n "
                                           "25 minutes are over! Time for a 5-minute break!")
                else:
                    self.show_notification("შესვენების დრო ამოიწურა, განაგრძე სწავლა! \n"
                                           " Break is over! Time to focus again!")


            if self.current_mode == "Pomodoro":
                self.play_break_music()
                self.current_mode = "Short Break"
                self.remaining_time = self.short_break_dur
                self.ui.combo_mode.blockSignals(True)
                self.ui.combo_mode.setCurrentText("შესვენება! "
                                                  "Short Break")
                self.ui.combo_mode.setEnabled(False)
            else:
                self.current_mode = "Pomodoro"
                self.remaining_time = self.work_dur
                self.ui.combo_mode.blockSignals(True)
                self.ui.combo_mode.setCurrentText("პომოდორო!"
                                                  "Pomodoro!")
                self.ui.combo_mode.blockSignals(False)

            self.update_display()
            self.timer.start(1000)

    def show_notification(self, message):
        QMessageBox.information(self, "Pomodoro Timer", message)


    def play_break_music(self):
        music_path = os.path.abspath("music/break_music.mp3")
        if os.path.exists(music_path):
            url = QUrl.fromLocalFile(music_path)
            self.player.setMedia(QMediaContent(url))
            self.player.play()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())