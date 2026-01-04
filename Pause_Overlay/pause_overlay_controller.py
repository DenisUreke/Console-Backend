class PauseOverlayController:
    def __init__(self, orchestrator, model):
        self.orchestrator = orchestrator
        self.model = model

    def stop(self): pass
    def update(self, dt_ms: int): pass

    def handle_input(self, translated_payload):
        if not translated_payload:
            return

        if translated_payload.get("type") == "pause_toggle":
            self.orchestrator.toggle_pause(translated_payload.get("player_number"))
