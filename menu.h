#pragma once
using namespace std;

const string WORD_PROMT = "Âגוהטעו סכמגמ: ";
const string TRANSLATION_PROMT = "Âגוהטעו ןונוגמה: ";
const string FILENAME_PROMT = "Âגוהטעו טלÿ פאיכא: ";
const char SEPARATOR = ',';

pair<string, string> split(string, char);

class Menu {
public:
	void displayMenu();
	int getNumericInput();
	string getStringInput(const string);
};