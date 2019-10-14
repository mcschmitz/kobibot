from IPython.display import clear_output
from keras.callbacks import Callback
from matplotlib import pyplot as plt


class PlotLearning(Callback):
    def __init__(self, path):
        super(PlotLearning, self).__init__()
        if path:
            plt.ioff()
            self.path = path
        self.i = 0
        self.x = []
        self.metrics = {}
        self.val_metrics = {}
        self.fig = None
        self.logs = []

    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.metrics = {m: [] for m in self.model.metrics_names}
        self.val_metrics = {m: [] for m in self.model.metrics_names}
        self.fig = plt.figure()
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        for metric in self.model.metrics_names:
            self.metrics[metric].append(logs.get(metric))
            self.val_metrics[metric].append(logs.get('val_' + metric))
        self.i += 1

        f, ax = plt.subplots(1, len(self.model.metrics_names), sharex=True, figsize=(16, 6))

        clear_output(wait=True)

        for idx, metric in enumerate(self.model.metrics_names):
            ax[idx].plot(self.x, self.metrics[metric], label=metric)
            ax[idx].plot(self.x, self.val_metrics[metric], label="validation " + metric)
            ax[idx].legend()
        if self.path:
            plt.savefig(self.path)
        else:
            plt.show()
        plt.close()
