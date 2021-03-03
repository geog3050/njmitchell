import csv

def hawkid():
    return(["Nathan Mitchell", "njmitchell"])

def import_data():
    participants = []
    with open('test_input.csv') as filename:
        myCSVreader = csv.reader(filename)
        for row in myCSVreader:
            participants.append(row)
            
    return participants

def attack_multiplier(attacker_type, defender_type):
    if attacker_type=="Water" and defender_type=="Fire":
        return 2.5
    elif attacker_type=="Fire" and defender_type=="Grass":
        return 3.0
    elif attacker_type=="Grass" and defender_type=="Water":
        return 1.5
    elif attacker_type=="Ground" and defender_type=="Electric":
        return 2
    elif attacker_type=="Electric" and defender_type=="Water":
        return 1.3
    return 1.0

def fight(participant1, participant2, first2attack):
    rounds = 0
    hp1 = int(participant1[2])
    hp2 = int(participant2[2])
    while hp1 and hp2 > 0:
        if first2attack==1:
            hp2=hp2-(int(participant1[3])*(attack_multiplier(participant1[1],participant2[1])))
            first2attack=2
            rounds=rounds+1
        elif first2attack==2:
            hp1=hp1-(int(participant2[3])*(attack_multiplier(participant2[1],participant1[1])))
            first2attack=1
            rounds=rounds+1
    if hp1>0:
        winner = 1
    else:
        winner= 2
    return [winner,rounds]

def tournament(participants):
    wins=[]
    for l in range(len(participants)): 
        wins.append(0)
    for i in participants:
        for j in participants:
            if i==j:
                continue
            else:
                r1=fight(i,j,1)
                r2=fight(i,j,2)
                if r1[0]==1:
                    wins[participants.index(i)]= wins[participants.index(i)]+1
                elif r1[0]==2:
                    wins[participants.index(j)]= wins[participants.index(j)]+1
                if r2[0]==1:
                    wins[participants.index(i)]= wins[participants.index(i)]+1
                elif r2[0]==2:
                    wins[participants.index(j)]= wins[participants.index(j)]+1 
    return wins