


from openai import OpenAI


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the API key
# openai.api_key = api_key
client = OpenAI(api_key=api_key)


board_prompt =  f"""
                Tic Tac Toe is a classic game played on a 3x3 grid. Let's represent this grid using a matrix.

                Take this matrix for example:
                [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]

                In the above matrix:
                - Each number represents a position on the board.
                - The numbers 1 to 9 correspond to the cells of the Tic Tac Toe grid, where players can place their symbols.

                Here's how the positions are laid out on the board:
                -------------------------
                |  1  |  2  |  3  |
                -------------------------
                |  4  |  5  |  6  |
                -------------------------
                |  7  |  8  |  9  |
                -------------------------

                Players take turns marking a cell with their chosen symbol, typically 'X' or 'O', until one player achieves a winning pattern or the board is full, resulting in a draw.

                You will strictly only return the matrix given above, which represents the initial state of the Tic Tac Toe board.
                """


def board():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # Choose the appropriate model
        messages=[
            {
                "role": "system",
                "content": "creating a matrix"
            },
            {
                "role": "user",
                "content":board_prompt
            }
        ]
    )
    board = response.choices[0].message.content
    return board




board = board()
print(board)





while True:

    def user_move_function(board):
        
        number = input("enter the number from 1 to 9")
        

        user_move_prompt = f"""
                In the current state of the Tic Tac Toe board:\n{board}

                You've entered the number {number}, indicating your desired position to place your 'X'.
                
                Here's the Tic Tac Toe board:
                -------------------------
                |  1  |  2  |  3  |
                -------------------------
                |  4  |  5  |  6  |
                -------------------------
                |  7  |  8  |  9  |
                -------------------------
                
        
                For example, if  number is '5', your symbol 'X' will be placed in the center cell of the board.
                
                Make sure to enter a number that represents an empty cell, otherwise, your move won't be valid.

                  Ensure that you follow these guidelines:
                - The number must be between 1 and 9.
                - The position indicated by the number must be unoccupied (i.e., not already marked by 'X' or 'O').
                - The updated board should be returned, reflecting the 'X' placed at the correct position.
                
                Please strictly return only the updated matrix representing the modified state of the Tic Tac Toe board.
                
                You must strictly return only the updated board after placing your symbol at the correct position specified by the number.
                """


        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",

            messages=[
            {
                "role":"system",
                "content":f"placing the symbol 'x' on the number={number} provided by the user in the matrix which is {board}" 
            },
            {
                "role":"user",
                "content":user_move_prompt
            }
            ]
        )

        board = response.choices[0].message.content
        return board


    board = user_move_function(board)
    print(board)

    def ai_move_function(board):
        ai_move_prompt = f"""
                You've been given the current state of the Tic Tac Toe board: {board}.
                
                Your task is to place the symbol 'O' on an empty position of the board.
                
                Ensure that you follow these guidelines:
                - Check for empty positions on the board.
                - Place the symbol 'O' on any available empty position.
                - Return the updated board with the 'O' placed at the correct position.
                
                Please strictly return only the updated matrix representing the modified state of the Tic Tac Toe board.
                """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",

            messages=[
            {
                "role":"system",
                "content":f"Placing your move in the board provided which is {board}making sure its placed on empty position " 
            },
            {
                "role":"user",
                "content":ai_move_prompt
            }
            ]
        )

        board = response.choices[0].message.content
        return board


    board = ai_move_function(board)
    print(board)
  


 
       
























