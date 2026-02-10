#pragma once
using namespace std;

const string WORD_PROMT = "Enter a word: ";
const string TRANSLATION_PROMT = "Enter a translation: ";
const string FILENAME_PROMT = "Enter file name: ";
const char SEPARATOR = ',';

/**
 * @class Menu
 * @brief Class responsible for handling program menu input/output.
 */
class Menu {
public:
    /**
     * @brief Display the menu in the console.
     */
    void displayMenu();

    /**
     * @brief Read a valid numeric input.
     * @return A number from 0 to 6.
     */
    int getNumericInput();

    /**
     * @brief Read a string input.
     * @param promt Text of the prompt.
     * @return Entered string.
     */
    string getStringInput(const string);
};
