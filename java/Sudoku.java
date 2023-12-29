package palygame;

public class Sudoku {
    char[][] a = new char[9][9];
    int count = 0;

//    public void aaadc(char[][] ans ){
//        for (int i = 0; i < ans.length; i++) {
//            for (int j = 0; j < ans[i].length; j++) {
//                System.out.print(ans[i][j]+"\t");
//            }
//            System.out.println();
//        }
//        System.out.println("---------------------------------------------------------------------");
//    }
    public void aaad(){
        for (int i = 0; i < this.a.length; i++) {
            for (int j = 0; j < this.a[i].length; j++) {
                System.out.print(this.a[i][j]+"\t");
            }
            System.out.println();
        }
        System.out.println("---------------------------------------------------------------------");
    }

    public boolean isValidSudoku(char[][] board) {
        boolean[][] row = new boolean[9][9];
        boolean[][] col = new boolean[9][9];
        boolean[][] block = new boolean[9][9];
        for (int i=0;i<9;i++){
            for (int j=0;j<9;j++){
                int a = board[i][j];
                if (a != '.'){
                    int num = a - '1';
//                     int c = i<3?0:i>=6?4:2;
//                     int numblock = j/3+i/3+c;
                    int numblock = j/3+i/3*3;
                    if (row[i][num] || col[j][num] || block[numblock][num]){
                        return false;
                    } else {
                        row[i][num] = true;
                        col[j][num] = true;
                        block[numblock][num] = true;
                    }
                }
            }
        }
        return true;
    }

    public void copychar(char[][] ans){
        for (int i = 0;i<9;i++) {
            for (int j = 0; j < 9; j++) {
                this.a[i][j] = ans[i][j];
            }
        }
    }

    public void playgame(char[][] ans){
        copychar(ans);
        boolean[][] row = new boolean[9][9];
        boolean aab = false;
        for (int x=0;x<9;x++){
            int y=0;
            if (aab){
                y=8;
                aab = false;
            }
            for (;y<9;y++){
                if (y == -1){
                    x -= 2;
                    aab = true;
//                    this.count++;
//                    System.out.println(this.count+"\t已撤回一个排");
                    break;
                }

                if (ans[x][y] != '.' && row[x][y]){
                    row[x][y] = false;
                    y -= 2;
                    continue;
                }
                if (ans[x][y] != '.'){
                    row[x][y] = true;
                    continue;
                }
                for (int z=1;z<=10;z++){
                    System.out.println(this.count++);
                    if (this.a[x][y] !='.'){
                        z = ((int)(this.a[x][y])-(int)'0')+1;
                        if (this.a[x][y] == '9')this.a[x][y]='.';
                    }
                    if (z == 10){
                        y -= 2;
//                        this.count++;
//                        System.out.println(this.count+"\t已撤回一个数");
                        break;
                    }
                    a[x][y] = (char)(z+48);
                    if (isValidSudoku(a)){
//                        this.count++;
//                        System.out.println(this.count+"\t已填入一个数");
                        break;
                    }else a[x][y]='.';
                }
            }
        }
    }

}

class A{
    public static void main(String[] args) {
        Sudoku su = new Sudoku();
        char[][] board =  {{'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'},
                           {'.','.','.','.','.','.','.','.','.'}};
        su.playgame(board);
        su.aaad();
//        System.out.println(su.isValidSudoku(board));
//        su.aaadc(board);
//        System.out.println(su.isValidSudoku1(board));
    }
}
