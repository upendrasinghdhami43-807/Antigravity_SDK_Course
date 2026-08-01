from rich import print
from app.agent import ask

def main():
    print("[green]Hello Agent[/green]")
    question = input("You : ")
    answer = ask(question)
    print()
    print("[cyan]Agent :[/cyan]")
    print(answer)

if __name__ == "__main__":
    main()
