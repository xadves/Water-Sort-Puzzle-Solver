# 1 brown
# 2 med green
# 3 light green
# 4 gray
# 5 light blue
# 6 red
# 7 yellow
# 8 pink
# 9 purple 
# 10 dark blue
# 11 orange
# 12 dark green

def printBoard(b):
    for x in b:
        print(x.pieces)

class vial:
    def __init__(self, pieces):
        self.pieces = [ele for ele in reversed(pieces)]
    def space(self, bits):
        if (len(self.pieces) + bits) > 4:
            return False
        else:
            return True
    def lastPiece(self, piece):
        if (len(self.pieces) > 0):
            if (piece == self.pieces[-1]):
                return True
            else:
                return False
        else:
            return True
        
    # Make sure we have a valid winning vial
    def complete(self):
        if (len(self.pieces) > 0):
            item = self.pieces[-1]
            if (len(self.pieces) == 4):
                for x in self.pieces:
                    if (item != x):
                        return False
            else:
                return False
        return True

    # Determine the top color and amount that we are going to move
    def topBits(self):
        p = [ele for ele in self.pieces]
        color = 0
        counter = 0
        if (len(p)>0):
            color = p[-1]
            while (len(p)>0):
                c = p.pop()
                if (color == c):
                    counter = counter + 1
                else:
                    break
        return [color, counter]

    # Wrote this because I was annoyed how lists and classes work.  
    def annoyVial(self):
        return [ele for ele in reversed(self.pieces)]


level127 = [
    vial([1,2,1,3]),
    vial([3,4,5,2]),
    vial([6,2,3,7]),
    vial([8,6,7,9]),
    vial([3,8,6,2]),
    vial([4,10,8,4]),
    vial([11,10,7,12]),
    vial([9,11,11,12]),
    vial([5,10,11,6]),
    vial([9,12,12,5]),
    vial([7,8,9,10]),
    vial([5,1,1,4]),
    vial([]),
    vial([])
]
level128 = [
    vial([2,9,5,6]),
    vial([2,8,6,5]),
    vial([11,9,9,11]),
    vial([10,10,11,6]),
    vial([6,4,8,9]),
    vial([10,4,8,4]),
    vial([8,5,2,3]),
    vial([10,4,3,3]),
    vial([5,3,2,11]),
    vial([]),
    vial([])
]
oBoard = level127

# Check our board makes sense.
validChecker = [0 for x in range(20)]
for b in oBoard:
    for x in b.pieces:
        validChecker[x] = validChecker[x] + 1 
valid = True
for x in validChecker:
    if ((x != 0) and (x != 4)):
        print(x)
        valid = False
if valid:
    print("The board is valid!")

# init our variables and copy the board
board = oBoard.copy()
printBoard(board)
badMoves = [[0,0,0]]
currentMove = []
newBoard = []
for v in board:
    newBoard.append(vial(v.annoyVial()))
currentMove.append(newBoard.copy())
iteration = 0
moveSet = []
badBranch = False
badBranches = 0
winCondition = True

# Function we use in the loop to check if we've tried this move before. A little crude, but it's worked so far. 
def checkMoves(inx, moves):
    for x in moves:
        if inx == x:
            return False
    return True

# keep playing until we win
while winCondition and valid:
    # Count our iterations and assume this run will fail.
    iteration = iteration + 1
    successRun = False
    for i in range(len(board)):
        # Grab our first piece and see if there is a fit
        foundSpace = False
        # Check the movable piece, if it has size and color. Else go to the next vial.
        topBits = board[i].topBits()
        if (topBits[0] == 0):
            continue
        if (topBits[1] == 0):
            continue
        

        # Check all the vials for a spot
        for x in range(len(board)):
            if i == x:
                continue
            # Check if we have enough room, the color matches, and we havent already tried this branch
            if ((board[x].space(topBits[1])) and (board[x].lastPiece(topBits[0])) and checkMoves([i, len(board[i].pieces), x, len(currentMove)], badMoves)):
                # if this is moving a single color vial to an empty one, ignore it. else we triple our move set
                if ((topBits[1] == len(board[i].pieces)) and (len(board[x].pieces) == 0)):
                    continue
                # Keep track of this as a list of moves we dont want to do
                badMoves.append([i, len(board[i].pieces), x, len(currentMove)])
                # Tell the user we are making this move. Vial-Space to new Vial
                print("Move[" + str(len(currentMove)+1) + "] " + str(i+1) + "-" + str(len(board[i].pieces)) + " moves to " + str(x+1))
                # Copy the state of the board so we can return to it later if needed
                newBoard = []
                for v in board:
                    newBoard.append(vial(v.annoyVial()))
                currentMove.append(newBoard.copy())
                # Keep track of the moves we've made so we can display it later.
                moveSet.append([i+1, x+1])
                # Actually make the move
                for y in range(topBits[1]):
                    board[i].pieces.pop()
                    board[x].pieces.append(topBits[0])
                # Mark bools to get out of the loops
                foundSpace = True
                successRun = True
                break

        # Stop try to find a move
        if foundSpace:
            break

    # Check for winning Condition. The bool is backwards because of the while loop. Assumme we won.
    winCondition = False
    for v in board:
        if not v.complete():
            winCondition = True
            # Victory not made, make sure we found a move from before. if so, leave now.
            if successRun:
                badBranch = False
                break
            # Naming is a little odd, check if we came from a bad branch for metrics sake
            if not badBranch:
                badBranch = True
                badBranches = badBranches + 1
            # Reset the board to the last known state
            board = []
            for va in currentMove.pop():
                board.append(vial(va.annoyVial()))
            # This may actually be useless 
            if len(moveSet) > 0:
                moveSet.pop()
            # Alert the user we are backtracking, and to what move.
            print("No moves found, reverting to last state- Move", len(currentMove))
            break

    if not winCondition:
        # Print out our Move set, and metrics
        for x in range(len(moveSet)):
            print("Move:", x+1, moveSet[x])
        print("Victory!! Iterations:", iteration, "Bad Branches:", badBranches)