from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class MediaPlayer(QWidget):
    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        
        layout = QVBoxLayout(self)
        
        controls = QHBoxLayout()
        
        self.play_button = QPushButton("▶ Воспроизвести")
        self.play_button.clicked.connect(self.play_music)
        controls.addWidget(self.play_button)
        
        self.stop_button = QPushButton("⏹ Стоп")
        self.stop_button.clicked.connect(self.stop_music)
        controls.addWidget(self.stop_button)
        
        layout.addLayout(controls)
        
    def play_music(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("▶ Воспроизвести")
        else: 
            self.player.stop()
            self.play_button.setText("⏸ Пауза")
            
    def stop_music(self):
        self.player.stop()
        self.play_button.setText("▶ Воспроизвести")
        