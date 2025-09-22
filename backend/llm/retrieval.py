# pt/backend/llm/retrieval.py
from typing import List, Dict, Tuple
from collections import defaultdict

from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever

from .settings import TOP_K_VECTOR, N_MULTI_QUERIES, USE_HYDE, RRF_K
from .prompts import MULTI_QUERY_PROMPT, HYDE_PROMPT
from .utils import guess_labels_from_query

def _run_llm_rewrite_variants(llm: ChatGroq, query: str, n: int) -> List[str]:
    prompt = MULTI_QUERY_PROMPT.format(n_variants=n, query=query)
    out = llm.invoke(prompt).content
    variants = [line.strip(" •-") for line in out.split("\n") if line.strip()]
    return variants[:n] if len(variants) >= n else variants

def _run_hyde(llm: ChatGroq, query: str) -> str:
    out = llm.invoke(HYDE_PROMPT.format(query=query)).content
    return out.strip()

def _rrf_merge(rank_lists: List[List[Tuple[str, int]]], k: int = RRF_K) -> List[str]:
    """
    rank_lists: list of ranked lists; each item is (doc_id, rank starting at 1).
    Returns doc_ids sorted by fused score descending.
    """
    scores = defaultdict(float)
    for lst in rank_lists:
        for doc_id, rank in lst:
            scores[doc_id] += 1.0 / (k + rank)
    return [doc for doc, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

def _rankify(docs: List[Document]) -> List[Tuple[str, int]]:
    return [(d.metadata.get("id"), i+1) for i, d in enumerate(docs)]

def build_bm25_corpus(docs: List[Document]) -> BM25Retriever:
    bm = BM25Retriever.from_documents(docs)
    bm.k = TOP_K_VECTOR
    return bm

def retrieve_fused(
    llm: ChatGroq,
    vectorstore,                # Chroma
    all_docs: List[Document],   # to build BM25 once
    query: str,
    label_filter: List[str] | None = None
) -> List[Document]:
    """
    RAG-FUSION:
    1) generate multi-query variants with LLM
    2) (optional) HyDE synthetic answer as another query
    3) retrieve TOP_K from vectorstore per variant (+ optional filter)
    4) retrieve TOP_K from BM25 per variant
    5) RRF fuse all result lists
    """
    # 1) multi-queries
    variants = [query] + _run_llm_rewrite_variants(llm, query, N_MULTI_QUERIES)

    # 2) HyDE
    if USE_HYDE:
        hyde = _run_hyde(llm, query)
        if hyde:
            variants.append(hyde)

    # 3) vectorstore + 4) BM25
    bm25 = build_bm25_corpus(all_docs)

    ranked_lists = []
    doc_by_id = {}

    for v in variants:
        # semantic
        if label_filter:
            sem = vectorstore.similarity_search(
                v, k=TOP_K_VECTOR, filter={"body_part_label": {"$in": label_filter}}
            )
        else:
            sem = vectorstore.similarity_search(v, k=TOP_K_VECTOR)

        for d in sem: doc_by_id[d.metadata["id"]] = d
        ranked_lists.append(_rankify(sem))

        # lexical (bm25)
        lex = bm25.get_relevant_documents(v)
        for d in lex: doc_by_id[d.metadata["id"]] = d
        ranked_lists.append(_rankify(lex))

    # 5) RRF
    fused_ids = _rrf_merge(ranked_lists)
    fused_docs = [doc_by_id[i] for i in fused_ids if i in doc_by_id]
    return fused_docs
