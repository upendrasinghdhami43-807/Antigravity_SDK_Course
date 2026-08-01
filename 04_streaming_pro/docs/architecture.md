# Architecture

Our streaming client uses an event-driven, decoupled architecture.

## 1. ChatEngine (Controller)
The main application loop. It handles taking user input and maintaining the flow of the application. It acts as the orchestrator.

## 2. StreamManager
The lifecycle controller for the stream. It connects the Agent (network), the Renderer (UI), and the Buffer (Storage). It monitors latency and controls cancellations.

## 3. StreamRenderer
Dedicated solely to output. It knows how to print things to the screen nicely. It handles the `flush=True` mechanics and setting up the Assistant's chat bubble.

## 4. StreamBuffer
Dedicated solely to data accumulation. It sits quietly collecting strings and returning them when the stream completes.

## 5. Agent
The API boundary. It wraps the `google.genai.Client` and exposes an asynchronous generator (`generate_stream`) that yields clean text strings, completely isolating the rest of the application from the underlying SDK's data structures.
