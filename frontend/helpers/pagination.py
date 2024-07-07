import streamlit as st

# Number of items to display per page
ITEMS_PER_PAGE = 3

# Function to create an expanding list with pagination
def expander_with_pagination(
    title, items, item_renderer, expander_state_key, current_page_key
):
    with st.expander(title, expanded=st.session_state[expander_state_key]):
        if not items:
            st.warning("No current items")
        else:
            total_items = len(items)
            total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

            # Display items for the current page
            start_index = (st.session_state[current_page_key] - 1) * ITEMS_PER_PAGE
            end_index = start_index + ITEMS_PER_PAGE
            current_items = items[start_index:end_index]

            for item in current_items:
                item_renderer(item, current_page_key)
                st.write("---")

            # Pagination controls
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button(
                    "Previous",
                    key=f"prev_{expander_state_key}",
                    disabled=st.session_state[current_page_key] == 1,
                ):
                    st.session_state[current_page_key] -= 1
                    st.session_state[expander_state_key] = True
                    st.rerun()

            with col2:
                st.write(f"Page {st.session_state[current_page_key]} of {total_pages}")

            with col3:
                if st.button(
                    "Next",
                    key=f"next_{expander_state_key}",
                    disabled=st.session_state[current_page_key] == total_pages,
                ):
                    st.session_state[current_page_key] += 1
                    st.session_state[expander_state_key] = True
                    st.rerun()


