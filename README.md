# DenPi Console (Raspberry Pi Game Console)

A small Raspberry Pi–based game console project where players use their phones as controllers.

The console runs a Python backend (with Pygame for the on-screen UI) and hosts a small Angular web app that acts as a controller. Players connect over Wi-Fi, open the controller page, and send input to the console in real time using WebSockets.

## What it does
- Runs a “console app” on a Raspberry Pi (Python + Pygame)
- Hosts a web-based controller UI (Angular)
- Players join by scanning a QR code shown on the console screen
- Login creates a player with:
  - player id
  - unique controller color theme
  - session token for reconnects
- Supports multiple players and a leader system (one person navigates menus)
- If everyone disconnects, the console pauses and shows the QR code again

## Architecture (high level)
- **Console (Raspberry Pi)**
  - Backend: Python + Pygame (game loop, state machine, player management)
  - Web server: serves the Angular controller
  - WebSockets: real-time channel between phone and console
- **Phone**
  - Browser loads the controller UI over Wi-Fi
  - Sends controller input (buttons/joystick/keypad) over WebSockets

## Why an Orchestrator?
Both backend and frontend use an “orchestrator” approach:
- Keeps track of the current state
- Switches active views/controllers at runtime
- Delegates work to services (sound, players, broadcasting, input translation)

## Getting started (dev notes)
- Start the backend on the Raspberry Pi (console app)
- Start/serve the Angular controller
- Connect your phone to the same network and open the controller URL (or scan the QR code)

> This project is under active development and the architecture will evolve as more games and controller types are added.


https://github.com/user-attachments/assets/cf4e0720-5609-4be8-9e5e-f0e6749424bc

