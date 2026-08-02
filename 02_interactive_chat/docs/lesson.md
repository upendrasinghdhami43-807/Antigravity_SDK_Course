# Lesson 2: Interactive Chat

In this module we move from a simple script to an event loop.
- **What is an interactive chat?** It's a continuous `while True` loop that accepts user input, processes it, and displays the response.
- **Chat loop:** Handled by `ChatSession.run()`.
- **AI request lifecycle:** Input -> Agent -> API -> Response -> History -> Output.
- **Error handling:** Using try-except blocks to catch API errors.
- **Logging:** Saving all events to `logs/app.log`.
- **Future improvements:** Module 3 will introduce persistent memory.
