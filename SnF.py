#A program implementing and measuring a Wa-Tor Simulation (outputs to a "temp" folder)

from matplotlib.pyplot import * #Library needed to plot results
from numpy import * #Library needed for some numerical functions
from random import * #Library needed to generate random numbers for movement
import sys, glob, shutil, os #Libraries needed to read/write files/folders and other system operations
from pathlib import Path #Library to determine the file paths to images
import imageio as io #Library for converting a collection of image files to a gif

#Main parameters of the simulation
breed_time = 3 #Number of steps before a fish is capable of duplicating
energy_gain = 1 #Additional steps granted to a shark after eating a fish
breed_energy = 20 #Number of stored steps before a shark is capable of duplicating

#Other simulation parameters
dims = [50,50] #Size of the simulation window
initial_fish = 400
initial_sharks = 400
steps = 500 #Time duration of the simulation
basicSetup = True #A random initial distribution (or not)

#Create a temporary folder for images if one doesn't exist; clear the folder if it does
subdir = 'temp'
if os.path.isdir(subdir):
    shutil.rmtree(subdir)
os.mkdir(subdir)
os.chdir(subdir) #Move into the temporary folder

#Function to determine available empty spaces to move into
def removeoccupied(locs):
    rlocs = []
    for k in range(0, 4, 1):
        if locs[k][1] == 0:
            rlocs.append(locs[k][0])
    return rlocs
  
#Function to determine if there are adjacent fish that a shark can feed on
def findfishoccupied(locs):
    rlocs = []
    for k in range(0, 4, 1):
        if locs[k][1] > 0:
            rlocs.append(locs[k][0])
    return rlocs

#Function to determine the common elements in two lists
def nestintersection(list1, list2):
    return list(map(list, set(map(tuple, list1)) & set(map(tuple, list2))))
  
#Function to combine all elements in two lists (with no repeats)
def nestunion(list1, list2):
    return list(map(list, set(map(tuple, list1)) | set(map(tuple, list2))))

#Main function of the simulation, updates the game array including all movements, hunts, breedings, and deaths
def stepgame(old_array):
    new_array = zeros((dims[0],dims[1]), dtype=int) #Creates the next game array
    for i in range(0, dims[0], 1): #Cycle over all entries in the previous game array
        for j in range(0, dims[1], 1):
            if 0 < old_array[i][j]: #Check if a fish occupies the space
                if breed_time < old_array[i][j]: #Check if the fish is elligible to breed
                    oldlocs = removeoccupied([[[i,(j+1)%dims[1]],old_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],old_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],old_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],old_array[(i-1)%dims[0]][j]]])
                    newlocs = removeoccupied([[[i,(j+1)%dims[1]],new_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],new_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],new_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],new_array[(i-1)%dims[0]][j]]])
                    availlocs = nestintersection(oldlocs, newlocs) #Determines which adjacent spaces are free in both arrays
                    if len(availlocs) != 0: #Check if there are any options
                        chosenloc = availlocs[randint(0, len(availlocs)-1)] #Randomly choose one of the options
                        new_array[chosenloc[0]][chosenloc[1]] = 1 #Place a new fish in that location
                        new_array[i][j] = 1 #Reset the fish that just bred
                    else: #If there are no options, the fish does not breed
                        new_array[i][j] = old_array[i][j] #The fish moves to the new game array without resetting
                else: #Implement fish moving
                    oldlocs = removeoccupied([[[i,(j+1)%dims[1]],old_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],old_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],old_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],old_array[(i-1)%dims[0]][j]]])
                    newlocs = removeoccupied([[[i,(j+1)%dims[1]],new_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],new_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],new_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],new_array[(i-1)%dims[0]][j]]])
                    availlocs = nestintersection(oldlocs, newlocs) #Determines which adjacent spaces are free in both arrays (i.e. actually empty)
                    if len(availlocs) != 0: #Check if there are any options
                        chosenloc = availlocs[randint(0, len(availlocs)-1)] #Randomly choose one of the options
                        new_array[chosenloc[0]][chosenloc[1]] = old_array[i][j] + 1 #The fish moves to the new game array with an increment to its breeding timer
                    else: #If there are no options, the fish does not move
                        new_array[i][j] = old_array[i][j] + 1 #The fish moves to the new game array with an increment to its breeding timer
                        old_array[i][j] = 0 #Removes the fish from the previous game array (so that it doesn't move/breed twice)
            elif 0 > old_array[i][j]: #Check if a shark occupies the space
                if -breed_energy > old_array[i][j]: #Check if the shark is elligible to breed
                    oldlocs = removeoccupied([[[i,(j+1)%dims[1]],old_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],old_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],old_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],old_array[(i-1)%dims[0]][j]]])
                    newlocs = removeoccupied([[[i,(j+1)%dims[1]],new_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],new_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],new_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],new_array[(i-1)%dims[0]][j]]])
                    availlocs = nestintersection(oldlocs, newlocs) #Determines which adjacent spaces are free in both arrays (i.e. actually empty)
                    if len(availlocs) != 0: #Check if there are any options
                        chosenloc = availlocs[randint(0, len(availlocs)-1)] #Randomly choose one of the locations
                        new_array[chosenloc[0]][chosenloc[1]] = floor(old_array[i][j]/2) #Add both sharks to the new array, sharing the energy between them
                        new_array[i][j] = floor(old_array[i][j]/2)
                    else: #If there are no options, the shark does not breed
                        new_array[i][j] = old_array[i][j] + 1 #The shark moves to the new game array with one less energy (or dies)
                else: #Implement shark hunting
                    oldlocs = findfishoccupied([[[i,(j+1)%dims[1]],old_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],old_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],old_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],old_array[(i-1)%dims[0]][j]]])
                    newlocs = findfishoccupied([[[i,(j+1)%dims[1]],new_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],new_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],new_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],new_array[(i-1)%dims[0]][j]]])
                    availlocs = nestunion(oldlocs, newlocs) #Find all nearby fish locations in either game array (whether they've been updated or not)
                    if len(availlocs) != 0: #Check if there are any options
                        chosenloc = availlocs[randint(0, len(availlocs)-1)] #Choose one of the adjacent fish randomly
                        if old_array[chosenloc[0]][chosenloc[1]] > 0: #Implement shark eating a fish that hasn't yet updated
                            new_array[chosenloc[0]][chosenloc[1]] = old_array[i][j] - energy_gain #Moves the shark to the new game array with an increase in energy
                            old_array[chosenloc[0]][chosenloc[1]] = 0 #Removes the dead fish
                        else: #Implement shark eating a fish that has already updated
                            new_array[chosenloc[0]][chosenloc[1]] = old_array[i][j] - energy_gain #Moves the shark to the new game array with an increase in energy (automatically removes the dead fish)
                    else: #Implement shark moving
                        oldlocs = removeoccupied([[[i,(j+1)%dims[1]],old_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],old_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],old_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],old_array[(i-1)%dims[0]][j]]])
                        newlocs = removeoccupied([[[i,(j+1)%dims[1]],new_array[i][(j+1)%dims[1]]],[[(i+1)%dims[0],j],new_array[(i+1)%dims[0]][j]],[[i,(j-1)%dims[1]],new_array[i][(j-1)%dims[1]]],[[(i-1)%dims[0],j],new_array[(i-1)%dims[0]][j]]])
                        availlocs = nestintersection(oldlocs, newlocs) #Determines which adjacent spaces are free in both arrays (i.e. actually empty)
                        if len(availlocs) != 0: #Check if there are any options
                            chosenloc = availlocs[randint(0, len(availlocs)-1)] #Randomly choose one of the options
                            new_array[chosenloc[0]][chosenloc[1]] = old_array[i][j] + 1 #The shark moves to the new game array with one less energy (or dies)
                        else: #If the shark can't move, it stays in place
                            new_array[i][j] = old_array[i][j] + 1 #The shark moves to the new game array with one less energy (or dies)
                old_array[i][j] = 0 #Removes the shark from the old game array (so that it doesn't eat/move/breed twice)
    return new_array #Outputs the updated game array

#Function that counts the total number of fish and sharks in the game array
def countsNf(game_array):
    fish_count = 0
    shark_count = 0
    for i in range(0, dims[0], 1):
        for j in range(0, dims[1], 1):
            if game_array[i][j] > 0:
                fish_count += 1
            if game_array[i][j] < 0:
                shark_count += 1
    return [shark_count, fish_count]
  
#Function to convert the game array into a format for visual display
def createimgarray(game_array):
    img_array = zeros((dims[0], dims[1]), dtype=int)
    for i in range(0, dims[0], 1):
        for j in range(0, dims[1], 1):
            if game_array[i][j] > 0:
                img_array[i][j] = 1
            if game_array[i][j] < 0:
                img_array[i][j] = -1
    return img_array

game_array = zeros((dims[0],dims[1]), dtype=int) #Initialize the game array

if basicSetup == True: #The basic set-up with random placement of new fish and sharks
    for k in range(0, initial_fish, 1): #Randomly populate the game array with new initial fish
        i = randint(0, dims[0]-1)
        j = randint(0, dims[1]-1)
        while game_array[i][j] != 0:
            i = randint(0, dims[0]-1)
            j = randint(0, dims[1]-1)
        game_array[i][j] = 1
    for k in range(0, initial_sharks, 1): #Randomly populate the game array with new initial sharks
        i = randint(0, dims[0]-1)
        j = randint(0, dims[1]-1)
        while game_array[i][j] != 0:
            i = randint(0, dims[0]-1)
            j = randint(0, dims[1]-1)
        game_array[i][j] = -energy_gain
else: #A more involved set-up, where the sharks and fish start grouped together with random energy/time
    for i in range(0, dims[0], 1): #Cycle over all entries in the previous game array
        for j in range(0, dims[1], 1):
            if (i-dims[0]/2)**2 + (j-dims[1]/2)**2 < initial_sharks/pi: #Populate a central disk of sharks with random energy
                game_array[i][j] = randint(-breed_energy,-1)
            elif (i-dims[0]/2)**2 + (j-dims[1]/2)**2 < (initial_sharks + initial_fish)/pi: #Populate a ring of fish surrounding the sharks with random time
                game_array[i][j] = randint(1,breed_time)

img_array = createimgarray(game_array)
arrayfig = figure(frameon=False)
ax = arrayfig.subplots()
ax.set_axis_off()
img = ax.imshow(img_array, cmap='bwr')
savefig('tmp_0000.png')
fishes = [initial_fish] #Initialize the list to store fish data
sharks = [initial_sharks] #Initialize the list to store the shark data
print("Playing game...")
prcnt = 0
k = 1
actual_steps = steps
while k <= steps:
    game_array = stepgame(game_array) #Update the game array
    currcount = countsNf(game_array) #Counts the number of fish and sharks
    fishes.append(currcount[1]) #Store the number data
    sharks.append(currcount[0])
    img_array = createimgarray(game_array) #Create a version of the game array that's easier to plot
    img.set_data(img_array) #Draw the plot of the new game array
    savefig('tmp%04d.png' % k) #Save the new plot to the temporary folder
    if floor(k*100/steps) > prcnt: #Output the progress of the simulation
        ppstr = str(prcnt) + '%'
        sys.stdout.write('%s\r' % ppstr)
        sys.stdout.flush()
        prcnt += 1
    if 0 < currcount[0] + currcount[1] < dims[0] * dims[1]: #Check if the species have not gone extinct and the array isn't full
        k += 1
    else:
        print('Early termination!')
        actual_steps = k
        k = steps + 1
    
sys.stdout.write('%s\r' % '100%') #Output that the game updates have completed
sys.stdout.flush()

print('Reading image files...')

filename = 'SnFanimation_'+str(dims[1])+'x'+str(dims[0])+'_('+str(breed_time)+','+str(energy_gain)+','+str(breed_energy)+')_('+str(initial_sharks)+','+str(initial_fish)+')_'+str(actual_steps)+'.gif' #File name for the output gif file, includes relevant simulation parameters
mypath = Path(__file__).parent.absolute() #File path to the temporary image folder
imgnames = glob.glob('tmp*.png') #Generate a list of all image names in the temporary image folder
imgPaths = []

for imgname in imgnames: #Convert the list of image names to a list of file paths to the images
    imgPaths.append(str(mypath/imgname))

imgPaths.sort() #Sort the images into chronological order
totaldata = []

for imgpath in imgPaths: #Read in all the image data
    currdata = io.imread(imgpath)
    totaldata.append(currdata)
    
print('Writing gif file...')
    
io.mimwrite(filename, totaldata, format= '.gif', fps = 20) #Convert all the images into a gif

for imgname in imgnames: #Remove all the png image files after the gif is created
    os.remove(imgname)

#Create and save plots of the number results
fig, axs = subplots(2)
fig.suptitle('Wa-Tor Populations')
axs[0].plot(range(0, actual_steps+1, 1), fishes, label='fish')
axs[0].plot(range(0, actual_steps+1, 1), sharks, label='sharks')
axs[0].legend()
axs[0].set(xlabel="", ylabel="Population")
axs[1].plot(take(fishes, range(0, actual_steps+1, 1)), take(sharks, range(0, actual_steps+1, 1)), marker='.')
axs[1].set(xlabel="Fish Population", ylabel="Shark Population")
savefig('SnFplots_'+str(dims[1])+'x'+str(dims[0])+'_('+str(breed_time)+','+str(energy_gain)+','+str(breed_energy)+')_('+str(initial_sharks)+','+str(initial_fish)+')_'+str(actual_steps)+'.png')

print('Complete!')
print('Output files will be deleted upon next run,')
print('be sure to move them out of the temp folder!')

os.chdir(os.pardir) #Move back out of the temporary folder
