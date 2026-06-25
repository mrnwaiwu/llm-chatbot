# Changelog

## [Unreleased]
- Planned: conversation history persistence
- Planned: support for multiple Claude model versions

## [1.2.4] - 2026-06-25
- Improved error handling in streaming SSE responses for dropped connections
- Added per-session token budget enforcement with configurable hard limits
- Fixed edge case in token counting when system prompt contains special characters

## [1.2.3] - 2026-06-21
- Minor improvements to session cleanup logging
- Small fixes to token usage reporting edge cases

## [1.2.2] - 2026-06-14
- Improved token usage logging for cost tracking
- Fixed null reference in session cleanup on idle timeout
- Added configurable max_tokens cap per conversation

## [1.2.1] - 2026-06-07
- Improved context window management for long conversations
- Fixed edge case in message deduplication on reconnect
- Added retry backoff for transient API errors

## [1.2.0] - 2026-05-28
- Minor improvements to token handling and error recovery
- Improved prompt sanitization for safety

## [1.1.0] - 2026-05-25
- Added streaming responses via SSE
- Updated browser UI to render streamed tokens in real time

## [1.0.0] - 2026-05-21
- Initial release
- FastAPI backend with Claude (Anthropic) integration
- Basic browser UI for chat
