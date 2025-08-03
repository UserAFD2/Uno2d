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

card_surface = pygame.transform.scale(pygame.image.load(r"C:\Users\djamesh\OneDrive\Pictures\uno2dcard.png"), (75, 105)).convert_alpha()
card_rect = card_surface.get_rect()
card_positions = [(400, 300),
                  (375, 300),
                  (350, 300),
                  (325, 300),
                  (300, 300),
                  (275, 300),
                  (250, 300),
                  (225, 300),]
    

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    

    screen.fill((255, 255, 255))  # Fill the screen with black
    
    mouse_pos = pygame.mouse.get_pos()
    
    for card_position in card_positions:
        screen.blit(card_surface, card_position)
    for card_position in card_positions:
        card_rect.x = card_position[0]
        card_rect.y = card_position[1]
        if card_rect.collidepoint(mouse_pos):
            screen.blit(pygame.transform.scale(card_surface, (90, 120)), (card_position[0]-15,  card_position[1]-15))
            break

    # for card_position in card_positions:     
    #     if card_surface
    #         pygame.draw.rect(screen, (200, 200, 200), card, border_radius=5)
    #         pygame.draw.rect(screen, (150, 150, 150), card, width=2, border_radius=5)
               
    
    pygame.display.flip()  # Update the display
    
pygame.quit()
sys.exit()