# Sift

Sift is a self-hosted AI news intelligence platform built on NewsGator. It adds personalized headline filtering and relevance-aware article processing to help users focus on news that matters to them.

## What makes Sift different

- **Per-user interests:** Users select the categories they care about. Those interests guide which shared articles continue through processing.
- **Early headline screening:** Sift classifies headlines before retrieving full text. Articles clearly outside the effective interest scope can be filtered before more expensive processing begins.
- **Safe handling of ambiguity:** When a headline is ambiguous, Sift assigns the `Uncertain` fallback and continues to full-text processing instead of discarding the article early.
- **Body classification remains authoritative:** After retrieval, Sift classifies the article body. An out-of-scope body category is filtered before embeddings and clustering, even if the headline passed screening.
- **Visible, persistent filtering:** Filtered articles keep a persistent `filtered` state, and filtering outcomes appear in the Activity pipeline.

Together, these stages reduce unnecessary full-text retrieval, summarization, and embedding while keeping ambiguous stories eligible for a more informed decision.

## Versioning

Sift versions are independent from upstream NewsGator versions. The initial Sift release is **0.1.0**, based on **NewsGator 1.6.0**. Sift releases advance the Sift version; the recorded upstream version changes only when a newer NewsGator release is integrated. The authoritative values live in `backend/src/app/SIFT_VERSION` and `backend/src/app/NEWSGATOR_UPSTREAM_VERSION` and are reported by the application.

## Upstream project and attribution

Sift is based on the open-source [NewsGator project by Tekka90](https://github.com/Tekka90/NewsGator). The original project retains its applicable license and attribution; see [LICENSE](LICENSE).

For general platform features, installation instructions, architecture, and the original documentation, refer to [NewsGator](https://github.com/Tekka90/NewsGator).

## Development and maintenance

Sift keeps its customizations in Git alongside the upstream history. Upstream releases are reviewed and integrated into Sift while preserving Sift-specific changes. Release tags use Sift's version; the upstream version records the latest integrated NewsGator release.
