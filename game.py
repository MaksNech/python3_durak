# -*- coding: utf-8 -*-
import sys
import os
import curses
import random
from random import shuffle
import numpy as np


class UserInterface:

    def __init__(self, h, w):
        """Constructor"""
        self.height = h
        self.width = w

    def render_status_bar(self, stdscr, statusbarstr):
        """Render status bar"""

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(self.height-1, 0, statusbarstr)
        stdscr.addstr(self.height-1, len(statusbarstr), " " *
                      (self.width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

    def showCard(self, stdscr, card):
        """Show one card"""
        whstr = str(card.symbol+" "+card.suit+" " +
                    card.title)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    def showCardSets(self, stdscr, card_sets_list, max_h, max_w):
        """Show sets of cards"""
        max_x = max_h
        max_y = max_w
        x = 0
        y = 0
        for card_set in card_sets_list:

            stdscr.addstr(x, y, str(card_set.name), curses.color_pair(1))
            x = x+1
            if x == max_x-1:
                x = 0
                y = y+20
            stdscr.addstr(x, y, "Priority: " +
                          str(card_set.sum_priority), curses.color_pair(1))
            x = x+1
            if x == max_x-1:
                x = 0
                y = y+20

            for card in card_set.temp_set:
                whstr = str(card.symbol+" "+card.suit + " " +
                            card.title)
                stdscr.addstr(x, y, whstr, curses.color_pair(1))
                x = x+1
                if x == max_x-1:
                    x = 0
                    y = y+20
            stdscr.addstr(x, y, " "*15, curses.color_pair(1))
            x = x+1
            if x == max_x-1:
                x = 0
                y = y+20


class PlayingCard:
    def __init__(self, suit, symbol, trump_suit, title, priority):
        """Constructor"""
        self.suit = suit
        self.symbol = symbol
        self.trump_suit = trump_suit
        self.title = title
        self.priority = priority


class CardDeck:
    suits_symbols = {'diamonds': '♦', 'clubs': '♣',
                     'hearts ': '♥', 'spades': '♠'}
    title_priority = {"6": 6, "7": 7, "8": 8,
                      "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    def __init__(self):
        """Constructor"""
        self.deck = []
        self.trump_suit = ""
        self.card_trump_suit = object
        for suit, symbol in CardDeck.suits_symbols.items():
            for title, priority in CardDeck.title_priority.items():
                self.deck.append(PlayingCard(
                    suit, symbol, False, title, priority))

    def shuffle_cards(self):
        """Shuffle cards in deck"""
        np.random.shuffle(self.deck)

    def set_trump_suit(self):
        """Set trump suit card in deck"""
        digit = random.randint(1, len(self.deck))
        self.trump_suit = self.deck[digit].suit
        self.card_trump_suit = self.deck[digit]
        for card in self.deck:
            if card.suit == self.trump_suit:
                card.trump_suit = True
                card.priority = card.priority+9
        temp = self.deck[digit]
        self.deck.remove(temp)
        self.deck.append(temp)

    def show(self, stdscr,  max_h, max_w):
        """Show all cards in deck"""
        x = 0
        y = 0
        max_x = max_h
        max_y = max_w
        if not self.deck:
            mes = "Sorry, card deck is empty"
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, 0, mes)
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)

        else:
            for card in self.deck:
                whstr = str(card.symbol+" "+card.suit+" " +
                            card.title)
                stdscr.addstr(x, y, whstr, curses.color_pair(1))
                x = x+1
                if x == max_x:
                    x = 0
                    y = y+30


class CardSet:

    def __init__(self, card_deck):
        """Constructor"""
        self.temp_set = []
        self.sum_priority = 0
        self.name = ""
        j = 0
        while True:
            for i in card_deck:
                temp = i
                self.temp_set.append(temp)
                j = j+1
                if j == 6:
                    del card_deck[:6]
                    break
            break

        for i in self.temp_set:
            self.sum_priority = self.sum_priority+i.priority

    @staticmethod
    def sort_set_by_priority(self):
        """Sort by priority method"""
        return self.sum_priority


class Game:

    def __init__(self, players):
        """Constructor"""
        self.players = players
        self.max_players = 6
        self.min_players = 2
        self.card_deck = CardDeck()
        self.card_sets = []

    def create_card_sets(self):
        """Create a list of card sets"""
        counter = self.players
        while counter > 0:
            self.card_sets.append(CardSet(self.card_deck.deck))
            self.card_sets[len(self.card_sets)-1].name = "Player-"+str(counter)
            counter = counter-1

    def get_sorted_sets(self, card_sets_list):
        """Sort list by value of priority"""
        sorted_list = sorted(
            card_sets_list, key=CardSet.sort_set_by_priority, reverse=True)
        return sorted_list

    @staticmethod
    def start_game(stdscr):
        """Main method that starts game"""
        k = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Loop where k is the last character pressed
        while (k != ord('q')):

            # Initialization
            stdscr.clear()
            stdscr.refresh()

            height, width = stdscr.getmaxyx()
            ui = UserInterface(height, width)

            # Declaration of strings
            title = 'The "Durak" card game'
            subtitle = "Written by Maksym Nechypurenko"
            keystr = "Press 'Enter' to start"
            statusbarstr = "Press: | 'q' to exit | 'Enter' to start "

            # Centering calculations
            start_x_title = int(
                (width // 2) - (len(title) // 2) - len(title) % 2)
            start_x_subtitle = int(
                (width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
            start_x_keystr = int(
                (width // 2) - (len(keystr) // 2) - len(keystr) % 2)
            start_y = int((height // 2) - 2)

            # Render status bar
            ui.render_status_bar(
                stdscr, statusbarstr)

            # Turning on attributes for title
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)

            # Rendering title
            stdscr.addstr(start_y, start_x_title, title)

            # Turning off attributes for title
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)

            # Print rest of text
            stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)

            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(start_y + 3, (width // 2) - 4, '♦')
            stdscr.attroff(curses.color_pair(4))
            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(start_y + 3, (width // 2) - 2, '♣')
            stdscr.attron(curses.color_pair(5))
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(start_y + 3, (width // 2), '♥')
            stdscr.attroff(curses.color_pair(4))
            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(start_y + 3, (width // 2) + 2, '♠')
            stdscr.attroff(curses.color_pair(5))

            stdscr.addstr(start_y + 5, start_x_keystr, keystr)

            stdscr.move(height-1, width-1)

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            k = stdscr.getch()

            if k == 10 or k == curses.KEY_ENTER:

                players_amount = 0
                # flags, variables of saved state
                flag_game_is_created = False
                flag_deck_is_shuffled = False
                flag_trump_suit_is_set = False
                flag_card_sets_is_created = False

                while k != ord('q'):

                    stdscr.clear()

                    while players_amount == 0:
                        stdscr.clear()

                        keystr = "Please, input how many players will play:"
                        pl_2_str = "Press '2' | if two players"
                        pl_3_str = "Press '3' | if three players"
                        pl_4_str = "Press '4' | if four players"
                        pl_5_str = "Press '5' | if five players"
                        pl_6_str = "Press '6' | if six players"

                        stdscr.attron(curses.color_pair(2))
                        stdscr.attron(curses.A_BOLD)
                        stdscr.addstr(start_y - 2, (width // 2) -
                                      (len(keystr)//2), keystr)
                        stdscr.attroff(curses.color_pair(2))
                        stdscr.attroff(curses.A_BOLD)
                        stdscr.addstr(start_y, (width // 2) -
                                      (len(pl_2_str)//2), pl_2_str)
                        stdscr.addstr(start_y + 1, (width // 2) -
                                      (len(pl_2_str)//2), pl_3_str)
                        stdscr.addstr(start_y + 2, (width // 2) -
                                      (len(pl_2_str)//2), pl_4_str)
                        stdscr.addstr(start_y + 3, (width // 2) -
                                      (len(pl_2_str)//2), pl_5_str)
                        stdscr.addstr(start_y + 4, (width // 2) -
                                      (len(pl_2_str)//2), pl_6_str)

                        k = stdscr.getch()

                        if k == ord('2'):
                            players_amount = 2

                        elif k == ord('3'):
                            players_amount = 3

                        elif k == ord('4'):
                            players_amount = 4

                        elif k == ord('5'):
                            players_amount = 5

                        elif k == ord('6'):
                            players_amount = 6

                        stdscr.clear()

                    if flag_game_is_created == False:
                        # create Game object
                        newGame = Game(players_amount)
                        deck = newGame.card_deck
                        flag_game_is_created = True

                    show_card_deck_str = "Press 's' | to show cards in the deck"
                    shuffle_card_deck_str = "Press 'x' | to shuffle the deck"
                    choose_trump_str = "Press 't' | to choose trump card"
                    create_card_sets_str = "Press 'с' | to create card sets"
                    show_card_sets_priority_str = "Press 'r' | to show the strongest card set"

                    stdscr.addstr(start_y-2, (width // 2) -
                                  (len(show_card_deck_str)//2), show_card_deck_str)
                    stdscr.addstr(start_y-1, (width // 2) -
                                  (len(show_card_deck_str)//2), shuffle_card_deck_str)
                    stdscr.addstr(start_y, (width // 2) -
                                  (len(show_card_deck_str)//2), choose_trump_str)
                    stdscr.addstr(start_y + 1, (width // 2) -
                                  (len(show_card_deck_str)//2), create_card_sets_str)
                    stdscr.addstr(start_y + 2, (width // 2) -
                                  (len(show_card_deck_str)//2), show_card_sets_priority_str)

                    # Render status bar
                    ui.render_status_bar(
                        stdscr, "Press: | 'q' to exit")

                    # Wait for next input
                    k = stdscr.getch()

                    if k == ord('s'):
                        while (k != ord('b')):
                            stdscr.clear()
                            stdscr.refresh()
                            deck.show(stdscr, height, width)
                            # Render status bar
                            ui.render_status_bar(
                                stdscr, "Press: | 'b' to back")
                            k = stdscr.getch()

                    elif k == ord('x'):
                        deck.shuffle_cards()
                        flag_deck_is_shuffled = True
                        while (k != ord('b')):
                            stdscr.clear()
                            stdscr.refresh()
                            deck.show(stdscr, height, width)
                            # Render status bar
                            ui.render_status_bar(
                                stdscr, "Press: | 'b' to back")
                            k = stdscr.getch()

                    elif k == ord('t'):
                        if flag_deck_is_shuffled == True:
                            if flag_trump_suit_is_set == False:
                                deck.set_trump_suit()
                                flag_trump_suit_is_set = True
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                ui.showCard(stdscr, deck.card_trump_suit)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()
                        else:
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                mes = "First you need to shuffle card deck"
                                stdscr.attron(curses.color_pair(2))
                                stdscr.attron(curses.A_BOLD)
                                stdscr.addstr(
                                    start_y, (width // 2) -
                                    (len(mes)//2), mes)
                                stdscr.attroff(curses.color_pair(2))
                                stdscr.attroff(curses.A_BOLD)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()

                    elif k == ord('c'):
                        if flag_trump_suit_is_set == True:
                            if flag_card_sets_is_created == False:
                                newGame.create_card_sets()
                                flag_card_sets_is_created = True
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                ui.showCardSets(
                                    stdscr, newGame.card_sets, height, width)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()
                        else:
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                mes = "First you need to set trump suit card"
                                stdscr.attron(curses.color_pair(2))
                                stdscr.attron(curses.A_BOLD)
                                stdscr.addstr(
                                    start_y, (width // 2) -
                                    (len(mes)//2), mes)
                                stdscr.attroff(curses.color_pair(2))
                                stdscr.attroff(curses.A_BOLD)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()

                    elif k == ord('r'):
                        if flag_card_sets_is_created == True:
                            sorted_list = newGame.get_sorted_sets(
                                newGame.card_sets)[:1]
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                ui.showCardSets(
                                    stdscr, sorted_list, height, width)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()
                        else:
                            while (k != ord('b')):
                                stdscr.clear()
                                stdscr.refresh()
                                mes = "First you need to create card sets"
                                stdscr.attron(curses.color_pair(2))
                                stdscr.attron(curses.A_BOLD)
                                stdscr.addstr(
                                    start_y, (width // 2) -
                                    (len(mes)//2), mes)
                                stdscr.attroff(curses.color_pair(2))
                                stdscr.attroff(curses.A_BOLD)
                                # Render status bar
                                ui.render_status_bar(
                                    stdscr, "Press: | 'b' to back")
                                k = stdscr.getch()

                    # Refresh the screen
                    stdscr.refresh()
                    stdscr.clear()


def main():

    curses.wrapper(Game.start_game)


if __name__ == "__main__":
    main()
