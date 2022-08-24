from typing import Dict, List

import streamlit as st
import yaml


class GiftManager():
    def __init__(self):
        with open('gifts.yaml', 'r') as gifts_yaml:
            gift_ideas = yaml.safe_load(gifts_yaml)['gifts']
        self.gift_ideas: List[str] = gift_ideas
        self.gift_ideas.sort()
        self.reserved_gift_ideas: Dict[str, str] = {}

    def create_gift_reservation(self, gift_idea: str, reserver: str):
        if gift_idea in self.gift_ideas:
            self.gift_ideas = [
                gift_idea_elem for gift_idea_elem in self.gift_ideas if gift_idea != gift_idea_elem]
            self.gift_ideas.sort()
            self.reserved_gift_ideas[gift_idea] = reserver
            return True
        else:
            return False

    def remove_gift_reservation(self, gift_idea: str, reserver: str):
        if gift_idea in self.reserved_gift_ideas and self.reserved_gift_ideas[
                gift_idea] == reserver:
            del self.reserved_gift_ideas[gift_idea]
            self.gift_ideas.append(gift_idea)
            self.gift_ideas.sort()
            return True
        else:
            return False


@st.experimental_singleton
def get_gift_manager() -> GiftManager:
    return GiftManager()


def create_button_callback(*args, **kwargs):
    gift_manager, gift_idea, reserver = args
    if reserver:
        if gift_manager.create_gift_reservation(gift_idea, reserver):
            st.success(
                f'Rezerwacja prezentu: {gift_idea} dla rezerwującego: {reserver} została dodana!')
            st.success(
                f'Reservation for gift: {gift_idea} and reserver: {reserver} added successfully!')
        else:
            st.warning(
                f'Ktoś zarezerwował prezent: {gift_idea} przed Tobą!')
            st.warning(
                f'Someone else reserved gift: {gift_idea} before you!')
    else:
        st.warning(
            'Musisz podać email rezerwującego, żeby zrobić rezerwację!')
        st.warning(
            'You need to provide the reserver email address to make reservation!')


def remove_button_callback(*args, **kwargs):
    gift_manager, gift_idea, reserver = args
    if not gift_manager.remove_gift_reservation(gift_idea, reserver):
        st.warning(
            f'Rezerwacja dla prezentu: {gift_idea} oraz rezerwującego: {reserver} nie istnieje!')
        st.warning(
            f'Reservation for gift: {gift_idea} and reserver: {reserver} does not exist!')
    else:
        st.success(
            f'Rezerwacja dla prezentu: {gift_idea} oraz rezerwujacego: {reserver} została usunięta!')
        st.success(
            f'Reservation for gift: {gift_idea} and reserver: {reserver} removed successfully!')


def main():
    st.header('Martyna & Filip - lista prezentów - wedding gift list')

    gift_manager = get_gift_manager()
    description_column_left, description_column_right = st.columns(2)

    with description_column_left:
        st.subheader('Instrukcja')
        st.markdown('Kochani Goście, dla nas **najważniejsza jest wasza obecność!** Jeżeli mimo to chcielibyście kupić nam dodatkowo jakiś prezent to poniżej znajdziecie kilka pomysłów. Do zarezerwowania prezentu wystarczy wpisać adres email i kliknąć na prezent w lewej kolumnie. By anulować rezerwację wystarczy kliknąć zarezerwowany prezent w prawej kolumnie uprzednio wpisując adres email podany przy rezerwacji.')

    with description_column_right:
        st.subheader('Instruction')
        st.markdown('Dear Guests, for us **the most important is your presence at our wedding!** If you want to buy a gift for us please consider the following ideas. To reserve the gift idea, specify your email address and click on the selected gift idea in the left column. To cancel your reservation you need to specify the same email address as in the reservation process and click on the gift idea in the right column.')

    reserver = st.text_input(
        label='Email rezerwującego - '
        'Email of reserver',
        placeholder='nick@foo.com',
        help='Podaj swój adres email, żeby dodać lub usunąć rezerwację prezentu! - '
        'Please enter your email address to make or remove gift idea reservation!')

    gift_column_left, gift_column_right = st.columns(2)

    with gift_column_left:
        st.subheader('Dostępne pomysły na prezenty - Available gift ideas')
        for gift_idea in gift_manager.gift_ideas:
            st.button(
                gift_idea,
                on_click=create_button_callback,
                args=(
                    gift_manager,
                    gift_idea,
                    reserver))

    with gift_column_right:
        st.subheader('Zarezerwowane pomysły na prezenty - Reserved gift ideas')
        for gift_idea in gift_manager.reserved_gift_ideas:
            st.button(
                gift_idea,
                on_click=remove_button_callback,
                args=(
                    gift_manager,
                    gift_idea,
                    reserver))


if __name__ == '__main__':
    main()
