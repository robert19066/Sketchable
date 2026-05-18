from time import time, sleep

class Ticky:
    def __init__(self, max_fps=None, smoothing=0.9):
        self.start_time = time()
        self.last_time = self.start_time
        self.tick_count = 0

        self.max_fps = max_fps
        self.min_frame_time = 1 / max_fps if max_fps else None

        self.smoothing = smoothing
        self._smoothed_fps = 0.0

        self.paused = False
        self._pause_time = 0.0

        self.frame_times = []  # debug history (last frames)
        self.max_history = 120

    def tick(self):
        if self.paused:
            return 0.0

        current_time = time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        self.tick_count += 1

        # store frame history
        self.frame_times.append(delta_time)
        if len(self.frame_times) > self.max_history:
            self.frame_times.pop(0)

        # FPS smoothing
        if delta_time > 0:
            fps = 1 / delta_time
            self._smoothed_fps = (
                self._smoothed_fps * self.smoothing +
                fps * (1 - self.smoothing)
            )

        # FPS cap (simple sleep limiter)
        if self.min_frame_time:
            if delta_time < self.min_frame_time:
                sleep(self.min_frame_time - delta_time)

        return delta_time

    def get_fps(self):
        elapsed = time() - self.start_time
        return self.tick_count / elapsed if elapsed > 0 else 0.0

    def get_smoothed_fps(self):
        return self._smoothed_fps

    def get_avg_frame_time(self):
        if not self.frame_times:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times)

    def reset(self):
        self.start_time = time()
        self.last_time = self.start_time
        self.tick_count = 0
        self.frame_times.clear()
        self._smoothed_fps = 0.0

    def pause(self):
        self.paused = True
        self._pause_time = time()

    def resume(self):
        if self.paused:
            paused_duration = time() - self._pause_time
            self.last_time += paused_duration
        self.paused = False

    def get_delta_time(self):
        if self.frame_times:
            return self.frame_times[-1]
        return 0.0