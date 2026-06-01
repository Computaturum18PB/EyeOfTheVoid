import os
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QFileDialog, QListWidget, QLabel, QSplitter
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from utils.data_reader import get_player_state
from core.environment_variables import CONTENT_PATH, MUSIC_1_PATH, MUSIC_2_PATH, MUSIC_3_PATH, MUSIC_4_PATH, MUSIC_5_PATH, DIALOG_CHOOSE_MUSIC_FILE

class MediaPlayer(QWidget):
    def __init__(self):
        super().__init__()
        
        self.playlist = [MUSIC_1_PATH, MUSIC_2_PATH, MUSIC_3_PATH, MUSIC_4_PATH, MUSIC_5_PATH]
        self.current_music_index = 0
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)
        
        splitter = QSplitter(self)
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.music_list_title = QLabel()
        left_layout.addWidget(self.music_list_title)
        
        self.music_list = QListWidget()
        self.music_list.itemDoubleClicked.connect(self.play_selected_music)
        left_layout.addWidget(self.music_list)
        
        self.add_music_button = QPushButton()
        self.add_music_button.clicked.connect(self.add_music)
        left_layout.addWidget(self.add_music_button)
        
        splitter.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.current_music_label = QLabel()
        right_layout.addWidget(self.current_music_label)
        
        controls = QHBoxLayout()
        
        self.previous_button = QPushButton()
        self.previous_button.clicked.connect(self.previous_music)
        controls.addWidget(self.previous_button)
        
        self.next_button = QPushButton()
        self.next_button.clicked.connect(self.next_music)
        controls.addWidget(self.next_button)
        
        self.play_text = get_player_state(CONTENT_PATH, 0)
        self.pause_text = get_player_state(CONTENT_PATH, 2)
        self.play_button = QPushButton(self.play_text)
        self.play_button.clicked.connect(self.toggle_play)
        controls.addWidget(self.play_button)
        
        self.stop_text = get_player_state(CONTENT_PATH, 1)
        self.stop_button = QPushButton(self.stop_text)
        self.stop_button.clicked.connect(self.stop_music)
        controls.addWidget(self.stop_button)
        
        right_layout.addLayout(controls)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([100, 400])

        self.update_music_list()

        if self.playlist:
            self.current_music_index = 0
            self.update_music_label()
            
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
    
    def update_music_list(self):
        self.music_list.clear()
        for path in self.playlist:
            music_name = os.path.basename(path)
            music_name = os.path.splitext(music_name)[0]
            self.music_list.addItem(music_name)
    
    def add_music(self):        
        files, _ = QFileDialog.getOpenFileNames(
            self, DIALOG_CHOOSE_MUSIC_FILE, "",
            "Audio Files (*.mp3);;All Files (*.*)"
        )
        
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                music_name = os.path.basename(file)
                music_name = os.path.splitext(music_name)[0]
                self.music_list.addItem(music_name)
    
    def play_selected_music(self, item):
        index = self.music_list.row(item)
        self.current_music_index = index
        self.play_current_music()
    
    def play_current_music(self):
        self.player.setSource(QUrl.fromLocalFile(self.playlist[self.current_music_index]))
        self.player.play()
        self.play_button.setText(self.pause_text)
        self.update_music_label()
        self.music_list.setCurrentRow(self.current_music_index)
    
    def update_music_label(self):
        music_name = os.path.basename(self.playlist[self.current_music_index])
        music_name = os.path.splitext(music_name)[0]
        self.current_music_label.setText(get_player_state(CONTENT_PATH, 8) + music_name)
    
    def next_music(self):
        self.current_music_index = (self.current_music_index + 1) % len(self.playlist)
        self.play_current_music()
    
    def previous_music(self):
        self.current_music_index = (self.current_music_index - 1) % len(self.playlist)
        self.play_current_music()
    
    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText(self.play_text)
        else: 
            self.player.play()
            self.play_button.setText(self.pause_text)
    
    def stop_music(self):
        self.player.stop()
        self.play_button.setText(self.play_text)
    
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_music()
    
    def update_content(self):
        self.play_text = get_player_state(CONTENT_PATH, 0)
        self.pause_text = get_player_state(CONTENT_PATH, 2)
        self.stop_text = get_player_state(CONTENT_PATH, 1)
        self.dont_choose = get_player_state(CONTENT_PATH, 3)
        self.back = get_player_state(CONTENT_PATH, 4)
        self.next = get_player_state(CONTENT_PATH, 5)
        self.add = get_player_state(CONTENT_PATH, 6)
        self.list = get_player_state(CONTENT_PATH, 7)
        
        self.music_list_title.setText(self.list)
                
        self.next_button.setText(self.next)
        self.previous_button.setText(self.back)
        
        music_name = os.path.basename(self.playlist[self.current_music_index])
        music_name = os.path.splitext(music_name)[0]
        self.current_music_label.setText(get_player_state(CONTENT_PATH, 8) + music_name)
        
        self.stop_button.setText(self.stop_text)
        self.add_music_button.setText(self.add)
        
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.play_button.setText(self.pause_text)
        else:
            self.play_button.setText(self.play_text)
            