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
        self.gift_ideas = [
            gift_idea_elem for gift_idea_elem in self.gift_ideas if gift_idea != gift_idea_elem]
        self.gift_ideas.sort()
        self.reserved_gift_ideas[gift_idea] = reserver

    def remove_gift_reservation(self, gift_idea: str, reserver: str):
        if self.reserved_gift_ideas[gift_idea] == reserver:
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
        gift_manager.create_gift_reservation(gift_idea, reserver)
        st.success(
            f'Reservation for gift: {gift_idea} and reserver: {reserver} added successfully!')
    else:
        st.warning(
            'You need to provide the reserver email address to make reservation!')


def remove_button_callback(*args, **kwargs):
    gift_manager, gift_idea, reserver = args
    if not gift_manager.remove_gift_reservation(gift_idea, reserver):
        st.warning(
            f'Reservation for gift: {gift_idea} and reserver: {reserver} does not exist!')
    else:
        st.success(
            f'Reservation for gift: {gift_idea} and reserver: {reserver} removed successfully!')


def main():
    st.header('Martyna & Filip wedding gift list')

    gift_manager = get_gift_manager()

    reserver = st.text_input(
        label='Email of reserver',
        placeholder='nick@foo.com',
        help='Please enter your email address to make or remove gift idea reservation!')

    col1, col2 = st.columns(2)

    with col1:
        st.header('Available gift ideas')
        for gift_idea in gift_manager.gift_ideas:
            st.button(
                gift_idea,
                on_click=create_button_callback,
                args=(
                    gift_manager,
                    gift_idea,
                    reserver))

    with col2:
        st.header('Reserved gift ideas')
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
