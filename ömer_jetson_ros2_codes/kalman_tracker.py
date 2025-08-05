class KalmanTracker:
    def __init__(self):
        self.estimate = [0.5, 0.5]
        self.alpha = 0.5

    def update(self, measurement):
        if measurement:
            self.estimate[0] = self.alpha * measurement[0] + (1 - self.alpha) * self.estimate[0]
            self.estimate[1] = self.alpha * measurement[1] + (1 - self.alpha) * self.estimate[1]
        return self.estimate
