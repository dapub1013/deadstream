"""
Standardized Error Messages for DeadStream

Phase 10E.7: Provides user-friendly error messages with helpful recovery suggestions.

This module centralizes all error messages to ensure consistency and provide
helpful guidance to users when things go wrong.
"""


class ErrorMessages:
    """
    Standardized error messages with helpful recovery suggestions.

    Each error type provides:
    - title: Short error title for the dialog
    - message: User-friendly description of what went wrong
    - suggestion: Helpful guidance on what the user can do
    """

    # Network Errors
    NETWORK_CONNECTION = {
        "title": "Network Error",
        "message": "Unable to connect to the internet",
        "suggestion": "Check your network connection and try again"
    }

    NETWORK_TIMEOUT = {
        "title": "Connection Timeout",
        "message": "The connection timed out while trying to reach archive.org",
        "suggestion": "Your network may be slow. Wait a moment and try again"
    }

    NETWORK_ARCHIVE_DOWN = {
        "title": "Archive.org Unavailable",
        "message": "Cannot reach archive.org servers",
        "suggestion": "Archive.org may be temporarily down. Try again later"
    }

    # Database Errors
    DATABASE_NOT_FOUND = {
        "title": "Database Not Found",
        "message": "The shows database could not be found",
        "suggestion": "Run the database initialization script: python3 scripts/init_database.py"
    }

    DATABASE_CORRUPT = {
        "title": "Database Error",
        "message": "The database appears to be corrupted or incomplete",
        "suggestion": "Try re-initializing the database or restoring from backup"
    }

    DATABASE_QUERY_FAILED = {
        "title": "Database Query Failed",
        "message": "An error occurred while searching the database",
        "suggestion": "Try restarting the application. If the problem persists, rebuild the database"
    }

    # Playback Errors
    PLAYBACK_NO_AUDIO = {
        "title": "Playback Error",
        "message": "Unable to load audio for this recording",
        "suggestion": "Try selecting a different recording of the same show"
    }

    PLAYBACK_STREAM_FAILED = {
        "title": "Stream Failed",
        "message": "The audio stream stopped unexpectedly",
        "suggestion": "Check your network connection or try a different recording"
    }

    PLAYBACK_FORMAT_UNSUPPORTED = {
        "title": "Format Not Supported",
        "message": "This audio format is not supported",
        "suggestion": "Try selecting a different recording with a supported format (MP3, FLAC)"
    }

    PLAYBACK_DEVICE_ERROR = {
        "title": "Audio Device Error",
        "message": "Cannot access audio output device",
        "suggestion": "Check your audio settings and ensure speakers/headphones are connected"
    }

    # API Errors
    API_RATE_LIMIT = {
        "title": "Too Many Requests",
        "message": "Archive.org is limiting our requests",
        "suggestion": "Wait a minute before trying again"
    }

    API_NOT_FOUND = {
        "title": "Recording Not Found",
        "message": "This recording is no longer available on archive.org",
        "suggestion": "Try searching for a different recording of the same show"
    }

    API_METADATA_FAILED = {
        "title": "Metadata Load Failed",
        "message": "Cannot retrieve show information from archive.org",
        "suggestion": "Try again in a moment, or skip to a different show"
    }

    # Search Errors
    SEARCH_NO_RESULTS = {
        "title": "No Shows Found",
        "message": "Your search didn't match any shows",
        "suggestion": "Try a different search term, date, or venue name"
    }

    SEARCH_INVALID_DATE = {
        "title": "Invalid Date",
        "message": "The date you entered is not valid",
        "suggestion": "Check the date format and try again"
    }

    # Selection Errors
    SELECTION_NO_RECORDINGS = {
        "title": "No Recordings Available",
        "message": "No audio recordings are available for this show",
        "suggestion": "Try browsing for a different show or date"
    }

    SELECTION_QUALITY_TOO_LOW = {
        "title": "Recording Quality Low",
        "message": "No high-quality recordings found for this show",
        "suggestion": "Adjust your quality preferences in settings, or choose a different show"
    }

    # System Errors
    SYSTEM_PERMISSION_DENIED = {
        "title": "Permission Denied",
        "message": "The application doesn't have permission to access required resources",
        "suggestion": "Check file permissions or run the application with appropriate privileges"
    }

    SYSTEM_DISK_FULL = {
        "title": "Disk Space Low",
        "message": "Not enough disk space for caching audio",
        "suggestion": "Free up some disk space or reduce cache size in settings"
    }

    SYSTEM_UNKNOWN = {
        "title": "Unexpected Error",
        "message": "An unexpected error occurred",
        "suggestion": "Try restarting the application. If the problem persists, check logs"
    }


class ErrorMessageFormatter:
    """
    Helper class to format error messages with optional custom details.
    """

    @staticmethod
    def format_error(error_dict, custom_message=None, custom_suggestion=None, details=None):
        """
        Format an error message with optional customization.

        Args:
            error_dict: Error dictionary from ErrorMessages class
            custom_message: Optional override for the message
            custom_suggestion: Optional override for the suggestion
            details: Optional technical details to append

        Returns:
            dict: Formatted error with title, message, suggestion, details
        """
        return {
            "title": error_dict["title"],
            "message": custom_message or error_dict["message"],
            "suggestion": custom_suggestion or error_dict["suggestion"],
            "details": details
        }

    @staticmethod
    def format_network_error(exception, custom_suggestion=None):
        """
        Format a network error from an exception.

        Args:
            exception: The exception that occurred
            custom_suggestion: Optional custom suggestion

        Returns:
            dict: Formatted error
        """
        error_msg = str(exception)

        if "timeout" in error_msg.lower():
            base_error = ErrorMessages.NETWORK_TIMEOUT
        elif "connection" in error_msg.lower():
            base_error = ErrorMessages.NETWORK_CONNECTION
        else:
            base_error = ErrorMessages.NETWORK_ARCHIVE_DOWN

        return ErrorMessageFormatter.format_error(
            base_error,
            custom_suggestion=custom_suggestion,
            details=error_msg
        )

    @staticmethod
    def format_playback_error(exception, custom_suggestion=None):
        """
        Format a playback error from an exception.

        Args:
            exception: The exception that occurred
            custom_suggestion: Optional custom suggestion

        Returns:
            dict: Formatted error
        """
        error_msg = str(exception)

        if "format" in error_msg.lower() or "codec" in error_msg.lower():
            base_error = ErrorMessages.PLAYBACK_FORMAT_UNSUPPORTED
        elif "device" in error_msg.lower() or "audio" in error_msg.lower():
            base_error = ErrorMessages.PLAYBACK_DEVICE_ERROR
        elif "stream" in error_msg.lower():
            base_error = ErrorMessages.PLAYBACK_STREAM_FAILED
        else:
            base_error = ErrorMessages.PLAYBACK_NO_AUDIO

        return ErrorMessageFormatter.format_error(
            base_error,
            custom_suggestion=custom_suggestion,
            details=error_msg
        )

    @staticmethod
    def format_database_error(exception, custom_suggestion=None):
        """
        Format a database error from an exception.

        Args:
            exception: The exception that occurred
            custom_suggestion: Optional custom suggestion

        Returns:
            dict: Formatted error
        """
        error_msg = str(exception)

        if "not found" in error_msg.lower() or "no such table" in error_msg.lower():
            base_error = ErrorMessages.DATABASE_NOT_FOUND
        elif "corrupt" in error_msg.lower() or "malformed" in error_msg.lower():
            base_error = ErrorMessages.DATABASE_CORRUPT
        else:
            base_error = ErrorMessages.DATABASE_QUERY_FAILED

        return ErrorMessageFormatter.format_error(
            base_error,
            custom_suggestion=custom_suggestion,
            details=error_msg
        )


# Convenience functions for quick error formatting
def format_no_shows_error(search_term):
    """Format a 'no shows found' error with the search term"""
    return {
        "title": ErrorMessages.SEARCH_NO_RESULTS["title"],
        "message": f"No shows found matching '{search_term}'",
        "suggestion": ErrorMessages.SEARCH_NO_RESULTS["suggestion"],
        "details": None
    }


def format_date_error(date_string):
    """Format an invalid date error with the attempted date"""
    return {
        "title": ErrorMessages.SEARCH_INVALID_DATE["title"],
        "message": f"'{date_string}' is not a valid date",
        "suggestion": ErrorMessages.SEARCH_INVALID_DATE["suggestion"],
        "details": None
    }


def format_no_recordings_error(show_date):
    """Format a 'no recordings' error for a specific show"""
    return {
        "title": ErrorMessages.SELECTION_NO_RECORDINGS["title"],
        "message": f"No audio recordings available for {show_date}",
        "suggestion": ErrorMessages.SELECTION_NO_RECORDINGS["suggestion"],
        "details": None
    }
