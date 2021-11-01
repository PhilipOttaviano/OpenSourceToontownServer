from direct.directnotify import DirectNotifyGlobal

from toontown.quest import Quests

from toontown.toon.DistributedNPCSpecialQuestGiverAI import DistributedNPCSpecialQuestGiverAI

QuestIdIndex = 0
QuestFromNpcIdIndex = 1
QuestToNpcIdIndex = 2
QuestRewardIdIndex = 3
QuestProgressIndex = 4

class QuestManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air

    def toonPlayedMinigame(self, toon, toons):
        # toons is never used. Sad!
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.TrolleyQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def recoverItems(self, toon, suitsKilled, zoneId):
        recovered, notRecovered = ([] for _ in xrange(2))
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                isComplete = quest.getCompletionStatus(toon, toon.quests[index])
                if isComplete == Quests.COMPLETE:
                    continue

                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.Any or quest.getHolderType() in ['type', 'track', 'level']:
                        for suit in suitsKilled:
                            if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                                break

                            if (quest.getHolder() == Quests.Any) or (
                                    quest.getHolderType() == 'type' and quest.getHolder() == suit['type']) or (
                                    quest.getHolderType() == 'track' and quest.getHolder() == suit['track']) or (
                                    quest.getHolderType() == 'level' and quest.getHolder() <= suit['level']):
                                # This seems to be how Disney did it.
                                progress = toon.quests[index][4] & pow(2, 16) - 1
                                completion = quest.testRecover(progress)
                                if completion[0]:
                                    # Recovered!
                                    recovered.append(quest.getItem())
                                    self.__incrementQuestProgress(toon.quests[index])
                                else:
                                    # Not recovered. Sad!
                                    notRecovered.append(quest.getItem())

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

        return recovered, notRecovered

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToons):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.CogQuest):
                for suit in suitsKilled:
                    for _ in xrange(quest.doesCogCount(toon.getDoId(), suit, zoneId, activeToons)):
                        self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonKilledCogdo(self, toon, difficulty, numFloors, zoneId, activeToons):
        pass

    def toonKilledBuilding(self, toon, track, difficulty, floors, zoneId, activeToons):
        # Thank you difficulty, very cool!
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.BuildingQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getBuildingTrack() == Quests.Any or quest.getBuildingTrack() == track:
                        if floors >= quest.getNumFloors():
                            for _ in xrange(quest.doesBuildingCount(toon.getDoId(), activeToons)):
                                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonDefeatedFactory(self, toon, factoryId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FactoryQuest):
                for _ in xrange(quest.doesFactoryCount(toon.getDoId(), factoryId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonRecoveredCogSuitPart(self, toon, zoneId, toonList):
        pass

    def toonDefeatedMint(self, toon, mintId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.MintQuest):
                for _ in xrange(quest.doesMintCount(toon.getDoId(), mintId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonDefeatedStage(self, toon, stageId, activeToonVictors):
        pass

    def hasTailorClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                return True

        return False

    def requestInteract(self, avId, npc):
        # Get the avatar.
        av=self.air.doId2do.get(avId)
        if not av:
            return

        history=av.getQuestHistory()
        avQuestPocketSize=av.getQuestCarryLimit()
        avQuests=av.getQuests()

        fakeTier=0

        avTrackProgress=av.getTrackProgress()

        # Iterate through their quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc=avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress=questDesc
            questClass=Quests.getQuest(questId)
            if questClass:
                completeStatus=questClass.getCompletionStatus(av, questDesc, npc)
            else:
                continue

            # If the quest is a DeliverGagQuest, add the gags.
            if isinstance(questClass, Quests.DeliverGagQuest):
                # Check if it's the required NPC.
                if npc.npcId == toNpcId:
                    track, level=questClass.getGagType()
                    currItems=av.inventory.numItem(track, level)
                    if currItems >= questClass.getNumGags():
                        av.inventory.setItem(track, level, av.inventory.numItem(track, level) - questClass.getNumGags())
                    else:
                        npc.rejectAvatar(avId)
                    av.b_setInventory(av.inventory.makeNetString())

            # If they've completed a quest.
            if completeStatus == Quests.COMPLETE:
                # ToonUp the toon to max health.
                av.toonUp(av.maxHp)

                # If it's a TrackChoiceQuest then present their track choices.
                if isinstance(questClass, Quests.TrackChoiceQuest):
                    npc.presentTrackChoice(avId, questId, [0, 1, 2, 3, 4, 5, 6])
                    break
                # If there is another part to this quest then give them that.
                if Quests.getNextQuest(questId, npc, av)[0] != Quests.NA:
                    self.nextQuest(av, npc, questId)
                    if int(avId) in self.air.tutorialManager.avId2fsm:
                        self.air.tutorialManager.avId2fsm[int(avId)].demand('Tunnel')
                    break
                else:
                    # The toon has completed this quest. Give them a reward!
                    npc.completeQuest(avId, questId, rewardId)
                    self.completeQuest(av, questId)
                break
        else:
            # They haven't completed any quests so we have to give them choices.
            # If they've got a full pouch then reject them.
            if (len(avQuests) == avQuestPocketSize * 5):
                npc.rejectAvatar(avId)
                return
            elif isinstance(npc, DistributedNPCSpecialQuestGiverAI):
                # Don't display choices. Force a choice.
                self.tutorialQuestChoice(avId, npc)
                return
            else:
                # Present quest choices.
                choices=self.avatarQuestChoice(av, npc)
                if choices != []:
                    for choice in choices:
                        questClass=Quests.QuestDict.get(choice[0])
                        for required in questClass[0]:
                            if required not in history:
                                if len(choices) == 1:
                                    choices=[]
                                else:
                                    if choice in choices:
                                        choices.remove(choice)
                            else:
                                continue
                    if choices != []:
                        npc.presentQuestChoice(avId, choices)
                    else:
                        npc.rejectAvatar(avId)
                else:
                    npc.rejectAvatar(avId)

    def __toonQuestsList2Quests(self, quests):
        return [Quests.getQuest(x[0]) for x in quests]

    def avatarCancelled(self, avId):
        pass

    def avatarQuestChoice(self, av, npc):
        # Get the best quests for an avatar/npc.
        return Quests.chooseBestQuests(npc, av)

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        self.npcGiveQuest(npc, av, questId, rewardId, toNpcId, storeReward=True)

    def npcGiveQuest(self, npc, av, questId, rewardId, toNpcId, storeReward=False):
        rewardId = Quests.transformReward(rewardId, av)
        finalReward = rewardId if storeReward else 0
        progress = 0
        av.addQuest((questId, npc.getDoId(), toNpcId, rewardId, progress), finalReward)
        npc.assignQuest(av.getDoId(), questId, rewardId, toNpcId)

    def __incrementQuestProgress(self, quest):
        quest[4] += 1

    def nextQuest(self, av, npc, questId):
        # Get the next QuestId and toNpcId.
        nextQuestId, toNpcId = Quests.getNextQuest(questId, npc, av)

        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]

            if questDesc[QuestIdIndex] == questId:
                questDesc[QuestIdIndex] = nextQuestId
                questDesc[QuestToNpcIdIndex] = toNpcId
                questDesc[QuestProgressIndex] = 0
            questList.append(questDesc)

        # Show the quest movie and set their quests.
        npc.incompleteQuest(av.doId, nextQuestId, Quests.QUEST, toNpcId)
        av.b_setQuests(questList)

    def completeQuest(self, toon, questId):
        toon.toonUp(toon.getMaxHp())
        toon.removeQuest(questId)

    def toonRodeTrolleyFirstTime(self, toon):
        # For this, we just call toonPlayedMinigame with the toon.
        # And for toons, we just pass in an empty list. Not like
        # it matters anyway, as that argument is never used.
        self.toonPlayedMinigame(toon, [])

    def removeClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = toon.quests[index]
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                toon.removeQuest(questId)
                return True

        return False

    def giveReward(self, toon, rewardId):
        reward = Quests.getReward(rewardId)
        if reward:
            reward.sendRewardAI(toon)

    def toonMadeFriend(self, toon, otherToon):
        # This is so sad, can we leave otherToon unused?
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FriendQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonFished(self, toon, zoneId):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                    continue

                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.AnyFish:
                        # This seems to be how Disney did it.
                        progress = toon.quests[index][4] & pow(2, 16) - 1
                        completion = quest.testRecover(progress)
                        if completion[0]:
                            # Recovered!
                            self.__incrementQuestProgress(toon.quests[index])
                            if toon.quests:
                                toon.d_setQuests(toon.getQuests())

                            return quest.getItem()

        return 0

    def toonCalledClarabelle(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.PhoneQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())
