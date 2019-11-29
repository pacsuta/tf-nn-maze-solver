import tensorflow as tf
import maze
import maze_collection as mc
import random as r
import numpy as np
import matplotlib.pyplot as plt


def main(output_file_name):
    # housekeeping
    m = maze.Maze(mc.simple_maze)
    sess = tf.Session()
    learning_rate = 0.0001
    num_memory_units = 0
    graphical = True
    file_output = True

    if file_output is True:
        # output to file (this is set to overwrite!)
        file = open(output_file_name + ".txt", "w")
        file.write("Iter\tWon?\tSteps\tAll steps\n")

    # neural network structure
    x = tf.placeholder(tf.float32, [None, 2+num_memory_units])

    W1 = tf.Variable(tf.truncated_normal([2+num_memory_units, 6]))
    b1 = tf.Variable(tf.truncated_normal([1, 6]))

    h1 = tf.sigmoid(tf.matmul(x, W1) + b1)

    W2 = tf.Variable(tf.truncated_normal([6, 6]))
    b2 = tf.Variable(tf.truncated_normal([1, 6]))

    h2 = tf.sigmoid(tf.matmul(h1, W2) + b2)

    W3 = tf.Variable(tf.truncated_normal([6, 4+num_memory_units]))
    b3 = tf.Variable(tf.truncated_normal([1, 4+num_memory_units]))

    output_final_layer_before_activation_function = tf.matmul(h2, W3) + b3
    left_output = output_final_layer_before_activation_function[:, 0:4]
    right_output = output_final_layer_before_activation_function[:, 4:]
    y = tf.nn.softmax(left_output)
    memory_units = tf.sigmoid(right_output)

    sess.run(tf.global_variables_initializer())

    weights_list = [W1, b1, W2, b2, W3, b3]

    # gradients (i.e. dp/dw) for backpropagation
    dprobability0_dweights = tf.gradients(y[:, 0], weights_list)
    dprobability1_dweights = tf.gradients(y[:, 1], weights_list)
    dprobability2_dweights = tf.gradients(y[:, 2], weights_list)
    dprobability3_dweights = tf.gradients(y[:, 3], weights_list)

    # weight update operation
    ph_delta_weights_list = [tf.placeholder(tf.float32, w.get_shape()) for w in weights_list]
    update_weights = [tf.assign(weights_list[i], weights_list[i] + ph_delta_weights_list[i])
                      for i in range(len(weights_list))]

    # training setup
    maxSteps = 4
    iteration = 0
    maxIterations = 10000

    steps_taken = np.zeros(maxIterations)

    # Plot display -----------------------------------------------------------------------------------------------------
    if graphical is True:
        spread = 50

        plt.ion()
        fig = plt.figure("Maze solver")
        ax = fig.add_subplot(111)
        ax.axis([0, maxIterations/spread + 1, 0, maxSteps + 1])
        plt.ylabel("Steps taken")
        plt.xlabel("Iterations ({})".format(spread))
        ax.plot([0], [0])
        ax.grid()

        iterations = []
        duration_history = []

    # Looping through iterations
    while iteration < maxIterations:
        # Current step
        step = 0

        # All outputs and dp_dthetas for this iteration
        probabilities = np.zeros(maxSteps)
        dp_dthetas = list()

        memory = np.zeros(num_memory_units)

        movements = ""

        while m.won is False and step < maxSteps:
            # Defining neural network input
            input_values = np.array([m.normal_x(), m.normal_y()])
            input_values = np.append(input_values, memory)

            # Running input through the neural network
            [output, dp0dtheta, dp1dtheta, dp2dtheta, dp3dtheta, output_memory] =\
                sess.run([y, dprobability0_dweights, dprobability1_dweights, dprobability2_dweights,
                          dprobability3_dweights, memory_units],
                         feed_dict={x: [input_values]})

            # Random value between 0 and 1, inclusive on both sides
            result = r.uniform(0, 1)

            if result <= output[0][0]:
                # Up
                m.move_up()
                probabilities[step] = output[0][0]
                dp_dthetas.append(dp0dtheta)
                movements += "U"
            elif result <= output[0][0] + output[0][1]:
                # Right
                m.move_right()
                probabilities[step] = output[0][1]
                dp_dthetas.append(dp1dtheta)
                movements += "R"
            elif result <= output[0][0] + output[0][1] + output[0][2]:
                # Down
                m.move_down()
                probabilities[step] = output[0][2]
                dp_dthetas.append(dp2dtheta)
                movements += "D"
            elif result <= output[0][0] + output[0][1] + output[0][2] + output[0][3]:
                # Left
                m.move_left()
                probabilities[step] = output[0][3]
                dp_dthetas.append(dp3dtheta)
                movements += "L"

            memory = output_memory[0]
            step += 1

        print("Iteration #{:05d}\tWon: {}\tSteps taken: {:04d}\tSteps: {}".format(iteration, m.won,
                                                                                  step, movements))
        if file_output is True:
            file.write("{:05d}\t{}\t{:04d}\t{}\n".format(iteration, m.won, step, movements))

        # Assigning a reward
        # reward = maxSteps - (2 * step)  # linear reward function
        reward = maxSteps - pow(step, 2)  # power reward function

        # Applying weight change for every step taken, based on the reward given at the end
        for i in range(step):
            deltaTheta = [(learning_rate * (1 / probabilities[i]) * reward) * dp_dthetas[i][j]
                          for j in range(len(weights_list))]

            sess.run(update_weights, feed_dict=dict(zip(ph_delta_weights_list, deltaTheta)))

        steps_taken[iteration] = step
        if graphical is True and iteration % spread == 0:
            steps_mean = np.mean(steps_taken[iteration-spread:iteration+1])
            iterations = iterations+[iteration/spread]
            duration_history = duration_history+[steps_mean]
            del ax.lines[0]
            ax.plot(iterations, duration_history, 'b-', label='Traj1')
            plt.draw()
            plt.pause(0.001)

        m.reset()

        iteration += 1
    if file_output is True:
        file.close()
    if graphical is True:
        if file_output is True:
            plt.savefig(output_file_name + ".png")
        else:
            plt.show()
        #input("Press [enter] to continue.")
        plt.close()
    sess.close()


if __name__ == "__main__":
    for run in range(10, 15):
        number = "{:05d}".format(run)
        main("./output/one_step_fixed-no_memory/" + number)
