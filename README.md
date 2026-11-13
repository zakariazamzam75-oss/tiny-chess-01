# Tiny Chess 4K: Deterministic Tactical Heuristic

A compact Python chess bot for Make.fun's `tiny-chess-01` competition. It uses only the standard library and selects moves from the environment's supplied legal UCI move list.

The root-move heuristic values captures, promotions, piece-square and center preferences, and penalizes non-king pieces left on squares attacked by an opponent. It is deterministic and keeps its work fixed. It does not search future plies, so this is a compact tactical heuristic rather than a full minimax chess engine.

The entry communicates with the game environment through `MAKEFUN_ENV_URL` and exits after all games are complete. `main.py` is designed to remain within the 4,096-byte source limit.
