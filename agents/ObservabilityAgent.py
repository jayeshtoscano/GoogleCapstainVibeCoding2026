import time

class ObservabilityAgent:

    def start_timer(self):
        return time.time()

    def log(self, prompt, response, start):

        duration = time.time() - start

        print({
            "latency": duration,
            "prompt": prompt,
            "response": response
        })
