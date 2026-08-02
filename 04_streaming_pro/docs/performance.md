# Performance Metrics

In streaming applications, standard "Total Response Time" is not enough to measure user experience. We must measure specific streaming metrics.

## First-Token Latency
Also known as "Time to First Byte" (TTFB). This is the exact time (in seconds) between when the user hits Enter, and when the very first character is printed to their screen. This is the most critical metric for perceived performance. Anything under 1.0 second feels instantaneous.

## Tokens per Second
Calculated as `Total Tokens / Total Response Time`. This measures the throughput of the model. 

## Characters per Second
Similar to Tokens per second, but easier for laymen to understand. It measures how fast the text is physically appearing on the screen.

In this module, all of these metrics are tracked in the `StatisticsManager` and can be viewed at any time by typing `/stats`.
