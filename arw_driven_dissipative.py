import numpy as np
import matplotlib.pyplot as plt

## defining object to hold data for each index
## welcome to change - just ease of access/understanding rn
## default index object is awake with one particle
class index:
    def __init__(self, state = "A", numPar = 1):
        self.state = state
        self.numPar = numPar

    def __str__(self):
        return f"State: {self.state}, numPar = {self.numPar}"


## creates an array of length n
## with one particle at each index (already awake)
def setUp(n: int):
    arr = []
    for i in range(n):
        arr.append(index())

    return arr

def runRound(arr, addIndex, lenArr, rate):
    topple = True
    numTopples = 0
    
    ## generate batch of instructions for speed
    instr = np.random.choice(np.arange(-1,2), size = 100*lenArr, p = [(1)/(2*(1+rate)), (rate)/(1+rate), (1)/(2*(1+rate))]).tolist()

    ## add 1 particle to de-stabilize, and set index to active
    arr[addIndex].numPar += 1
    arr[addIndex].state = "A"

    while topple:
        roundTopples = 0
        for i in range(lenArr):
            currIndex = arr[i]
            if currIndex.state == "A" and currIndex.numPar > 0:
                if len(instr) < 1: ## if instruction list was empty, replenish, then grab instruction for index
                    instr = np.random.choice(np.arange(-1,2), size = 100*lenArr, p = [(1)/(2*(1+rate)), (rate)/(1+rate), (1)/(2*(1+rate))]).tolist()
                
                currInstr = instr.pop() ## generate instruction for current index


                if currInstr == 0 and currIndex.numPar == 1:
                    currIndex.state = "S"
                    numTopples += 1
                    roundTopples += 1
                elif currInstr == -1 or currInstr == 1: ## left or right
                    currIndex.numPar -= 1
                    currIndex.state = "S" if currIndex.numPar < 1 else "A"

                    ## check to make sure particle is added to index in range of arr
                    if (i + currInstr) < (lenArr) and (i + currInstr) >= 0:
                        arr[i + currInstr].numPar += 1
                        arr[i + currInstr].state = "A"
                        
                    numTopples += 1
                    roundTopples += 1

            topple = True if roundTopples > 0 else False ## topple is false if no indices needed to be stabilized

    
    ## now stabilization is complete - exits after one round of no need for stabilizing
    ## ie. all indices were stable in the pass through
    numPar = sum([obj.numPar for obj in arr])
    print(f"Average density: {numPar / lenArr}")
    return (numPar / lenArr), numTopples



if __name__ == "__main__":
    ntrials = 100
    nparticles = 100
    lambda_rate = 0.5
    
    arr = setUp(nparticles)

    avgDens = []
    numTopples = []
    for i in range(ntrials):
        density, topples = runRound(arr, int(len(arr) / 2), len(arr), lambda_rate)
        avgDens.append(density)
        numTopples.append(topples)


    plt.plot(np.array(range(len(avgDens))), np.array(avgDens))
    plt.plot(np.array(range(len(avgDens))), np.array(np.repeat(np.mean(np.array(avgDens), axis = 0), len(avgDens))), color = "hotpink")
    plt.ylim(0.6, 0.9)
    plt.xlabel("Number of Rounds (Trials)")
    plt.ylabel(f"Average Density (# of Particles / Length of Array ({len(arr)}))")
    plt.suptitle("Particle Density of Driven-Dissipative ARW Model")
    plt.title(f"Average density: {np.round(np.mean(np.array(avgDens), axis = 0), 3)}", size = 10)
    plt.legend(["Density per Round", "Average After All Rounds"], loc="lower right")
    plt.savefig(f"Plots/Average_density_{ntrials}_trials_{nparticles}_particles.png")

    plt.plot(np.array(range(len(numTopples))), np.array(numTopples))
    plt.xlabel("Number of Rounds (Trials)")
    plt.ylabel(f"Number of Topples to Stabilization ({len(arr)}))")
    plt.title("Number of Topples to Stabilization of Driven-Dissipative ARW Model")
    plt.savefig(f"Plots/Number_of_Topples_{ntrials}_trials_{nparticles}_particles.png")
    print(f"Average density: {np.mean(np.array(avgDens), axis = 0)}")





