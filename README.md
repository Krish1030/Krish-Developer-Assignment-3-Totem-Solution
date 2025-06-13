# Real-Time Median Tracker with Outlier Detection and Correction

This project provides a Python-based implementation for tracking the median of a stream of integers fetched from an API. It includes automatic outlier detection using standard deviation and correction using a moving average strategy.

---

## 📌 Features

- Calculates real-time median from a stream of integers
- Detects outliers using 3-sigma rule (3 × standard deviation)
- Corrects outliers using the moving average of previous values
- Visualizes original, corrected, and median values using Matplotlib
- Fetches streaming data from a custom API endpoint

---

## 🧠 How It Works

1. **Heaps for Median Tracking**:  
   - Max-heap for the left half
   - Min-heap for the right half  
   These heaps are balanced to maintain the median in O(log n) time.

2. **Outlier Detection**:  
   A data point is considered an outlier if:
