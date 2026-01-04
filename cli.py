import argparse
from analyzer import analyze

def print_results(result):
    print("\nRed Flag Scan Results")
    print("-" * 25)

    if not result["flags"]:
        print("No obvious red flags detected.")
        print("Either this is healthy… or it’s too early to tell.")
    else:
        print("Red flags detected:\n")
        for category, value in result["flags"].items():
            if isinstance(value, list):
                for phrase in value:
                    print(f"- {category.replace('_', ' ').title()}: \"{phrase}\"")
            else:
                print(f"- {category.replace('_', ' ').title()}")

    print("\nSuggested next move:")
    if result["severity"] == "LEAVE":
        print("It might be time to disengage. The patterns here aren’t great.")
    elif result["severity"] == "CAUTION":
        print("Proceed carefully. Something feels a bit off.")
    else:
        print("No major issues spotted. You can probably keep the conversation going.")

        print("\nWhy this recommendation was made:")
        for category in result["flags"].keys():
            print(f"- {category.replace('_', ' ').title()}")



def main():
    parser = argparse.ArgumentParser(
        description="Scan a conversation for common dating red flags"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to a conversation text file"
    )
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        conversation_text = f.read()

    result = analyze(conversation_text)
    print_results(result)

if __name__ == "__main__":
    main()
