import random
import itertools


RANKS = "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
SUITS = "♥", "♦", "♣", "♠"
TRANS_TABLE = str.maketrans({"J": "11", "Q": "12", "K": "13", "A": "14", "♥": "4", "♦": "3", "♣": "2", "♠": "1"})


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def to_str(self) -> str:
        return f"{self.rank}{self.suit}"
    
    def equal_suit(self, other: "Card") -> bool:
        return self.suit == other.suit
    
    def more(self, other: "Card") -> bool:
        digit_rank = int(self.rank.translate(TRANS_TABLE))
        digit_other_rank = int(other.rank.translate(TRANS_TABLE))

        digit_suit = int(self.suit.translate(TRANS_TABLE))
        digit_other_suit = int(other.suit.translate(TRANS_TABLE))

        card1 = digit_rank, digit_suit
        card2 = digit_other_rank, digit_other_suit

        return card1 > card2

    def less(self, other: "Card") -> bool:
        return not self.more(other)

    
class Deck:
    def __init__(self) -> None:
        self.cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    
    def draw(self, x: int) -> list[Card]:
        cards_to_draw = self.cards[0:x]
        del self.cards[0:x]

        return cards_to_draw
    
    def show(self) -> None:

        card_list = " ".join(card.to_str() for card in self.cards)

        print(f"Колода[{len(self.cards)}]: {card_list}")


def find_card_for_player1(cards_on_table: list[Card], player_hand: list[Card]) -> Card | None:
    for card in player_hand:
        if card.rank in [table_card.rank for table_card in cards_on_table]:
            return card   


def find_card_for_player2(cards_on_table: list[Card], player_hand: list[Card]) -> Card | None:
    for card in player_hand:
        for table_card in cards_on_table:
            if card.more(table_card):
                return card


def use_card(card: Card, cards_on_table: list[Card], player_hand: list[Card]) -> None:
    cards_on_table.append(card)
    player_hand.remove(card)


def main() -> None:
    deck = Deck()
    deck.shuffle()
    deck.show()

    first_player_hand = deck.draw(10)
    second_player_hand = deck.draw(10)
    first_player_hand.sort(key=lambda card: int(card.rank.translate(TRANS_TABLE)))
    second_player_hand.sort(key=lambda card: int(card.rank.translate(TRANS_TABLE)))

    print(f'\nРаздали первому игроку: {" ".join(card.to_str() for card in first_player_hand)}')
    print(f'Раздали второму игроку: {" ".join(card.to_str() for card in second_player_hand)}\n')

    cards_on_table = []

    for turn_counter in itertools.count(start=1):

        print(f"Ход {turn_counter}")

        if turn_counter == 1:
            player1_card = random.choice(first_player_hand)
            print(f"Игрок 1: {player1_card.to_str()}")
            use_card(player1_card, cards_on_table, first_player_hand)
        else:
            player1_card = find_card_for_player1(cards_on_table, first_player_hand)
            
            cards_on_table.clear()

            if player1_card is None:
                print("Игрок 1: Не смог подкинуть\n\nИгрок 2 выиграл.")
                break
            else:
                print(f"Игрок 1: {player1_card.to_str()}")
                use_card(player1_card, cards_on_table, first_player_hand)

        player2_card = find_card_for_player2(cards_on_table, second_player_hand)

        if player2_card is None:
            print("Игрок 2: Не смог подкинуть\n\nИгрок 1 выиграл.")
            break
        else:
            print(f"Игрок 2: {player2_card.to_str()}")
            use_card(player2_card, cards_on_table, second_player_hand)

        print(f'\nУ первого игрока осталось: {" ".join(card.to_str() for card in first_player_hand)}')
        print(f'У второго игрока осталось: {" ".join(card.to_str() for card in second_player_hand)}\n')


if __name__ == "__main__":
    main()
