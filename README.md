# epics-at-jwc

epics-at-jwc is a small project that enables safe, two-way serial control of a motion system and produces G-code for handwritten characters using a connected G-code database.

## Key features

1. Two-way serial communication
   - Full-duplex serial interface for sending commands to, and receiving responses/status from, the controller.
   - Message framing, retries, timeouts, and acknowledgements to improve reliability.
   - Telemetry and status parsing to keep the host synchronized with the machine (position, buffer state, errors).

2. Bounds check and emergency-stop (E-STOP) G-code writer
   - G-code generator performs workspace bounds checks (X/Y/Z limits, axis travel ranges) before emitting motion commands.
   - If a planned move would exceed limits or a hardware/software fault is detected, the writer emits an immediate E-STOP sequence to safely halt the machine.
   - E-STOP behavior:
     - Emits a configurable emergency sequence (e.g., an immediate stop G-code like `M112` or firmware-specific equivalent).
     - Optionally follows with safe park/disable commands if configured.
     - Logs and reports the fault over the serial link so the host and operator are informed.

3. G-code writer connected to a G-code database for handwritten characters
   - Stroke data for handwritten characters is stored in a small, queryable G-code database (formats supported: SQLite/JSON or similar).
   - The writer composes G-code from stroke primitives (moves, pen up/down / spindle on/off, feedrates) and applies scaling, rotation, and position offsets so characters can be rendered at arbitrary positions and sizes.
   - Supports concatenation and kerning of characters, configurable feedrates, and optional dwell/ink-lift behavior between strokes.

## Architecture overview

- Serial Interface
  - Handles port configuration (baud, parity, flow control), message framing, and two-way messaging.
  - Exposes APIs for sending commands and registering handlers for incoming telemetry and status.

- G-code Writer
  - Produces validated G-code sequences, performs bounds checks, and emits emergency sequences when needed.
  - Uses configurable motion primitives and safety limits.

- G-code Database
  - Stores and serves character stroke data used by the writer.
  - Provides a simple API to retrieve stroke sequences by character or glyph ID.

## Getting started

Requirements
- C++ compiler (Clang or GCC) and the toolchain used by the project.
- A serial device or simulator (e.g., /dev/ttyUSB0 on Linux) for testing.

Example serial configuration (example TOML):
```toml
[serial]
port = "/dev/ttyUSB0"
baud = 115200
parity = "None"
timeout_ms = 500
```

Example bounds configuration:
```toml
[bounds]
x_min = 0.0
x_max = 200.0
y_min = 0.0
y_max = 200.0
z_min = 0.0
z_max = 100.0
```

Example E-STOP config:
```toml
[estop]
command = "M112"         # firmware-specific emergency stop
post_commands = ["M84"]  # optional commands to disable steppers
```

Running (high-level)
1. Configure serial port and motion bounds in the project's config file.
2. Start the application; it opens the serial port and begins two-way communication.
3. Use the G-code writer API/CLI to render characters. The writer checks bounds and will emit an E-STOP if a move is unsafe.

## Safety notes

- Always verify workspace limits before enabling motors.
- Test E-STOP behavior in a safe environment with motors unloaded or disabled.
- Respect firmware-specific emergency-stop semantics — change the E-STOP command to match the target controller.

## Testing

- Unit tests for stroke-to-G-code conversion, bounds checking, and emergency logic.
- Integration tests using a simulator or a hardware-in-the-loop setup to validate serial comms and E-STOP response.

## Contributing

- Open issues or pull requests with a clear description and tests where appropriate.
- Prefer small, focused changes that include tests and documentation updates.

## License

- See the repository LICENSE file for details.

## Maintainer

- eazhang28
