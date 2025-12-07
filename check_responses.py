#!/usr/bin/env python3
"""
Utility script to manually check for email responses
"""

import sys
from response_detector import ResponseDetector
from logger_config import EmailLogger

logger = EmailLogger("check_responses")

def main():
    logger.info("Email Response Checker")
    logger.info("=" * 50)
    
    try:
        detector = ResponseDetector()
        
        # Check for responses
        logger.info("Checking Gmail for responses...")
        new_replies = detector.check_responses()
        
        if new_replies:
            logger.success(f"Found {len(new_replies)} new responses!\n")
            for i, reply in enumerate(new_replies, 1):
                print(f"  {i}. {reply['email']}")
                print(f"     Replied on: {reply['reply_date']}")
                if reply['subject']:
                    print(f"     Subject: {reply['subject']}")
                print()
        else:
            logger.info("No new responses found.")
        
        # Show statistics
        stats = detector.get_response_stats()
        if stats:
            logger.info("\n" + "=" * 50)
            logger.info("Response Statistics:")
            logger.info("=" * 50)
            print(f"  Total Sent:      {stats['total_sent']}")
            print(f"  Total Replied:   {stats['total_replied']}")
            print(f"  No Response:     {stats['no_response']}")
            print(f"  Response Rate:   {stats['response_rate']}%")
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.info("\nMake sure EMAIL_ADDRESS and EMAIL_PASSWORD are set in environment variables.")
        sys.exit(1)
    
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        logger.info("\nTroubleshooting:")
        logger.info("  1. Check your internet connection")
        logger.info("  2. Verify Gmail credentials are correct")
        logger.info("  3. Ensure IMAP is enabled in Gmail settings")
        logger.info("  4. Check if you're using App Password (not regular password)")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
