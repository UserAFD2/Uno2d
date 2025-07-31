import pygame
import sys
import random

from pygame.examples.stars import move_stars


class Card:
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number

    def __repr__(self):
        return f"{self.colour} {self.number}"

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
colours = ['red', 'blue', 'green', 'yellow']

def create_deck():
    deck = []
    for i in range(9):
        deck.append(Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)]))
    return deck

deck = create_deck()
print(f"Deck created: {deck}")
current_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)])
moves = 0
playable_card = True
while playable_card:
    print(f"Deck: {deck}")
    print(f"Current card: {current_card}")
    temp_card = current_card
    if len(deck) < 1:
        print("No more cards in the deck, exiting...")
        playable_card = False
        break
    for card in deck:
        if card.colour == current_card.colour:
            print(f"Playable card found: {card}")
            current_card = card
            deck.remove(card)
            break
    for card in deck:
        if card.number == current_card.number:
            print(f"Playable card found: {card}")
            current_card = card
            deck.remove(card)
            break
    if temp_card == current_card:
        print("Picking up card...")
        picked_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)])
        if picked_card.number == current_card.number or picked_card.colour == current_card.colour:
            print(f"Playable card picked: {picked_card}")
            current_card = picked_card
        else:
            print(f"Picked card {picked_card} is not playable, continuing...")
            deck.append(picked_card)
    moves += 1
    
print(f"Game finished in {moves} moves. Thanks for playing!")
        
pygame.init()
screen = pygame.display.set_mode((800, 600))


run = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255, 255, 255))  # Fill the screen with black
    pygame.display.flip()  # Update the display
    
pygame.quit()
sys.exit()