import random
import time

def randomWalk(graph, graphFrequency, threshold):
    totalFre = 0
    selected_chain = []

    count = 0   # Count how many chains are generated in this repo
    start_time = time.time()   # Prevent infinite loop
    while totalFre < threshold and time.time() - start_time < 1:     
        # Missing a condition: when all possible chains are added but haven't exceeded the threshold yet 
        Fre = 0  # A buffer variable to store frequency
        # print(list(graph.items()))  # Uncomment to print items in the graph
        random_item = random.choice(list(graph.items()))[0]
        # Randomly select an item to start the chain
        
        newlist = []
        check = []
        newlist.append(random_item)
        check.append(random_item)
        Fre += graphFrequency[random_item] 
        
        while graph[random_item] and totalFre < threshold and time.time() - start_time < 1:
            # Construct a chain starting from this item until encountering an empty item or exceeding the threshold
            random_item = random.choice(graph[random_item])
            if random_item in check:
                break
            check.append(random_item)
            newlist.append(random_item)
            Fre += graphFrequency[random_item]

        if newlist not in selected_chain:
            # Add the chain only if it hasn't been added before
            selected_chain.append(newlist)
            totalFre += Fre
            # Add the frequency only if the chain is added
            count += 1   # Count total number of chains

    return selected_chain
