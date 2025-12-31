# Copilot / AI-Agent Instructions for Console-Backend

Purpose: short, actionable guidance so an AI coding assistant can be immediately productive in this repository.

**Big picture**
- **Entry points:** `main.py` (primary runner) and `main_init.py` (initial setup). Start here to run the application locally.
- **Services & responsibilities:**
  - `Websocket_Service/websocket_service.py` — single source of truth for network I/O with clients. Most cross-component messages arrive here.
  - `Broadcasting_Manager/broadcasting_manager.py` — publishes events to interested components and clients.
  - `Orchestrator/orchestrator.py` — high-level game flow and orchestration between Lobby, Games, and Player Manager.
  - `Database_Service/database_service.py` — persistence layer (see `tables.sql`).

**Architecture & patterns (what to expect)**
- Project follows a component + MVC-ish pattern: many features are grouped into folders that contain `*_controller.py`, `*_model.py`, and `*_view.py` (examples: `Welcome_Screen`, `Pause_Overlay`, `Team_Selection`, `Lobby`).
- Input handling (controllers) is separated from rendering (views) and state (models). When adding features follow the same three-file grouping.
- Controller implementations usually implement interfaces found in `Interfaces/` (notably `controller_interface.py` and `controller_handler_interface.py`). Use these interfaces when adding or refactoring controllers.
- Joystick / input handling lives in `Controller_Functions/Joystick_Handlers/` (e.g., `button_handlers.py`, `joystick_handlers.py`, `keypad_handlers.py`). These handlers are small utilities called by controllers.
- Message parsing and routing to controllers: `Message_Parser/message_parser.py`. To see how external messages map to in-app actions, inspect this parser and `Websocket_Service` together.
- Enums: application-wide constants and message types are stored in `Enums/` (e.g., `state_enum.py`, `ws_type_enum.py`, `controller_enum.py`). Use them rather than adding ad-hoc strings.

**Key integration points**
- Network: `Websocket_Service/websocket_service.py` receives/sends JSON/text messages. Follow existing JSON shapes used in `Message_Parser/message_parser.py`.
- Broadcasts: publishing events should go through `Broadcasting_Manager/broadcasting_manager.py` to ensure consistent fan-out.
- Persistence: use `Database_Service/database_service.py` for reads/writes. Look at `tables.sql` for schema expectations.
- Game flow: `Orchestrator/orchestrator.py` is the place to modify global game transitions (start, end, lobby -> game).

**Developer workflows**
- Install deps: `pip install -r requirements.txt` (project is Python; requirements.txt exists at repo root).
- Run (local): `python main.py` from the repo root — this starts normal runtime. If a separate initialization path is needed try `python main_init.py`.
- Debugging tips: attach debugger to `main.py` or set breakpoints inside `Websocket_Service` to inspect incoming message handling. Use `logging` statements added near `Message_Parser` or `Broadcasting_Manager` to trace flows.

**Project-specific conventions**
- File naming: snake_case for modules, directories for feature groups (e.g., `Welcome_Screen` contains related controller/model/view files).
- Controller/View/Model naming convention: featureXYZ_controller.py, featureXYZ_model.py, featureXYZ_view.py. New features should follow this split.
- Use enums in `Enums/` for any message/state/value that must be shared.
- When adding new public API surface or message types, update `Message_Parser/message_parser.py` and the relevant `ws_type_enum.py` entry.

**Where to make common edits (examples)**
- Add a new UI flow called `example`: create `Example/` with `example_controller.py`, `example_model.py`, `example_view.py` and wire into `Orchestrator` or the Lobby depending on scope.
- Add a new WebSocket message type: add enum to `Enums/ws_type_enum.py`, handle parsing in `Message_Parser/message_parser.py`, then emit events via `Broadcasting_Manager`.
- Add persistence fields: update `tables.sql`, migrate DB schema via the existing `Database_Service` patterns before writing new DB calls.

**Quick-file map (start here)**
- Root runner: `main.py`, `main_init.py`
- Network: `Websocket_Service/websocket_service.py`, `Message_Parser/message_parser.py`
- Broadcast & events: `Broadcasting_Manager/broadcasting_manager.py`
- Orchestration: `Orchestrator/orchestrator.py`
- Controllers & input: `Controller_Functions/`, `Lobby/`, `Games/`, `Welcome_Screen/` (search for `*_controller.py`)
- Persistence: `Database_Service/database_service.py`, `tables.sql`

If you need more detail in any area (message formats, DB schema, or a walkthrough for adding a new controller), say which part you want expanded and I will add targeted examples and test commands.

-- End of file
