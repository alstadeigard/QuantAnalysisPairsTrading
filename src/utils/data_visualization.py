import matplotlib.pyplot as plt

def plot_data(data, title, y_label):
    data.plot(figsize=(12,6))
    plt.title(title)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()
