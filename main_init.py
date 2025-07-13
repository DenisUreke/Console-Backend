import pygame
import time
from Sound_Manager.sound_manager import SoundManager
from Player_Manager.player_manager import PlayerManager
from Message_Parser.message_parser import MessageParser
from Broadcasting_Manager.broadcasting_manager import BroadcastingManager
from Controller_Functions.Controller_Translator.controller_translator import ControllerTranslator
from Orchestrator.orchestrator import Orchestrator
from Websocket_Service.websocket_service import WebSocketServer
from Database_Service.database_service import DatabaseService

def initialize_game():
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("DenPi")
    clock = pygame.time.Clock()
    pygame.font.init()
    
    # Initialize classes for orchestrator
    sounds_manager = SoundManager()
    player_manager = PlayerManager()
    message_parser = MessageParser()
    broadcasting_manager = BroadcastingManager()
    controller_translator = ControllerTranslator()
    database_service = DatabaseService()
    
    # Initialize orchestrator
    orchestrator = Orchestrator(
        screen= screen,
        sound_manager= sounds_manager,
        player_manager= player_manager,
        message_parser= message_parser,
        broadcasting_manager= broadcasting_manager,
        controller_translator= controller_translator,
        database_service= database_service
    )
    
    # Initialize Websocket 
    server = WebSocketServer(orchestrator)
    orchestrator.websocket_server = server
    
    return {
        "clock": clock,
        "orchestrator": orchestrator,
        "server": server
    }
    