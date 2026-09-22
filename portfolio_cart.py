"""Session-local service selection for project inquiries."""

import streamlit as st


def save_cart_preferences() -> None:
    st.session_state["cart_preferences"] = {
        "budget": st.session_state.get("cart_budget", "Not decided"),
        "payment": st.session_state.get("payment_preference", ""),
    }


def select_work(filename: str, title: str, kind: str) -> None:
    st.session_state.setdefault("work_cart", {})[filename] = {"title": title, "kind": kind}
    st.session_state["navigation"] = "Cart"


def remove_work(filename: str) -> None:
    st.session_state.setdefault("work_cart", {}).pop(filename, None)


def add_service(title: str) -> None:
    cart = st.session_state.setdefault("service_cart", [])
    if title not in cart:
        cart.append(title)


def remove_service(title: str) -> None:
    cart = st.session_state.setdefault("service_cart", [])
    if title in cart:
        cart.remove(title)


def open_inquiry() -> None:
    save_cart_preferences()
    fields = st.session_state.setdefault("inquiry_fields", {})
    fields["budget"] = st.session_state.get("cart_budget", "Not decided")
    st.session_state.pop("contact_budget", None)
    st.session_state["inquiry_payment_preference"] = st.session_state.get("payment_preference", "")
    st.session_state["navigation"] = "Contact"


def render_cart() -> None:
    st.title("Your service cart")
    st.write("Select the services you need and include them in a project inquiry. Pricing is confirmed by quote.")
    cart = st.session_state.get("service_cart", [])
    works = st.session_state.get("work_cart", {})
    if not cart and not works:
        st.info("Your cart is empty. Add services from the Services page.")
        return
    for filename, work in list(works.items()):
        with st.container(border=True):
            st.subheader(work["title"])
            st.caption(f"{work['kind']} reference: {filename}")
            st.write("Awaiting pricing and standard limits" if work["kind"] == "Video" else "Price confirmed by quote")
            st.button("Remove", key=f"remove-work-{filename}", on_click=remove_work, args=(filename,))
    for title in list(cart):
        with st.container(border=True):
            st.subheader(title)
            st.button("Remove", key=f"remove-{title}", on_click=remove_service, args=(title,))
    st.caption("Selections are kept for this browser session. This is not an order or a payment.")
    preferences = st.session_state.get("cart_preferences", {})
    budgets = ["Not decided", "Under $100", "$100–$300", "$300–$750", "$750+"]
    st.selectbox("Budget range (USD)", budgets, index=budgets.index(preferences.get("budget", "Not decided")), key="cart_budget", on_change=save_cart_preferences)
    st.text_input("Preferred payment method (optional)", value=preferences.get("payment", ""), key="payment_preference", on_change=save_cart_preferences,
                  help="Request a method; availability will be confirmed with your quote.")
    st.caption("Payment methods and checkout are not configured yet. Proceed prepares an inquiry; it does not charge you.")
    st.button("Proceed to inquiry", on_click=open_inquiry)
