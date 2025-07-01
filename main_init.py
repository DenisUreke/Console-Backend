import pygame
import time
from Sound_Manager.sound_manager import SoundManager
from Player_Manager.player_manager import PlayerManager
from Message_Parser.message_parser import MessageParser
from Broadcasting_Manager.broadcasting_manager import BroadcastingManager
from Controller_Functions.Controller_Translator.controller_translator import ControllerTranslator
from Orchestrator.orchestrator import Orchestrator
from Websocket_Service.websocket_service import WebSocketServer

def initialize_game():
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Lobby")
    clock = pygame.time.Clock()
    pygame.font.init()
    
    # Initialize classes for orchestrator
    sounds_manager = SoundManager()
    player_manager = PlayerManager()
    message_parser = MessageParser()
    broadcasting_manager = BroadcastingManager()
    controller_translator = ControllerTranslator()
    
    # Initialize orchestrator
    orchestrator = Orchestrator(
        screen= screen,
        sound_manager= sounds_manager,
        player_manager= player_manager,
        message_parser= message_parser,
        broadcasting_manager= broadcasting_manager,
        controller_translator= controller_translator
    )
    
    # Initialize Websocket 
    server = WebSocketServer(orchestrator)
    
    return {
        "clock": clock,
        "orchestrator": orchestrator,
        "server": server
    }
    