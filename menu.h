#pragma once
using namespace std;

const string WORD_PROMT = "������� �����: ";
const string TRANSLATION_PROMT = "������� �������: ";
const string FILENAME_PROMT = "������� ��� �����: ";
const char SEPARATOR = ',';

pair<string, string> split(string, char);

class Menu {
public:
	void displayMenu();
	int getNumericInput();
	string getStringInput(const string);
};