import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chat import ChatSession

def main():
    session = ChatSession()
    session.run()

if __name__ == "__main__":
    main()
