import datetime
import sys

import streamlit as st


def get_inputs() -> tuple[str, list[str]]:
    """Returns last modified data string and input files in single endpoint call."""
    last_indexed_files = []
    formatted_time = ""
    try:
        docs_list = st.session_state.vector_client.get_input_files()
        last_modified = max([x["seen_at"] for x in docs_list])

        docs_list.sort(
            key=lambda x: (x["seen_at"], x.get("path", x.get("name"))), reverse=True
        )

        for added_file in docs_list:
            full_path = added_file.get("path", added_file.get("name"))
            status = added_file.get("status")
            if full_path is None:
                continue
            name = full_path.split("/")[-1]
            if name in [
                "osservabilita-con-intelligenza-artificiale.pdf",
                "Design_and_Costmodeling.pdf",
                "Realtime Classification with Nearest Neighbors (1_2) _ Pathway.pdf",
                "Build an LLM App _ Pathway.pdf",
                "Use LLMs to Ingest Raw Text into DB _ Pathway.pdf",
                "Always up-to-date Vector Data Indexing pipeline _ Pathway.pdf",
                "2307.06435v9.pdf",
                "arxiv 2307.13116.pdf",
                "Launching Pathway + LlamaIndex.pdf",
                "LLM doc.pdf",
                "trading-con-excel.pdf",
                "Realtime Twitter Analysis App _ Pathway.pdf",
                "A data-driven approach to predicting diabetes and cardiovascular disease with machine learning.pdf",
                "pw.io.http _ Pathway.pdf",
            ]:
                continue
            last_indexed_files.append([name, status])
            formatted_time = datetime.datetime.fromtimestamp(last_modified)
            
    except Exception as e:
        print(f"Failed to get last indexed file: {e}", file=sys.stderr)
    return (f"Last document change: {formatted_time} UTC.", last_indexed_files)


# TODO: Remove these while going public, unless need to call other endpoints
def get_last_change() -> str:
    try:
        dt = st.session_state.vector_client.get_vectorstore_statistics()[
            "last_modified"
        ]
    except Exception as e:
        print(f"Failed to get status string: {e}", file=sys.stderr)
        return ""

    # if time.time() - dt > 3600:
    #     return f"No documents have been added by users yet."

    formatted_time = datetime.datetime.fromtimestamp(dt)
    return f"Last document change: {formatted_time} UTC."


async def async_get_last_change():
    return get_last_change()


async def async_get_inputs():
    return get_inputs()


import asyncio


async def call_endpoints():  # reduce lag to endpoint by half
    tasks = [async_get_last_change(), async_get_inputs()]

    results = await asyncio.gather(*tasks)
    return results
