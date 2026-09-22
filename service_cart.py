"""Session-local service selection for project inquiries."""

import streamlit as st


def add_service(title: str) -> None:
    cart = st.session_state.setdefault("service_cart", [])
    if title not in cart:
        cart.append(title)


def remove_service(title: str) -> None:
    cart = st.session_state.setdefault("service_cart", [])
    if title in cart:
        cart.remove(title)


def open_inquiry() -> None:
    st.session_state["navigation"] = "Contact"


def render_cart() -> None:
    st.title("Your service cart")
    st.write("Select the services you need and include them in a project inquiry. Pricing is confirmed by quote.")
    cart = st.session_state.get("service_cart", [])
    if not cart:
        st.info("Your cart is empty. Add services from the Services page.")
        return
    for title in list(cart):
        with st.container(border=True):
            st.subheader(title)
            st.button("Remove", key=f"remove-{title}", on_click=remove_service, args=(title,))
    st.caption("Selections are kept for this browser session. This is not an order or a payment.")
    st.button("Continue to project inquiry", on_click=open_inquiry)
