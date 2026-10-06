// File: DimacsParser.hpp
#ifndef DIMACS_PARSER_HPP
#define DIMACS_PARSER_HPP

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

struct Clause {
    std::vector<int> literals;
};

class DimacsParser {
public:
    int numVariables = 0;
    int numClauses = 0;
    std::vector<Clause> clauseRegistry;

    bool parseFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "[ERROR] Could not open DIMACS target: " << filename << std::endl;
            return false;
        }

        std::string line;
        while (std::getline(file, line)) {
            if (line.empty() || line[0] == 'c') continue; // Skip comments smoothly

            if (line[0] == 'p') {
                std::stringstream ss(line);
                std::string dummy, format;
                ss >> dummy >> format >> numVariables >> numClauses;
                continue;
            }

            std::stringstream ss(line);
            Clause currentClause;
            int literal;
            while (ss >> literal) {
                if (literal == 0) {
                    clauseRegistry.push_back(currentClause);
                    break;
                }
                currentClause.literals.push_back(literal);
            }
        }
        file.close();
        return true;
    }
};

#endif
