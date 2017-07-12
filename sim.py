import random

class Card(object):
    played = False
    name = 'Location'
    location_id = -1

    def __unicode__(self):
        return self.name

    def ability(self, player):
        print 'hello ' + unicode(player.id_number)

    def play(self, player):
        if self.played:
            print 'something went wrong'
            return self
        else:
            self.played = True
            print 'played ' + unicode(self.name)
            self.ability(player)
            return self
    
    def caught(self, player):
        self.played = True
    
    def discard(self):
        self.played = True
        print 'discarded ' + unicode(self.name)

    def recover(self):
        if self.played == True:
            self.played = False
            print 'recovered ' + self.name

class Jungle(Card):
    name = 'Jungle'
    location_id = 1

    def ability(self, player):
        self.recover()
        recover_me = []
        for x in player.hand:
            if x.played == True:
                recover_me.append(x)
        if len(recover_me) > 0:
            random.choice(recover_me).recover()

class River(Card):
    name = 'River'
    location_id = 2

    def ability(self, player):
        player.river_turn = True

class Beach(Card):
    name = 'Beach'
    location_id = 3
    
    def ability(self, player):
        player.game.beach_this_turn = True

class Rover(Card):
    name = 'Rover'
    location_id = 4

    def ability(self, player):
        if len(player.not_in_hand) > 0:
            random.shuffle(player.not_in_hand)
            for location in player.not_in_hand:
                new_card = player.game.rover.get_location_or_none(location)
                if new_card != None:
                    player.hand.append(new_card)
                    print 'adding ' + unicode(new_card.name)
                    player.not_in_hand.remove(location)
                    break
            


class Swamp(Card):
    name = 'Swamp'
    location_id = 5

    def ability(self, player):
        self.Played = False
        for two in range(2):
            recover_me = []
            for x in player.hand:
                if x.played == True:
                    recover_me.append(x)
            if len(recover_me) > 0:
                random.choice(recover_me).recover()

class Shelter(Card):
    name = 'Shelter'
    location_id = 6

    #TODO
    def ability(self, player):
        print 'how to abstract survival cards? fractional rescue points?'

class Wreck(Card):
    name = 'Wreck'
    location_id = 7

    def ability(self, player):
        player.game.wreck_this_turn = True

class Source(Card):
    name = 'Source'
    location_id = 8

    def ability(self, player):
        injured = []
        for x in player.game.hunted:
            if x.will < 3:
                injured.append(x)
        if len(injured) > 0:
            healed = random.choice(injured)
            healed.will += 1
            print 'healed player ' + unicode(healed.id_number)
        else:
            print 'abstract survival card'

class Artefact(Card):
    name = 'Artefact'
    location_id = 9

    def ability(self, player):
        player.artefact_turn = True

class Lair(Card):
    name = 'Lair'
    location_id = 0
    copy_abilities = [None, Jungle(), River(), Beach(), Rover(), Swamp(), Shelter(), Wreck(), Source()]


    def caught(self, player):
        player.will -= 1
        player.will_zero()
        self.played = True

    def ability(self, player):
        discard_pile = []
        for x in player.hand:
            if x.played == True:
                discard_pile.append(x)
        if len(discard_pile) > 2:
            for x in player.hand:
                if x != self:
                    x.recover()
        else:
            if player.alien_loc != 9:
                print 'copying The ' + unicode(self.copy_abilities[player.alien_loc].name) 
                loc = self.copy_abilities[player.alien_loc].ability(player)
            elif player.alien_loc == 9:
                print 'cannot copy the Artefact'




class RoverDeck(object):
    deck = []

    def __init__(self, num_players):
        copies = 0
        deck = []
        if num_players == 1:
            copies = 1
        elif num_players in range(2,4):
            copies = 2
        else:
            copies = 3
        for x in range(copies):
            self.deck.append(Swamp())
            self.deck.append(Shelter())
            self.deck.append(Wreck())
            self.deck.append(Source())
            self.deck.append(Artefact())

    def get_location_or_none(self, location_id):
        location = None
        deck_index = None
        for index, item in enumerate(self.deck):
            if item.location_id == location_id:
                deck_index = index
                print index
                break
        if deck_index != None:
            location = self.deck.pop(deck_index)
        print location
        return location

class Alien(object):
    locations = []
    current_selection = [-1, -1] #alien, artemia

    def __init__(self):
        self.locations = [0,1,2,3,4]
        self.current_selection[1] = random.randrange(5)

    def pick(self):
        self.current_selection[0] = random.choice(self.locations)
        self.current_selection[1] = random.choice(self.locations)
        while self.current_selection[0] == self.current_selection[1] and len(set(self.locations)) > 1:

            self.current_selection[1] = random.choice(self.locations)

    def evaluate(self, hunted):
        self.locations = []
        hands = []
        for x in hunted:
            hands.append(x.hand)
        for hand in hands:
            for card in hand:
                if card.played == False:
                    self.locations.append(card.location_id)
        self.locations.sort()
        print self.locations


class Player(object):

    will = 0
    hand = []
    id_number = 0
    river_turn = False
    artefact_turn = False
    not_in_hand = []
    current_selection= []
    game = None
    alien_loc = -1

    def __init__(self, id_num):
        self.will = 3
        self.id_number = id_num
        self.hand = [Lair(), Jungle(), River(), Beach(), Rover()]
        self.not_in_hand = [5,6,7,8,9]

    def init_game(self, game):
        self.game = game

    def get_available_cards(self):
        available_cards = []
        for x in self.hand:
            if x.played == False:
                available_cards.append(x)
        return available_cards

    def resist(self):
        self.will -= 1
        if not self.will_zero():
            print 'resisting(' + unicode(self.will) + ')'
            discard = []
            for x in self.hand:
                if x.played == True:
                    discard.append(x)
            recovered = random.sample(discard, 2)
            for x in recovered:
                x.recover()

    def giveup(self):
        self.will = 3
        for x in self.hand:
            x.recover()
        self.game.artemia()

    def will_zero(self):
        if self.will <= 0:
            print 'giving up'
            self.giveup()
            return True
        else:
            return False

    def select_card(self):
        print 'river ' + unicode(self.river_turn)
        self.current_selection = []
        playable = self.get_available_cards()
        if playable == []:
            self.resist()
            playable = self.get_available_cards() #trying to be clever?
        if self.river_turn and len(playable) > 1 or self.artefact_turn and len(playable) > 1: 
            random.shuffle(playable)
            self.current_selection = playable[0:2]
        else: 
            self.current_selection.append(random.choice(playable))


    def play(self, alien_pick):
        self.alien_loc = alien_pick[0] #this is such an awful way to faciliate lair
        if self.river_turn:

            self.river_turn = False
            'river turn!'
            if self.current_selection[0].location_id == alien_pick[0]:
                self.current_selection.remove(self.current_selection[0])
            else:
                self.current_selection.remove(self.current_selection[-1])
        if self.artefact_turn:
            self.artefact_turn = False
        for x in self.current_selection:
            if x.location_id == alien_pick[0]:
                x.caught(self)
                self.caught()
            elif x.location_id == alien_pick[1] and self.game.rescue_count <=6:
                x.discard()
                self.artemia()
            else:
                x.play(self)


    def artemia(self):
        print 'artemia-ed player ' + unicode(self.id_number) + '(' + unicode(self.will) + ')'
        self.will_zero()
        discard_one = self.get_available_cards() 
        if len(discard_one) > 0:
            random.choice(discard_one).discard()

    def caught(self):
        self.will -= 1
        print 'caught player ' + unicode(self.id_number) + '(' + unicode(self.will) + ')'

        #special will_zero/giveup for the edge case single artemia advance due to total will loss in phase 3
        if self.will <= 0:
            print 'giving up'
            self.will = 3
            for x in self.hand:
                x.recover()
            if not self.game.will_loss_this_turn:
                self.game.artemia()
                self.game.will_loss_this_turn = True

        if not self.game.caught_this_turn:
            self.game.caught_this_turn = True
            self.game.artemia()


class Game(object):
    hunted = []
    rover = None
    alien = None
    rescue_count = 0
    artemia_count = 0
    caught_this_turn = False
    will_loss_this_turn = False
    beach_this_turn = False
    beach_marker_on = False
    wreck_this_turn = False

    def __init__(self, hunted, rover, alien):
        self.hunted = hunted
        for x in self.hunted:
            x.init_game(self)
        self.rover = rover
        self.alien = alien
        self.rescue_count = 12 + len(hunted)
        self.artemia_count = 6 + len(hunted)

    def phase_1(self):
        for x in self.hunted:
            x.select_card()
            print x.current_selection
        self.alien.evaluate(self.hunted)
        print 'phase 1 complete'

    def phase_2(self):
        self.alien.pick()
        print self.alien.current_selection
        print 'phase 2 complete'

    def phase_3(self):
        for x in self.hunted:
            x.play(self.alien.current_selection)
        if self.beach_this_turn and self.beach_marker_on:
            print 'beach beacon activated'
            self.rescue()
            self.beach_marker_on = False
        elif self.beach_this_turn and not self.beach_marker_on:
            print 'beach beacon primed'
            self.beach_marker_on = True
        if self.wreck_this_turn:
            print 'wreck beacon activated'
            self.rescue()

    def phase_4(self):
        self.rescue()

        print 'artemia ' + unicode(self.artemia_count)
        print '====================='
        if self.artemia_count <= 0 and self.artemia_count < self.rescue_count:
            print '*****alien wins*****'
            return True
        elif self.rescue_count <= 0:
            print '*****hunted win*****'
            return False
        #cleanup
        self.will_loss_this_turn = False
        self.caught_this_turn = False
        self.beach_this_turn = False
        self.wreck_this_turn = False
        return False
    
    def artemia(self):
        self.artemia_count -= 1
        print 'artemia ' + unicode(self.artemia_count)

    def rescue(self):
        self.rescue_count -= 1
        print 'rescue ' + unicode(self.rescue_count)

    def not_alone(self):
        while self.artemia_count > 0 and self.rescue_count > 0:
            self.phase_1()
            raw_input('')
            self.phase_2()
            raw_input('')
            self.phase_3()
            raw_input('')
            self.phase_4()
            raw_input('')

    def sim(self):
        alien_win = False
        while self.artemia_count > 0 and self.rescue_count > 0:
            self.phase_1()
            self.phase_2()
            self.phase_3()
            alien_win = self.phase_4()
        return alien_win

def main():
    players = input('how many hunted(1-6)')
    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    hunted = []
    for x in range(players):
        player = Player(x)
        hunted.append(player)
    rover = RoverDeck(players)
    alien = Alien()

    return Game(hunted, rover, alien)


def sim(players, trials):
    artemia = 0
    humans = 0
    for x in range(0,trials):
        players = players
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        hunted = []
        for x in range(players):
            player = Player(x)
            hunted.append(player)
        rover = RoverDeck(players)
        alien = Alien()

        game = Game(hunted, rover, alien)

        if game.sim():
            artemia += 1
        else:
            humans += 1
    print unicode(trials) + ' trial(s)'
    print 'artemia won ' + unicode(artemia)
    print 'hunted won ' + unicode(humans)
