import heapq
import statistics
import requests
import matplotlib.pyplot as plt

class RealTimeMedianTracker:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []
        self.original_data = []
        self.corrected_data = []
        self.medians = []

    def add_number(self, num):
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)

        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def get_median(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2

    def process_stream(self, stream, window_size=3):
        for val in stream:
            self.original_data.append(val)

            median = self.get_median() if self.corrected_data else val
            std_dev = statistics.stdev(self.corrected_data) if len(self.corrected_data) >= 2 else 0
            threshold = 3 * std_dev

            if std_dev == 0 or abs(val - median) <= threshold:
                corrected_val = val
                reason = "Accepted"
            else:
                if len(self.corrected_data) >= window_size:
                    moving_avg = sum(self.corrected_data[-window_size:]) / window_size
                else:
                    moving_avg = median
                corrected_val = round(moving_avg)
                reason = f"Outlier corrected to {corrected_val}"

            self.corrected_data.append(corrected_val)
            self.add_number(corrected_val)
            self.medians.append(self.get_median())

            print(f"{reason}: {val} → Used: {corrected_val} | Median: {self.get_median():.2f} | Std Dev: {std_dev:.2f}")

    def plot(self):
        steps = list(range(len(self.original_data)))

        plt.figure(figsize=(12, 6))
        plt.plot(steps, self.original_data, label='Original Input', linestyle='--', marker='o', color='blue')
        plt.plot(steps, self.corrected_data, label='Corrected Data', linestyle='-', marker='s', color='orange')
        plt.plot(steps, self.medians, label='Median', linestyle='-', marker='^', color='green')

        plt.title("Real-time Median Tracker with Outlier Correction")
        plt.xlabel("Time Step")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def get_stream_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print("API error:", e)
        return []

if __name__ == '__main__':
    api_url = "http://127.0.0.1:5000/stream"  # Local API
    stream = get_stream_from_api(api_url)
    if stream:
        tracker = RealTimeMedianTracker()
        tracker.process_stream(stream)
        tracker.plot()
    else:
        print("No data received from the API.")



