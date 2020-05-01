// Wen Liang Goh - https://github.com/wenlianggg
// 29 April 2020
// Snake game within a 7x7 grid, with an initial length of 4

#include <queue>
#include <vector>
#include <iostream>

using namespace std;

namespace SnakeSpace {
    
    class Snake {

        public:
            deque<vector<int>> queue;

            void new_game(int length, int row, int col) {
                for (int i; i < length; i++) {
                    queue.push_back({row, col});
                }
            }

            void move(char direction, bool grow) {
                vector<int> head = queue.back();
                switch (direction) {
                    case 'n':
                        queue.push_back({ head[0]-1, head[1] });
                        break;
                    case 's':
                        queue.push_back({ head[0]+1, head[1] });
                        break;
                    case 'e':
                        queue.push_back({ head[0], head[1]+1 });
                        break;
                    case 'w':
                        queue.push_back({ head[0], head[1]-1 });
                        break;
                }

                if (!grow) {
                    queue.pop_front();
                }
            }

            void get_state(vector<vector<bool>> &grid) {
                for (vector<int>& coord : queue) {
                    cout << coord[0] << " " << coord[1] << endl;
                    grid[coord[0]][coord[1]] = true;
                }
            }
    };
}

void printvec(vector<vector<bool>> v) {
    for (int i = 0; i < v.size(); i++) {
        for (int j = 0; j< v.size(); j++) {
            cout << v[i][j] << "|";
        }
        cout << endl;
    }
}

int main() {
    vector<vector<bool>> gridtemplate;

    // TODO: Neater way of generating new grid template
    for (int i; i < 7; i++) {
        gridtemplate.push_back({false, false, false, false, false, false, false});
    }

    SnakeSpace::Snake s;
    s.new_game(4, 1, 3);
    vector<vector<bool>> grid(gridtemplate);
    s.get_state(grid);
    printvec(grid);

    // TODO: Ask user for input
    s.move('s', false);
    s.move('s', false);
    s.move('e', false);
    s.move('e', true);
    s.move('n', false);
    s.move('n', true);
    s.move('w', true);
    s.move('w', true);
    s.move('w', false);

    vector<vector<bool>> grid2(gridtemplate);
    s.get_state(grid2);
    printvec(grid2);
    
    return 0;
}
