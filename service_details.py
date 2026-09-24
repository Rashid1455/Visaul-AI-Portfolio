"""Service URLs, live estimates, review, and JSON order submission."""
import json
import os
from pathlib import Path
from uuid import uuid4
import streamlit as st
from orders import save_order
from service_catalog import load_catalog, validate_selection

def open_service(title):
    slug = next(k for k,v in load_catalog()["services"].items() if v["title"] == title)
    st.session_state["selected_service"] = slug
    st.session_state["navigation"] = "Service details"
    st.query_params["service"] = slug
    st.session_state["service_url_seen"] = slug

def sync_service_url():
    slug = st.query_params.get("service")
    if slug and slug != st.session_state.get("service_url_seen"):
        st.session_state["service_url_seen"] = slug
        st.session_state["selected_service"] = slug
        st.session_state["navigation"] = "Service details"

def clear_service_url():
    if st.session_state.get("navigation") != "Service details":
        st.query_params.pop("service", None)
        st.session_state.pop("service_url_seen", None)

def show_price(pricing):
    st.metric("Estimated budget", "Request a quote" if pricing["quote_required"] else f"{pricing['currency']} {pricing['estimated_total']:,}")

def render_service_details(assets):
    catalog = load_catalog()
    slug = st.session_state.get("selected_service")
    if slug not in catalog["services"]:
        st.info("Choose a service from Services. This service URL is not available.")
        return
    service = catalog["services"][slug]
    st.title(service["title"])
    st.write(service["description"])
    st.markdown(f"[Link to this service](?service={slug})")
    st.subheader("Examples")
    st.caption("Portfolio style references; final deliverables depend on your brief.")
    for column, filename in zip(st.columns(2), service["samples"]):
        with column:
            sample = assets / filename
            if sample.is_file():
                if sample.suffix.lower() == ".mp4":
                    st.video(str(sample))
                else:
                    st.image(str(sample), width="stretch")
    key = f"order-flow-v2-{slug}"
    flow = st.session_state.setdefault(key, {"id":str(uuid4()), "stage":"configure"})
    if "receipt" in flow:
        receipt = flow["receipt"]
        st.success(f"Request submitted: {receipt['order_id']}")
        st.info("Payment status: unpaid. The studio will confirm your scope and final price. No email has been sent automatically.")
        st.download_button("Download order receipt", json.dumps(receipt,indent=2), file_name=f"{receipt['order_id']}.json", mime="application/json")
        if st.button("Start another request"):
            st.session_state[key] = {"id":str(uuid4()), "stage":"configure"}
            st.rerun()
        return
    if flow["stage"] == "configure":
        st.subheader("Options and budget estimate")
        previous = flow.get("selection", {})
        option = st.selectbox("Requested deliverable", service["options"], index=service["options"].index(previous.get("option", service["options"][0])))
        dimensions = st.selectbox("Dimensions", service["dimensions"], index=service["dimensions"].index(previous.get("dimensions", service["dimensions"][0])))
        quantity = st.number_input("Quantity",1,100,value=previous.get("quantity",1))
        duration = None
        if service["kind"] == "video":
            duration = st.slider("Seconds per video",2,300,value=previous.get("duration_seconds",30),step=1)
            st.caption("2 seconds to 5 minutes in one-second increments. For longer work, select custom requirements and describe the duration below.")
        brief = st.text_area("Project requirements",value=previous.get("requirements",""),max_chars=10000)
        custom = st.checkbox("Custom requirements / request a quote",value=previous.get("custom_requirements",False))
        selection = dict(option=option, dimensions=dimensions, quantity=quantity, duration_seconds=duration, requirements=brief, custom_requirements=custom)
        _, pricing = validate_selection(slug,{**selection,"requirements":brief or "Pending brief"})
        show_price(pricing)
        st.caption(catalog["pricing_note"])
        if st.button("Proceed"):
            try:
                flow["selection"], flow["pricing"] = validate_selection(slug,selection)
            except ValueError as exc:
                st.warning(str(exc))
            else:
                flow["stage"] = "review"
                st.rerun()
        return
    st.subheader("Review your request")
    selection = flow["selection"]
    _, pricing = validate_selection(slug,selection)
    st.write(f"{selection['quantity']} × {selection['option']} · {selection['dimensions']}")
    if selection["duration_seconds"]:
        st.write(f"Duration per video: {selection['duration_seconds']} seconds")
    st.text(selection["requirements"])
    show_price(pricing)
    if st.button("Edit options"):
        flow["stage"] = "configure"
        st.rerun()
    with st.form(f"customer-{slug}"):
        name = st.text_input("Name",max_chars=120)
        email = st.text_input("Email",max_chars=254)
        phone = st.text_input("Phone (optional)",max_chars=40)
        consent = st.checkbox("I agree to storage of my details to handle this request.")
        submitted = st.form_submit_button("Submit request")
    if submitted:
        directory = Path(os.environ.get("PORTFOLIO_ORDER_DIR",str(Path(__file__).parent / "orders")))
        try:
            flow["receipt"] = save_order(directory,flow["id"],dict(service_id=slug,selection=selection,customer=dict(name=name,email=email,phone=phone),consent=consent))
        except ValueError as exc:
            st.warning(str(exc))
        except OSError:
            st.error("We could not finish saving your request. Please retry; your reference will not be duplicated.")
        else:
            st.rerun()
