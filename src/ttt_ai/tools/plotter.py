import matplotlib.pyplot as plt

plt.ion()


def plot(scores, mean_scores):
    # display.clear_output(wait=True)
    # display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], "X: " + str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], "O: " + str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(0.05)
