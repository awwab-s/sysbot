# Discord AI Bot

## Overview

This is a Discord bot built with discord.py that integrates AI capabilities through OpenRouter's API. The bot features basic utility commands and AI chat functionality, designed to run as a persistent service with uptime monitoring and console interaction capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py Library**: Uses discord.py 2.6.3 as the core framework for Discord API interactions
- **Cogs System**: Modular command organization with separate cogs for general utilities and AI functionality
- **Command Prefix**: Configurable command prefix system for bot invocation
- **Intents**: Configured with message content intent for reading and processing messages

### AI Integration
- **OpenRouter API**: Integrates with OpenRouter's API for AI chat completions
- **Model Configuration**: Supports configurable AI models through environment variables (CHAT_MODEL)
- **Rate Limiting**: Implements retry logic with exponential backoff for API rate limits
- **Daily Limits**: Built-in request limiting (50 requests per 24 hours) to manage API usage
- **Response Management**: Truncates overly long responses and handles empty responses gracefully

### Configuration Management
- **Environment Variables**: Uses python-dotenv for secure configuration management
- **Required Variables**: TOKEN, PREFIX, CHANNEL_ID, CHAT_API_KEY, CHAT_MODEL
- **Centralized Config**: Single config.py file for all environment variable access

### Persistence & Monitoring
- **Flask Web Server**: Lightweight web server for health checks and keeping the bot alive on hosting platforms
- **Uptime Tracking**: Monitors bot uptime and reports disconnections to a configured channel
- **Console Interface**: Asynchronous console input system for direct bot interaction
- **Debug Logging**: Command execution logging with user and channel information

### Command Structure
- **General Commands**: Basic utility commands (hello, ping, help, userinfo, uptime)
- **AI Commands**: AI interaction commands with error handling and response formatting
- **Custom Help System**: Disabled default help command in favor of custom implementation

## External Dependencies

### Core Dependencies
- **discord.py**: Discord API wrapper and bot framework
- **aiohttp**: Asynchronous HTTP client for API requests
- **Flask**: Lightweight web framework for health check endpoints
- **python-dotenv**: Environment variable management

### External Services
- **Discord API**: Primary platform integration for bot functionality
- **OpenRouter API**: AI model access and chat completions
- **Hosting Platform**: Designed for platforms that require HTTP endpoints for service persistence

### API Integrations
- **OpenRouter Chat Completions**: RESTful API integration with authentication, rate limiting, and error handling
- **Discord Gateway**: WebSocket connection for real-time message processing and bot presence