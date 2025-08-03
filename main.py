
import pygame
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource for dev and PyInstaller .exe """
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import random


class Card:
    def __init__(self, colour, number, pos):
        self.colour = colour
        self.number = number
        img_path = resource_path(f"Uno/individual/{colour}/{number}_{colour}.png")
        self.image = pygame.transform.scale(pygame.image.load(img_path), (75, 105)).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        
        # Animation state
        self.animating = False
        self.start_pos = None
        self.target_pos = None
        self.animation_start_time = 0
        self.animation_duration = 500  # ms

    def start_animation(self, target_pos):
        self.animating = True
        self.start_pos = self.pos[:]
        self.target_pos = target_pos
        self.animation_start_time = pygame.time.get_ticks()

    def update_animation(self):
        if self.animating:
            now = pygame.time.get_ticks()
            elapsed = now - self.animation_start_time
            duration = self.animation_duration

            t = min(elapsed / duration, 1)  # Normalized time from 0 to 1

            # Linear interpolation
            self.pos[0] = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * t
            self.pos[1] = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * t
            self.rect.topleft = self.pos

            if t >= 1:
                self.animating = False

    def __repr__(self):
        return f"{self.colour} {self.number}"

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
colours = ['red', 'blue', 'green', 'yellow']

def create_deck(is_player_deck=True):
    deck = []
    if is_player_deck:
        for i in range(9):
            deck.append(Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [280+i*30, 450]))
    else:
        for i in range(9):
            deck.append(Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [280+i*30, 50]))
    return deck

def sort_deck(deck, is_player_deck=True):
    deck = sorted(deck, key=lambda card: (card.colour, card.number))
    deck_length = len(deck)
    if deck_length % 2 == 0:
        first_pos = 400 - (deck_length // 2)*30+15
    else:
        first_pos = 400 - (deck_length // 2)*30
    if is_player_deck:
        for i, card in enumerate(deck):
            card.pos = [first_pos + i * 30, 450]
            card.rect.topleft = card.pos
    else:
        for i, card in enumerate(deck):
            card.pos = [first_pos + i * 30, 50]
            card.rect.topleft = card.pos
    return deck

        

def opponent_turn(deck, current_card):
    # print(f"Deck: {deck}")
    # print(f"Current card: {current_card}")
    temp_card = current_card
    picked_up_card = None
    next_card = None
    played_card = False
    if len(deck) < 1:
        print("Opponent wins")
    for card in deck:
        if card.colour == current_card.colour:
            next_card = card
            next_card.start_animation([400, 250])
            deck.remove(card)
            played_card = True
            break
    for card in deck:
        if played_card:
            break
        if card.number == current_card.number:
            next_card = card
            next_card.start_animation([400, 250])
            deck.remove(card)
            played_card = True
            break
    if not played_card:
        print("Picking up card...")
        picked_up_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [200, 250])
        picked_up_card.start_animation([400, 50])
        if picked_up_card.number == current_card.number or picked_up_card.colour == current_card.colour:
            # next_card = picked_card
            # next_card.start_animation([400, 200])
            pass
        else:
            pass
            
    return deck, next_card, picked_up_card
          
pygame.init()
screen = pygame.display.set_mode((800, 600))

players_deck = create_deck()
opponents_deck = create_deck(is_player_deck=False)
print(f"Your deck: {players_deck}")
current_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [400, 250])
card_pile = Card('back', 'card', [200, 250])
start_time = pygame.time.get_ticks()
not_clicked_recently = True
mouse_button_down = False
players_turn = True
opponent_thinking = False
thinking_time = 10000000
next_card = None
opponent_played = False
picked_up_card = None
players_deck = sort_deck(players_deck)
opponents_deck = sort_deck(opponents_deck, is_player_deck=False)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    

    screen.fill((100, 100, 100))  # Fill the screen with black
    opponent_thinking = (pygame.time.get_ticks() - start_time) < thinking_time
    not_clicked_recently = (pygame.time.get_ticks() - start_time) > 500  # 500 ms cooldown for clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    if not mouse_buttons[0]:
        mouse_button_down = False
    hovered_card = None
    
    if not players_turn and not opponent_thinking and not opponent_played:
        opponents_deck, next_card, picked_up_card = opponent_turn(opponents_deck, current_card)
        opponents_deck = sort_deck(opponents_deck, is_player_deck=False)
        opponent_played = True

    
    # Check for hover starting from the topmost card
    for card in reversed(players_deck):  # Topmost card drawn last
        if card.rect.collidepoint(mouse_pos):
            hovered_card = card
            break
        # Draw all cards except the hovered one
    for card in players_deck:
        card.rect.topleft = card.pos  # Update rect position in case pos changed
        if card != hovered_card:
            screen.blit(card.image, card.pos)
    
    # Redraw hovered card on top and enlarged
    if hovered_card:
        screen.blit(pygame.transform.scale(hovered_card.image, (75, 105)), (hovered_card.pos[0]-10, hovered_card.pos[1]-25))
        
        is_valid_play = (
                hovered_card.number == current_card.number or
                hovered_card.colour == current_card.colour
        )
        
        if (
            mouse_buttons[0] and
            players_turn and
            is_valid_play and
            not_clicked_recently and
            not mouse_button_down
        ):
            players_deck.remove(hovered_card)
            next_card = hovered_card
            next_card.start_animation([400, 250])
            not_clicked_recently = False
            mouse_button_down = True
            players_deck = sort_deck(players_deck)
    
    if card_pile.rect.collidepoint(mouse_pos) and mouse_buttons[0] and players_turn and not_clicked_recently and not mouse_button_down:
        picked_up_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [200, 250])
        picked_up_card.start_animation([400, 450])

        not_clicked_recently = False
        mouse_button_down = True



    screen.blit(current_card.image, current_card.pos)
    if picked_up_card:
        picked_up_card.update_animation()
        screen.blit(card_pile.image, picked_up_card.pos)
        if not picked_up_card.animating:
            if opponent_played:
                opponents_deck.append(picked_up_card)
                opponents_deck = sort_deck(opponents_deck, is_player_deck=False)
                players_turn = True
                not_clicked_recently = True
                opponent_played = False
                picked_up_card = None
            else:
                players_deck.append(picked_up_card)
                players_deck = sort_deck(players_deck)
                players_turn = False
                opponent_thinking = True
                thinking_time = random.randint(500, 2000)
                start_time = pygame.time.get_ticks()
                picked_up_card = None
    # Update animations for card
    if next_card:
        next_card.update_animation()
        screen.blit(next_card.image, next_card.pos)
        if not next_card.animating:
            current_card = next_card
            if opponent_played:
                players_turn = True
                not_clicked_recently = True
                opponent_played = False
                next_card = None
            else:
                players_turn = False
                opponent_thinking = True
                thinking_time = random.randint(500, 2000)
                start_time = pygame.time.get_ticks()
                next_card = None


    for i, card in enumerate(opponents_deck):
        screen.blit(pygame.transform.rotate(card_pile.image, 180), card.pos)
    screen.blit(card_pile.image, card_pile.pos)

    
    pygame.display.flip()  # Update the display
    
pygame.quit()
sys.exit()