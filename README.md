# Red Flag Scanner

A Python command-line tool that analyzes dating conversations to identify potential red flags using rule-based behavioral analysis.

The project focuses on explainable logic rather than machine learning, making all decisions transparent and easy to reason about.

## Overview

Given a text-based conversation, the scanner:

- Extracts messages from the other participant
- Evaluates each message for predefined red flag signals
- Aggregates results across the conversation
- Calculates red flag density and category distribution
- Produces a final recommendation based on configurable thresholds

The goal is to detect problematic communication patterns in a deterministic and interpretable way.

## Features

- Message-level red flag detection
- Configurable phrase banks and thresholds
- Red flag density calculation (percentage of flagged messages)
- Category frequency tracking
- Escalation detection in recent messages
- Clear severity classification:
  - CONTINUE
  - CAUTION
  - LEAVE

## Red Flag Categories

The analyzer checks for patterns including:

- Vague or non-committal intent
- Deflection and avoidance
- Blame shifting
- Lack of accountability
- Gaslighting language
- Emotional unavailability
- Inconsistency
- Control or dismissal
- Low-effort replies
- Lack of engagement (no questions)

Each category is weighted to reflect relative severity.

## How It Works

1. The conversation is parsed into individual messages  
2. Messages sent by the other participant are isolated  
3. Each message is evaluated against:
   - phrase-based rules
   - effort and engagement heuristics  
4. Results are aggregated into summary metrics  
5. A final recommendation is produced using threshold-based logic  

All logic is rule-based and configurable in `rules.py`.

## Usage

Run the scanner from the project root:

```bash
python cli.py --file conversation.txt
```

The input file should follow this format:

```bash
Me: hey how was your day
Them: idk
Me: what are you looking for
Them: just seeing where things go
Me: okay
Them: lol
```

## Disclaimer

This project is for educational purposes only and is not intended to provide relationship advice.
