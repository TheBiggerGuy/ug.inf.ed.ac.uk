#include <iostream>
#include <map>
#include <stack>
 
enum Symbols {
    // the symbols:
    // Terminal symbols:
    TS_L_PARENS,    // (
    TS_R_PARENS,    // )
    TS_A,           // a
    TS_PLUS,        // +
    TS_EOS,         // $, in this case corresponds to '\0'
    TS_INVALID,     // invalid token

    // Non-terminal symbols:
    NTS_S,          // S
    NTS_F
};
 
/* 
Converts a valid token to the corresponding terminal symbol
*/
enum Symbols lexer(char c)
{
    switch(c)
    {
    case '(':
            return TS_L_PARENS;
            break;

    case ')':
            return TS_R_PARENS;
            break;

    case 'a':
            return TS_A;
            break;

    case '+':
            return TS_PLUS;
            break;

    case '\0':  // this will act as the $ terminal symbol
            return TS_EOS;
            break;

    default:
            return TS_INVALID;
            break;
    }
}
 
int main(int argc, char **argv)
{
    using namespace std;

    if (argc < 2)
    {
        cout << "usage:\n\tll '(a+a)'" << endl;
        return 0;
    }

    map< enum Symbols, map<enum Symbols, int> > table; // LL parser table, maps < non-terminal, terminal> pair to action        
    stack<enum Symbols>    ss;    // symbol stack
    char *p;     // input buffer

    // initialize the symbols stack
    ss.push(TS_EOS);    // terminal, $
    ss.push(NTS_S);     // non-terminal, S

    // initialize the symbol stream cursor
    p = &argv[1][0];

    // setup the parsing table
    table[NTS_S][TS_L_PARENS] = 2;   table[NTS_S][TS_A] = 1;
    table[NTS_F][TS_A] = 3;

    while(ss.size() > 0)
    {
        if(lexer(*p) == ss.top())
        {
            cout << "Matched symbols: " << lexer(*p) << endl;
            p++;
            ss.pop();
        }
        else
        {
            cout << "Rule " << table[ss.top()][lexer(*p)] << endl;
            switch(table[ss.top()][lexer(*p)])
            {
            case 1:      // 1. S → F
                    ss.pop();
                    ss.push(NTS_F);     // F
                    break;

            case 2:      // 2. S → ( S + F )
                    ss.pop();
                    ss.push(TS_R_PARENS);       // )
                    ss.push(NTS_F);             // F
                    ss.push(TS_PLUS);   // +
                    ss.push(NTS_S);             // S
                    ss.push(TS_L_PARENS);       // (
                    break;

            case 3:      // 3. F → a
                    ss.pop();
                    ss.push(TS_A);      // a
                    break;

            default:
                    cout << "parsing table defaulted" << endl;
                    return 0;
                    break;
            }
        }
    }

    cout << "finished parsing" << endl;

    return 0;
}
