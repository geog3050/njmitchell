def thermMovement(climString,tempList):
    threshold = 0
    if climString=="Tropical":
        threshold=30
    elif climString=="Contintental":
        threshold=25
    else:
        threshold=18
    for i in tempList:
        if i<= threshold:
            print ("F")
        else:
            print ("U")
