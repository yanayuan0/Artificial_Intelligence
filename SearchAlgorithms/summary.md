# Comparing local search methods

You should use the coordinates `North_America_75.json` and do
multiple runs for each local search. Be sure to experiment with the
default parameter settings to try to get the best results you can.
Then run at least 3 experiments using each search method and compute
the average best cost found.

| HC     | Best Cost |
| ------ | --------- |
| run 1  |    342.58       |
| run 2  |    376.49       |
| run 3  |    354.68       |
| Avg    |    357.92       |

HC parameters: runs = 2, steps = 200, rand_move_prob = 0.01

| SA     | Best Cost |
| ------ | --------- |
| run 1  |   478.38        |
| run 2  |   466.69        |
| run 3  |   473.32        |
| Avg    |   485.33        |

SA parameters: runs = 5, steps = 5000, init_temp = 80, temo_decay = 0.999

| BS     | Best Cost |
| ------ | --------- |
| run 1  |   358.49        |
| run 2  |   359.70        |
| run 3  |   360.82        |
| Avg    |   359.67        |

BS parameters: pop_size = 30, steps = 600, max_neighbors = 40

| SBS    | Best Cost |
| ------ | --------- |
| run 1  |   285.08        |
| run 2  |   291.43        |
| run 3  |   283.92        |
| Avg    |   286.81        |

SBS parameters: pop_size = 50, steps = 600, init_temp = 100, temp_decay = 0.99, max_neighbors = 10


Which local search algorithm (HC, SA, BS, or SBS) most consistently finds
the best tours and why do you think it outperforms the others?


SBS most consistently finds the best tour and we think the reason it outperforms 
the others is because BS algorithms might stuck at a local maxima due to search for
the cheapest path, but SBS allowsd more randomnes for the search algorithm and that it could
escape from the local maxima and have more possibility of finding the global maxima. Compared to
HC and SA, which starts from one random start, SBS starts from multiple starts at the same time, 
and that it will be more likely to find the global maxima. 
