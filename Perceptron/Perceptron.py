import numpy as np

class MyPerceptron ():

    def __init__(self):

        self.x = ([0,0,1],[0,1,0],[1,0,0],
             [1,1,0],[0,1,1],[1,0,1],
             [0,0,0],[1,1,1])

        self.weights = [0.4, 0.6, 0.5]

        self.lr = 0.1

        self.bias = 0

        self.actual_class = [1, -1, -1,
                            -1, 1, -1,
                            -1, -1]

    def step(self, weighted_sum):
        if weighted_sum > self.bias:
            return 1
        else:
            return -1

    def perceptron(self, x_input):
        weighted_sum = 0
        for x_i,w, in zip(x_input, self.weights):
            weighted_sum += x_i*w
        return self.step(weighted_sum)

    def rebalance_weights(self, prediction, target, x_input):
        rw = list()
        for i in range(0, len(self.weights)):
            new_weight = self.weights[i] + self.lr * (target - prediction) * x_input[i]
            rw.append(new_weight)
        return rw

    def main(self):

        for i in range(0, len(instance.x)):
            print("%d. "%i + str(instance.x[i]) + " prediction: " + f"{str(instance.perceptron(instance.x[i])):>3}" + "  actual: " + f"{str(instance.actual_class[i]):>3}" +
                  f"{(' true  ' if instance.perceptron(instance.x[i]) == instance.actual_class[i] else ' false '):>3}" + f"{str(instance.weights):>10}")

        for i in range(0, 100):
            for i in range(0, len(instance.x)):
                if instance.perceptron(instance.x[i]) is not instance.actual_class[i]:
                    instance.weights = instance.rebalance_weights(instance.perceptron(instance.x[i]), instance.actual_class[i], instance.x[i])

        print("--------------------------------------------------------------------------------------")

        for i in range(0, len(instance.x)):
            print("%d. "%i + str(instance.x[i]) + " prediction: " + f"{str(instance.perceptron(instance.x[i])):>3}" + "  actual: " + f"{str(instance.actual_class[i]):>3}" +
                  f"{(' true  ' if instance.perceptron(instance.x[i]) == instance.actual_class[i] else ' false '):>3}" + f"{str(instance.weights):>10}")

instance = MyPerceptron()
instance.main()
