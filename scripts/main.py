import pygame
import sys
from card import Card
import random

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
colours = ['red', 'blue', 'green', 'yellow']

def create_deck(is_player=True):
    y = 450 if is_player else 50
    return [
        Card(random.choice(colours), random.choice(numbers), [280 + index * 30, y])
        for index in range(9)
    ]

def sort_deck(deck, is_player_deck=True):
    # Sort by colour, then number
    deck = sorted(deck, key=lambda card: (card.colour, card.number))

    # Compute starting X so cards are centered
    deck_length = len(deck)
    total_width = (deck_length - 1) * 30
    first_pos_x = 400 - total_width // 2

    # Y position depends on whether it's the player's or opponent's deck
    y_pos = 450 if is_player_deck else 50

    # Assign new positions and update rects
    for index, card in enumerate(deck):
        card.pos = [first_pos_x + index * 30, y_pos]
        card.rect.topleft = card.pos

    return deck

def opponent_turn(deck, current_card):
    for card in deck:
        if card.matches(current_card):
            deck.remove(card)
            card.start_animation([400, 250])
            return deck, card, None

    # No match, pick a card
    drawn_card = Card(random.choice(colours), random.choice(numbers), [200, 250])
    drawn_card.start_animation([400, 50])
    return deck, None, drawn_card


def draw_players_cards():
    hovered = None
    mouse_pos = pygame.mouse.get_pos()

    for players_card in reversed(players_deck):
        if players_card.rect.collidepoint(mouse_pos):
            hovered = players_card
            break

    for players_card in players_deck:
        players_card.rect.topleft = players_card.pos
        if players_card != hovered:
            screen.blit(players_card.image, players_card.pos)

    if hovered:
        # Enlarge hovered card
        screen.blit(pygame.transform.scale(hovered.image, (75, 105)),
                    (hovered.pos[0] - 10, hovered.pos[1] - 25))
    return hovered


pygame.init()
screen = pygame.display.set_mode((800, 600))

# Setup
players_deck = sort_deck(create_deck())
opponents_deck = sort_deck(create_deck(is_player=False), is_player_deck=False)
current_card = Card(colours[random.randint(0, len(colours)-1)], numbers[random.randint(0, len(numbers)-1)], [400, 250])
card_pile = Card('back', 'card', [200, 250])

# Game state
start_time = pygame.time.get_ticks()
not_clicked_recently = True
mouse_button_down = False
players_turn = True
opponent_thinking = False
thinking_time = 10000000
next_card = None
opponent_played = False
picked_up_card = None


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
    
    if not players_turn and not opponent_thinking and not opponent_played:
        opponents_deck, next_card, picked_up_card = opponent_turn(opponents_deck, current_card)
        opponents_deck = sort_deck(opponents_deck, is_player_deck=False)
        opponent_played = True

    
    hovered_card = draw_players_cards()
    
    # Redraw hovered card on top and enlarged
    if hovered_card:
        screen.blit(pygame.transform.scale(hovered_card.image, (75, 105)), (hovered_card.pos[0]-10, hovered_card.pos[1]-25))
        
        if (
            mouse_buttons[0] and
            players_turn and
                hovered_card.matches(current_card) and
            not_clicked_recently and
            not mouse_button_down
        ):
            players_deck.remove(hovered_card)
            next_card = hovered_card
            next_card.start_animation([400, 250])
            not_clicked_recently = False
            mouse_button_down = True
            players_deck = sort_deck(players_deck)
    
    elif card_pile.rect.collidepoint(mouse_pos) and mouse_buttons[0] and players_turn and not_clicked_recently and not mouse_button_down:
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