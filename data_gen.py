import json
import numpy as np
import pprint
import math

def calculate_rank(vector):
	  a={}
	  rank=5
	  for num in sorted(vector):
	    if num not in a:
	      a[num]=rank
	      rank=rank-1
	  return[a[i] for i in vector]

globalContestantsList = { 
		"data" : []
	}

for i in range(9):
	filename = "s" + str(i+1) + ".json"
	with open (filename) as f:
		data = json.load(f)

	# first - iterate through the episodes and start creating episodic sums (in another object)
	# does python have objects? Hmmmm.... they have dictionaries - whatever that means
	# second - once the iteration is done, for each episodes sum, assign a winner flag
	# finally - sum all the score for each user and find winner (this can be done at or before step two)
	# we're looking at a massive fuckin object:
	# episode
	#  contestantID 
	#  
	#  contestantSum
	#  contestantRank
	#  seasonrank

	# eventually flatten it out:
	# for each contestant, get tasks score, episode rank, season rank, prizeTaskRank, liveTaskRank, outcome (winner or looser)


	### setting up initial variables and structures

	episodeDict = [
		{
				"episodeID" : 1,
				"contestantScores" : [0,0,0,0,0],
				"contestantRanks": [1,2,3,4,5],
				"prizeTaskRank": [1,2,3,4,5],
				"liveTaskRank": [1,2,3,4,5]
		}
	]
			


	contestant = [ ## for each contestant
		{
			"outcome": "winner" 
		},{
			"outcome": "winner" 
		},{
			"outcome": "winner" 
		},{
			"outcome": "winner" 
		},{
			"outcome": "winner" 
		},
	]

	seasonScore = [0,0,0,0,0]
	seasonRank = [0,0,0,0,0]

	contestantLiveTaskAverage = [ 0, 0, 0, 0, 0]
	contestantPrizeTaskAverage = [ 0, 0, 0, 0, 0]

	def calculate_rank(vector):
	  a={}
	  rank=5
	  for num in sorted(vector):
	    if num not in a:
	      a[num]=rank
	      rank=rank-1
	  return[a[i] for i in vector]
	## json file structure:
	# episode : { task : results per contestant}
	episodeCount = 0

	for index, ep in enumerate(data, start = 1):
		## {'TASK': '1-P', 'Frank': 4, 'Josh': 1, 'Roisin': 2, 'Romesh': 3, 'Tim': 5}
		iter = list(ep.values())
		epId = int(iter[0].split("-")[0])
		taskId = iter[0].split("-")[1]
		cscore_1 = iter[1]
		cscore_2 = iter[2]
		cscore_3 = iter[3]
		cscore_4 = iter[4]
		cscore_5 = iter[5]
		
		## now comes the episodeDict update:
		##episodeDict[epId -1]["contestantScores"] = np.add([cscore_1, cscore_2,cscore_3,cscore_4,cscore_5],episodeDict[epId -1]["contestantScores"])

		## we'll have to run a try to see if episode object exists in list:
		try:
			#print(iter[0])
			episodeDict[epId -1]["contestantScores"] = np.add([cscore_1, cscore_2,cscore_3,cscore_4,cscore_5],episodeDict[epId -1]["contestantScores"])
			seasonScore = np.add([cscore_1, cscore_2,cscore_3,cscore_4,cscore_5], seasonScore)
			if taskId == "L":  ## live task
				episodeDict[epId -1]["liveTaskRank"] = [cscore_1, cscore_2,cscore_3,cscore_4,cscore_5]
			elif taskId == "P":  ## prize task
				episodeDict[epId -1]["prizeTaskRank"] = [cscore_1, cscore_2,cscore_3,cscore_4,cscore_5]
		except Exception as e: 
			## we're in a new episode... we should run the scoring for the previous episode first
			## processing the previous epside:
			episodeDict[epId -2]["contestantRanks"] = calculate_rank(episodeDict[epId -2]["contestantScores"])
			episodeDict[epId -2]["liveTaskRank"] = calculate_rank(episodeDict[epId -2]["liveTaskRank"])
			episodeDict[epId -2]["prizeTaskRank"] = calculate_rank(episodeDict[epId -2]["prizeTaskRank"])

			for index, i in enumerate(episodeDict[epId -2]["prizeTaskRank"]):
				contestantPrizeTaskAverage[index] += i
			for index, i in enumerate(episodeDict[epId -2]["liveTaskRank"]):
				contestantLiveTaskAverage[index] += i	
			
			## for the contestant array - we've hit the end of an episode - time to add the episode score:
			episodeScoreName = "episode" + str(epId-1) + "Result"
			contestant[0][episodeScoreName] = episodeDict[epId -2]["contestantRanks"][0]
			contestant[1][episodeScoreName] = episodeDict[epId -2]["contestantRanks"][1]
			contestant[2][episodeScoreName] = episodeDict[epId -2]["contestantRanks"][2]
			contestant[3][episodeScoreName] = episodeDict[epId -2]["contestantRanks"][3]
			contestant[4][episodeScoreName] = episodeDict[epId -2]["contestantRanks"][4]


			## new episode starts:
			episodeDict.append( {
					"episodeID" : epId,
					"contestantScores" : [0,0,0,0,0],
					"contestantRanks": [1,2,3,4,5],
					"prizeTaskRank": [1,2,3,4,5],
					"liveTaskRank": [1,2,3,4,5]
					})
			
			episodeDict[epId -1]["contestantScores"] = [cscore_1, cscore_2,cscore_3,cscore_4,cscore_5]
			seasonScore = np.add([cscore_1, cscore_2,cscore_3,cscore_4,cscore_5], seasonScore)
			episodeDict[epId -1]["prizeTaskRank"] = [cscore_1, cscore_2,cscore_3,cscore_4,cscore_5]

		# if we've reached the last task of the season:
		
		if index == len(data):
			episodeDict[epId -1]["contestantRanks"] = calculate_rank(episodeDict[epId -1]["contestantScores"])
			episodeDict[epId -1]["liveTaskRank"] = calculate_rank(episodeDict[epId -1]["liveTaskRank"])
			episodeDict[epId -1]["prizeTaskRank"] = calculate_rank(episodeDict[epId -1]["prizeTaskRank"])

			### update the last season task:
			episodeScoreName = "episode" + str(epId) + "Result"
			contestant[0][episodeScoreName] = episodeDict[epId -1]["contestantRanks"][0]
			contestant[1][episodeScoreName] = episodeDict[epId -1]["contestantRanks"][1]
			contestant[2][episodeScoreName] = episodeDict[epId -1]["contestantRanks"][2]
			contestant[3][episodeScoreName] = episodeDict[epId -1]["contestantRanks"][3]
			contestant[4][episodeScoreName] = episodeDict[epId -1]["contestantRanks"][4]


		## using the same iteration, we'll build our contestant list

		contestant[0][iter[0]]	= iter[1]
		contestant[1][iter[0]]	= iter[2]
		contestant[2][iter[0]]	= iter[3]
		contestant[3][iter[0]]	= iter[4]
		contestant[4][iter[0]]	= iter[5]
		
		## for future use:
		episodeCount = epId

	#pprint.pprint(contestantLiveTaskAverage)
	seasonRank = calculate_rank(seasonScore)

	## calculate the average rank for both live & prize tasks:
	for index, i in enumerate(contestantPrizeTaskAverage):
		contestant[index]["prizeTaskAverageScore"] = math.ceil(i/episodeCount)
		contestant[index]["liveTaskAverageScore"] = math.ceil(contestantLiveTaskAverage[index]/episodeCount)
		contestant[index]["seasonRank"] = seasonRank[index] 
		contestant[index]["outcome"] = "Winner" if contestant[index]["seasonRank"] == 1  else "Looser"
	#pprint.pprint(contestant)
	globalContestantsList["data"] += (contestant)

with open("finalData.json", "w") as wFile:
	wFile.write(json.dumps(globalContestantsList))