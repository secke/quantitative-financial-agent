#!/usr/bin/env python3
"""Launch script for the Financial Agent UI."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.gradio_app import create_ui
from src.utils.logger import log


def main():
    """Launch the Gradio UI."""
    try:
        log.info("=" * 70)
        log.info("Starting Financial Agent Web UI")
        log.info("=" * 70)

        # Create and launch UI
        ui = create_ui()

        log.info("UI created successfully")
        log.info("Launching on http://localhost:7860")
        log.info("Press Ctrl+C to stop the server")

        ui.launch(
            server_name="0.0.0.0",  # Allow external access
            server_port=7860,
            share=False,  # Set to True to create a public link
            show_error=True,
            show_api=False
        )

    except KeyboardInterrupt:
        log.info("\nShutting down gracefully...")
    except Exception as e:
        log.error(f"Error starting UI: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
