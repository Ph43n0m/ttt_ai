import matplotlib.pyplot as plt

plt.ion()


def plot(x_scores, o_scores):
    # display.clear_output(wait=True)
    # display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(x_scores)
    plt.plot(o_scores)
    plt.ylim(
        ymin=(
            min(o_scores[-1], x_scores[-1]) - 10
            if min(o_scores[-1], x_scores[-1]) < 0
            else 0
        )
    )
    plt.text(len(x_scores) - 1, x_scores[-1], "X: " + str(x_scores[-1]))
    plt.text(len(o_scores) - 1, o_scores[-1], "O: " + str(o_scores[-1]))
    plt.show(block=False)
    plt.pause(0.01)
