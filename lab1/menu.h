#pragma once
using namespace std;

const string WORD_PROMT = "Ââåäèòå ñëîâî: ";
const string TRANSLATION_PROMT = "Ââåäèòå ïåðåâîä: ";
const string FILENAME_PROMT = "Ââåäèòå èìÿ ôàéëà: ";
const char SEPARATOR = ',';

pair<string, string> split(string, char);

class Menu {
public:
	void displayMenu();
	int getNumericInput();
	string getStringInput(const string);
};
